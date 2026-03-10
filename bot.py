from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

allowed_words = ["wts", "wtb", "#wts", "#wtb"]

async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    
    if not message:
        return
        
    if not message.text:
        return

    text = message.text.lower()

    if not any(word in text for word in allowed_words):
        try:
            await message.delete()
        except:
            pass

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, filter_messages))

print("Bot started")


app.run_polling()
