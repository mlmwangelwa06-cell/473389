"""
Stock Predictor Bot - With Electronic Device Prices
"""

import logging
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = "8709139209:AAEDzbFiR2EQ713b-Nz_GcybP-_C6FVnuE4"

logging.basicConfig(level=logging.INFO)

# Create folder for charts
os.makedirs("charts", exist_ok=True)

# Electronic devices database
# Electronic devices database
ELECTRONIC_DEVICES = {
    # iPhones (no underscores needed)
    'iphone15': {'name': 'iPhone 15', 'price': 799, 'category': 'Smartphone'},
    'iphone15pro': {'name': 'iPhone 15 Pro', 'price': 999, 'category': 'Smartphone'},
    'iphone15promax': {'name': 'iPhone 15 Pro Max', 'price': 1199, 'category': 'Smartphone'},
    'iphone14': {'name': 'iPhone 14', 'price': 699, 'category': 'Smartphone'},
    'iphone14pro': {'name': 'iPhone 14 Pro', 'price': 899, 'category': 'Smartphone'},

    # MacBooks
    'macbookair': {'name': 'MacBook Air M2', 'price': 1099, 'category': 'Laptop'},
    'macbookpro14': {'name': 'MacBook Pro 14"', 'price': 1999, 'category': 'Laptop'},
    'macbookpro16': {'name': 'MacBook Pro 16"', 'price': 2499, 'category': 'Laptop'},

    # Graphics Cards (simple names)
    'rtx4090': {'name': 'NVIDIA RTX 4090', 'price': 1599, 'category': 'Graphics Card'},
    'rtx4080': {'name': 'NVIDIA RTX 4080', 'price': 1199, 'category': 'Graphics Card'},
    'rtx4070': {'name': 'NVIDIA RTX 4070', 'price': 599, 'category': 'Graphics Card'},
    'rtx4060': {'name': 'NVIDIA RTX 4060', 'price': 299, 'category': 'Graphics Card'},
    'rx7900xtx': {'name': 'AMD RX 7900 XTX', 'price': 999, 'category': 'Graphics Card'},
    'rx7800xt': {'name': 'AMD RX 7800 XT', 'price': 499, 'category': 'Graphics Card'},

    # Gaming Consoles
    'ps5': {'name': 'PlayStation 5', 'price': 499, 'category': 'Gaming Console'},
    'ps5digital': {'name': 'PlayStation 5 Digital', 'price': 399, 'category': 'Gaming Console'},
    'xboxseriesx': {'name': 'Xbox Series X', 'price': 499, 'category': 'Gaming Console'},
    'xboxseriess': {'name': 'Xbox Series S', 'price': 299, 'category': 'Gaming Console'},
    'nintendoswitch': {'name': 'Nintendo Switch OLED', 'price': 349, 'category': 'Gaming Console'},

    # Processors
    'i913900k': {'name': 'Intel Core i9-13900K', 'price': 589, 'category': 'Processor'},
    'i713700k': {'name': 'Intel Core i7-13700K', 'price': 409, 'category': 'Processor'},
    'i513600k': {'name': 'Intel Core i5-13600K', 'price': 319, 'category': 'Processor'},
    'ryzen97950x': {'name': 'AMD Ryzen 9 7950X', 'price': 699, 'category': 'Processor'},
    'ryzen77800x3d': {'name': 'AMD Ryzen 7 7800X3D', 'price': 449, 'category': 'Processor'},

    # RAM
    'ddr532gb': {'name': 'Corsair Vengeance 32GB DDR5', 'price': 189, 'category': 'RAM'},
    'ddr416gb': {'name': 'Corsair Vengeance 16GB DDR4', 'price': 89, 'category': 'RAM'},

    # Storage
    'samsung980pro1tb': {'name': 'Samsung 980 Pro 1TB NVMe', 'price': 89, 'category': 'Storage'},
    'wdblack2tb': {'name': 'WD Black 2TB SN850X', 'price': 159, 'category': 'Storage'},

    # Other
    'airpodspro': {'name': 'AirPods Pro 2', 'price': 249, 'category': 'Accessories'},
    'applewatch': {'name': 'Apple Watch Series 9', 'price': 399, 'category': 'Smartwatch'},
    'ipadpro': {'name': 'iPad Pro 12.9"', 'price': 1099, 'category': 'Tablet'},
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Hi {user.first_name}! 📈📱\n\n"
        f"I can help you with TWO things:\n\n"
        f"📊 *STOCKS:*\n"
        f"/price AAPL - Get stock price\n"
        f"/predict AAPL - Get 7-day prediction with chart\n\n"
        f"📱 *ELECTRONIC DEVICES:*\n"
        f"/device rtx4090 - Get device price\n"
        f"/device iphone15pro - Get iPhone price\n"
        f"/devices - Show all available devices\n\n"
        f"Try these now:\n"
        f"/price AAPL\n"
        f"/device rtx4090",
        parse_mode='Markdown'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 *Stock Predictor Bot - Help*\n\n"
        "*📊 STOCK COMMANDS:*\n"
        "/price SYMBOL - Get current stock price\n"
        "/predict SYMBOL - Get 7-day prediction with chart\n\n"
        "*📱 DEVICE COMMANDS:*\n"
        "/device NAME - Get electronic device price\n"
        "/devices - Show all available devices\n"
        "/categories - Show devices by category\n\n"
        "*Examples:*\n"
        "/price AAPL\n"
        "/predict TSLA\n"
        "/device rtx_4090\n"
        "/device iphone_15_pro\n\n"
        "*Popular Stocks:* AAPL, TSLA, MSFT, NVDA, GOOGL\n"
        "*Popular Devices:* rtx_4090, iphone_15_pro, ps5, macbook_pro_14",
        parse_mode='Markdown'
    )


