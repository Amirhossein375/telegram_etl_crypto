from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv()

# پیام خوش‌آمد
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 🤖\n\n"
        "من ربات قیمت لحظه‌ای رمزارزها هستم.\n"
        "برای دیدن قیمت ۵ رمزارز اول بازار بنویس:\n"
        "`/prices`\n\n"
        "🧠 قیمت‌ها از CoinGecko API دریافت می‌شن."
    )

# گرفتن قیمت لحظه‌ای
async def prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 5,
        "page": 1
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        msg = "\n".join([
            f"{coin['symbol'].upper()}: ${coin['current_price']:,}"
            for coin in data
        ])
        await update.message.reply_text("💰 قیمت ۵ رمزارز برتر:\n\n" + msg)

    except Exception as e:
        await update.message.reply_text("❌ خطا در دریافت اطلاعات از API.")
        print("خطا:", e)

# راه‌اندازی بات
app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("prices", prices))

app.run_polling()
