from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    port=os.getenv("DB_PORT")
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! بزن بریم قیمت رمزارزها رو ببینیم.")

async def prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = """
        SELECT symbol, current_price 
        FROM crypto_prices 
        ORDER BY market_cap DESC 
        LIMIT 5
    """
    df = pd.read_sql(query, conn)
    msg = "\n".join([f"{row.symbol.upper()}: ${row.current_price}" for _, row in df.iterrows()])
    await update.message.reply_text(msg)

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("prices", prices))
app.run_polling()