async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get stock price"""
    if not context.args:
        await update.message.reply_text("Please provide a symbol. Example: /price AAPL")
        return

    symbol = context.args[0].upper()
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        name = info.get('longName', symbol)
        hist = stock.history(period='1d')

        if not hist.empty:
            price = hist['Close'].iloc[-1]
            await update.message.reply_text(
                f"📊 *{name}* ({symbol})\n\n"
                f"💰 Price: *${price:.2f}*\n\n"
                f"Data from Yahoo Finance",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(f"❌ Could not find stock: {symbol}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {symbol} not found")


async def device_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get electronic device price"""
    if not context.args:
        # Show quick help
        devices_list = "\n".join(
            [f"• {d}" for d in list(ELECTRONIC_DEVICES.keys())[:10]])
        await update.message.reply_text(
            f"📱 *Available Devices:*\n{devices_list}\n\n"
            f"Use /devices to see all\n"
            f"Example: /device rtx_4090",
            parse_mode='Markdown'
        )
        return

    device_name = context.args[0].lower()

    if device_name in ELECTRONIC_DEVICES:
        device = ELECTRONIC_DEVICES[device_name]
        await update.message.reply_text(
            f"📱 *{device['name']}*\n\n"
            f"💰 Price: *${device['price']}*\n"
            f"📂 Category: *{device['category']}*\n\n"
            f"Find it at: Amazon, Best Buy, etc.",
            parse_mode='Markdown'
        )
    else:
        # Suggest similar devices
        suggestions = [d for d in ELECTRONIC_DEVICES.keys()
                       if device_name in d]
        if suggestions:
            await update.message.reply_text(
                f"❌ Device '{device_name}' not found.\n\n"
                f"Did you mean:\n" +
                "\n".join([f"• /device {s}" for s in suggestions[:5]])
            )
        else:
            await update.message.reply_text(
                f"❌ Device '{device_name}' not found.\n\n"
                f"Use /devices to see all available devices."
            )


async def devices_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all available electronic devices"""
    message = "📱 *ALL ELECTRONIC DEVICES*\n\n"

    # Group by category
    categories = {}
    for key, device in ELECTRONIC_DEVICES.items():
        cat = device['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((key, device['name'], device['price']))

    for category, devices in categories.items():
        message += f"*{category}:*\n"
        for key, name, price in devices:
            message += f"• {name} - ${price}\n"
        message += "\n"

    message += "Use: /device NAME\nExample: /device rtx_4090"

    await update.message.reply_text(message, parse_mode='Markdown')


async def categories_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show devices by category"""
    message = "📂 *DEVICE CATEGORIES*\n\n"

    categories = set(device['category']
                     for device in ELECTRONIC_DEVICES.values())
    for cat in sorted(categories):
        message += f"• {cat}\n"

    message += "\nUse /devices to see all devices in each category"
    await update.message.reply_text(message, parse_mode='Markdown')


