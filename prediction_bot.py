"""
Stock Predictor Bot - With Electronic Device Prices & GPU Comparison
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

# ============================================
# ELECTRONIC DEVICES DATABASE
# ============================================
ELECTRONIC_DEVICES = {
    # iPhones
    'iphone15': {'name': 'iPhone 15', 'price': 799, 'category': 'Smartphone'},
    'iphone15pro': {'name': 'iPhone 15 Pro', 'price': 999, 'category': 'Smartphone'},
    'iphone15promax': {'name': 'iPhone 15 Pro Max', 'price': 1199, 'category': 'Smartphone'},
    'iphone14': {'name': 'iPhone 14', 'price': 699, 'category': 'Smartphone'},
    'iphone14pro': {'name': 'iPhone 14 Pro', 'price': 899, 'category': 'Smartphone'},

    # MacBooks
    'macbookair': {'name': 'MacBook Air M2', 'price': 1099, 'category': 'Laptop'},
    'macbookpro14': {'name': 'MacBook Pro 14"', 'price': 1999, 'category': 'Laptop'},
    'macbookpro16': {'name': 'MacBook Pro 16"', 'price': 2499, 'category': 'Laptop'},

    # Graphics Cards
    'rtx4090': {'name': 'NVIDIA RTX 4090', 'price': 1599, 'category': 'Graphics Card'},
    'rtx4080': {'name': 'NVIDIA RTX 4080', 'price': 1199, 'category': 'Graphics Card'},
    'rtx4070': {'name': 'NVIDIA RTX 4070', 'price': 599, 'category': 'Graphics Card'},
    'rtx4060': {'name': 'NVIDIA RTX 4060', 'price': 299, 'category': 'Graphics Card'},
    'rx7900xtx': {'name': 'AMD RX 7900 XTX', 'price': 999, 'category': 'Graphics Card'},
    'rx7800xt': {'name': 'AMD RX 7800 XT', 'price': 499, 'category': 'Graphics Card'},

    # Gaming Consoles
    'ps5': {'name': 'PlayStation 5', 'price': 499, 'category': 'Gaming Console'},
    'xboxseriesx': {'name': 'Xbox Series X', 'price': 499, 'category': 'Gaming Console'},
    'nintendoswitch': {'name': 'Nintendo Switch OLED', 'price': 349, 'category': 'Gaming Console'},

    # Processors
    'i913900k': {'name': 'Intel Core i9-13900K', 'price': 589, 'category': 'Processor'},
    'i713700k': {'name': 'Intel Core i7-13700K', 'price': 409, 'category': 'Processor'},
    'ryzen97950x': {'name': 'AMD Ryzen 9 7950X', 'price': 699, 'category': 'Processor'},

    # Accessories
    'airpodspro': {'name': 'AirPods Pro 2', 'price': 249, 'category': 'Accessories'},
    'applewatch': {'name': 'Apple Watch Series 9', 'price': 399, 'category': 'Smartwatch'},
}

# ============================================
# GPU DATABASE FOR COMPARISON
# ============================================
GPU_DATABASE = {
    'rtx4090': {
        'name': 'NVIDIA RTX 4090',
        'price': 1599,
        'vram': 24,
        'performance_score': 100,
        'best_for': '4K Gaming, Professional Work',
        'power': 450,
        'tier': 'Ultra High-End'
    },
    'rtx4080': {
        'name': 'NVIDIA RTX 4080',
        'price': 1199,
        'vram': 16,
        'performance_score': 85,
        'best_for': '4K Gaming',
        'power': 320,
        'tier': 'High-End'
    },
    'rtx4070': {
        'name': 'NVIDIA RTX 4070',
        'price': 599,
        'vram': 12,
        'performance_score': 65,
        'best_for': '1440p Gaming',
        'power': 200,
        'tier': 'Mid-Range'
    },
    'rx7900xtx': {
        'name': 'AMD RX 7900 XTX',
        'price': 999,
        'vram': 24,
        'performance_score': 90,
        'best_for': '4K Gaming',
        'power': 355,
        'tier': 'High-End'
    },
    'rx7800xt': {
        'name': 'AMD RX 7800 XT',
        'price': 499,
        'vram': 16,
        'performance_score': 68,
        'best_for': '1440p Gaming',
        'power': 263,
        'tier': 'Mid-Range'
    },
    'rtx3060': {
        'name': 'NVIDIA RTX 3060',
        'price': 299,
        'vram': 12,
        'performance_score': 45,
        'best_for': '1080p Gaming',
        'power': 170,
        'tier': 'Entry Level'
    }
}

# ============================================
# COMMAND HANDLERS
# ============================================


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Hi {user.first_name}! 📈📱\n\n"
        f"I can help you with:\n\n"
        f"📊 *STOCKS:*\n"
        f"/price AAPL - Get stock price\n"
        f"/predict AAPL - Get 7-day prediction with chart\n\n"
        f"📱 *ELECTRONIC DEVICES:*\n"
        f"/device rtx4090 - Get device price\n"
        f"/devices - Show all devices\n\n"
        f"🆚 *GPU COMPARISON:*\n"
        f"/gpucompare rtx4090 rx7900xtx - Compare GPUs\n\n"
        f"Try these:\n"
        f"/price AAPL\n"
        f"/device rtx4090\n"
        f"/gpucompare rtx4070 rx7800xt",
        parse_mode='Markdown'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 *COMPLETE COMMAND LIST*\n\n"
        "*📊 STOCKS:*\n"
        "/price SYMBOL - Current stock price\n"
        "/predict SYMBOL - 7-day prediction with chart\n\n"
        "*📱 DEVICES:*\n"
        "/device NAME - Electronic device price\n"
        "/devices - All available devices\n\n"
        "*🆚 GPU COMPARISON:*\n"
        "/gpucompare GPU1 GPU2 - Compare two graphics cards\n\n"
        "*Examples:*\n"
        "/price AAPL\n"
        "/predict TSLA\n"
        "/device rtx4090\n"
        "/gpucompare rtx4090 rx7900xtx\n\n"
        "*Popular Stocks:* AAPL, TSLA, MSFT, NVDA, GOOGL\n"
        "*Popular Devices:* rtx4090, iphone15pro, ps5\n"
        "*Popular GPUs:* rtx4090, rtx4070, rx7900xtx, rx7800xt",
        parse_mode='Markdown'
    )

# ============================================
# STOCK COMMANDS
# ============================================


async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get stock price"""
    if not context.args:
        await update.message.reply_text("Please provide a symbol. Example: /price AAPL")
        return

    symbol = context.args[0].upper()
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period='1d')

        if not hist.empty:
            price = hist['Close'].iloc[-1]
            info = stock.info
            name = info.get('longName', symbol)

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


def predict_stock_price(symbol, days=7):
    """Predict stock price using linear regression"""
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

# ============================================
# DEVICE COMMANDS
# ============================================


async def device_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get electronic device price"""
    if not context.args:
        devices_list = "\n".join(
            [f"• {d}" for d in list(ELECTRONIC_DEVICES.keys())[:10]])
        await update.message.reply_text(
            f"📱 *Available Devices:*\n{devices_list}\n\n"
            f"Use /devices to see all\n"
            f"Example: /device rtx4090",
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

    categories = {}
    for key, device in ELECTRONIC_DEVICES.items():
        cat = device['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((device['name'], device['price']))

    for category, devices in categories.items():
        message += f"*{category}:*\n"
        for name, price in devices:
            message += f"• {name} - ${price}\n"
        message += "\n"

    message += "Use: /device NAME\nExample: /device rtx4090"

    await update.message.reply_text(message, parse_mode='Markdown')

# ============================================
# GPU COMPARE COMMAND
# ============================================


async def gpu_compare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Compare two graphics cards"""

    if len(context.args) < 2:
        await update.message.reply_text(
            "📊 *GPU Comparison Tool*\n\n"
            "Compare two graphics cards:\n"
            "/gpucompare GPU1 GPU2\n\n"
            "*Examples:*\n"
            "/gpucompare rtx4090 rx7900xtx\n"
            "/gpucompare rtx4070 rx7800xt\n\n"
            "*Available GPUs:*\n"
            "rtx4090, rtx4080, rtx4070\n"
            "rx7900xtx, rx7800xt\n"
            "rtx3060",
            parse_mode='Markdown'
        )
        return

    gpu1 = context.args[0].lower()
    gpu2 = context.args[1].lower()

    if gpu1 not in GPU_DATABASE:
        await update.message.reply_text(f"❌ GPU '{gpu1}' not found")
        return

    if gpu2 not in GPU_DATABASE:
        await update.message.reply_text(f"❌ GPU '{gpu2}' not found")
        return

    g1 = GPU_DATABASE[gpu1]
    g2 = GPU_DATABASE[gpu2]

    perf_diff = g1['performance_score'] - g2['performance_score']
    price_diff = g1['price'] - g2['price']

    if g1['performance_score'] > g2['performance_score']:
        winner = f"🏆 WINNER: {g1['name']} (+{perf_diff}% performance)"
    elif g2['performance_score'] > g1['performance_score']:
        winner = f"🏆 WINNER: {g2['name']} (+{-perf_diff}% performance)"
    else:
        winner = "🤝 TIED in performance!"

    g1_value = g1['performance_score'] / (g1['price'] / 100)
    g2_value = g2['performance_score'] / (g2['price'] / 100)

    message = f"""
🆚 *GPU COMPARISON*

*{g1['name']}* vs *{g2['name']}*

━━━━━━━━━━━━━━━━━━━━━━
📊 *SPECIFICATIONS*
━━━━━━━━━━━━━━━━━━━━━━
💰 Price: ${g1['price']} vs ${g2['price']}
🎮 VRAM: {g1['vram']}GB vs {g2['vram']}GB
⚡ Power: {g1['power']}W vs {g2['power']}W
📈 Score: {g1['performance_score']}/100 vs {g2['performance_score']}/100
🎯 Tier: {g1['tier']} vs {g2['tier']}

━━━━━━━━━━━━━━━━━━━━━━
📈 *PERFORMANCE*
━━━━━━━━━━━━━━━━━━━━━━
• Performance diff: {perf_diff:+d}%
• Price diff: ${price_diff:+d}
• Value score: {g1_value:.1f} vs {g2_value:.1f}
• {winner}

━━━━━━━━━━━━━━━━━━━━━━
💡 *RECOMMENDATION*
━━━━━━━━━━━━━━━━━━━━━━
• Best for gaming: {'✅ ' + g1['name'] if g1['performance_score'] > g2['performance_score'] else '✅ ' + g2['name']}
• Best value: {'✅ ' + g1['name'] if g1_value > g2_value else '✅ ' + g2['name']}

🎯 *{g1['best_for']}*
🎯 *{g2['best_for']}*
    """

    await update.message.reply_text(message, parse_mode='Markdown')

# ============================================
# MAIN FUNCTION
# ============================================


def main():
    app = Application.builder().token(TOKEN).build()

    # Register all command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("price", price_command))
    app.add_handler(CommandHandler("predict", predict_command))
    app.add_handler(CommandHandler("device", device_command))
    app.add_handler(CommandHandler("devices", devices_command))
    app.add_handler(CommandHandler("gpucompare", gpu_compare))

    print("=" * 60)
    print("🤖 STOCK PREDICTOR BOT")
    print("=" * 60)
    print("\n✅ Features:")
    print("  📊 Stock prices & predictions")
    print("  📱 Electronic device prices")
    print("  🆚 GPU comparison tool")
    print("\n📱 Try these commands in Telegram:")
    print("  /start")
    print("  /price AAPL")
    print("  /predict AAPL")
    print("  /device rtx4090")
    print("  /devices")
    print("  /gpucompare rtx4090 rx7900xtx")
    print("\n🚀 Bot is running... Press Ctrl+C to stop")
    print("=" * 60)

    app.run_polling()


if __name__ == '__main__':
    main()