def predict_stock_price(symbol, days=7):
    """Predict stock price for next days"""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period='3mo')

        if hist.empty:
            return None, None, None, None

        hist = hist[['Close']].reset_index()
        hist['Days'] = (hist['Date'] - hist['Date'].min()).dt.days

        X = hist[['Days']].values
        y = hist['Close'].values

        model = LinearRegression()
        model.fit(X, y)

        current_price = y[-1]

        last_day = hist['Days'].iloc[-1]
        future_days = np.array(
            [last_day + i for i in range(1, days + 1)]).reshape(-1, 1)
        predictions = model.predict(future_days)

        predicted_price = predictions[-1]
        change_percent = (
            (predicted_price - current_price) / current_price) * 100

        # Create chart
        plt.figure(figsize=(10, 6))
        plt.plot(hist['Date'], hist['Close'], 'b-',
                 label='Historical', linewidth=2)

        last_date = hist['Date'].iloc[-1]
        future_dates = pd.date_range(
            start=last_date, periods=days + 1, freq='D')[1:]

        plt.plot(future_dates, predictions, 'r--',
                 label='Predicted', linewidth=2, marker='o')
        plt.scatter(last_date, current_price, color='green',
                    s=100, label='Current', zorder=5)

        plt.title(
            f'{symbol} Stock Price Prediction - Next {days} Days', fontsize=14)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price (USD)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        chart_path = f'charts/{symbol}_prediction.png'
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()

        return current_price, predicted_price, change_percent, chart_path

    except Exception as e:
        print(f"Prediction error: {e}")
        return None, None, None, None


async def predict_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /predict command"""
    if not context.args:
        await update.message.reply_text("Please provide a symbol. Example: /predict AAPL")
        return

    symbol = context.args[0].upper()

    await update.message.reply_text(f"🔮 Analyzing {symbol} and generating prediction... (about 5 seconds)")
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='upload_photo')

    try:
        result = predict_stock_price(symbol)

        if result[0] is None:
            await update.message.reply_text(f"❌ Could not generate prediction for {symbol}")
            return

        current_price, predicted_price, change_percent, chart_path = result

        message = f"""
🔮 *Prediction for {symbol}*

📊 Current Price: *${current_price:.2f}*
🎯 Predicted Price (7 days): *${predicted_price:.2f}*
📈 Expected Change: *{change_percent:+.2f}%*

📅 Based on 3 months of historical data

*Note:* Predictions are for educational purposes only.
        """
        await update.message.reply_text(message, parse_mode='Markdown')

        with open(chart_path, 'rb') as photo:
            await update.message.reply_photo(photo, caption=f"📈 {symbol} Price Prediction Chart")

    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("❌ Error generating prediction. Please try again.")


def main():
    app = Application.builder().token(TOKEN).build()

    # Stock commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("price", price_command))
    app.add_handler(CommandHandler("predict", predict_command))

    # Device commands
    app.add_handler(CommandHandler("device", device_command))
    app.add_handler(CommandHandler("devices", devices_command))
    app.add_handler(CommandHandler("categories", categories_command))

    print("=" * 50)
    print("🤖 Stock Predictor Bot with ELECTRONIC DEVICES is RUNNING!")
    print("=" * 50)
    print("\nTry these commands in Telegram:")
    print("  📊 STOCKS:")
    print("  /price AAPL")
    print("  /predict AAPL")
    print("\n  📱 DEVICES:")
    print("  /device rtx_4090")
    print("  /device iphone_15_pro")
    print("  /devices")
    print("  /categories")
    print("\nPress Ctrl+C to stop\n")

    app.run_polling()


if __name__ == '__main__':
    main()
