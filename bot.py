import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

allowed_words = ["wts", "wtb", "#wts", "#wtb"]

REMINDER_TEXT = """Для безопасной сделки используйте гаранта @delta_otc.


For a secure deal, use escrow @delta_otc.

@SHVEDOFFRECORD @nekitdelta
"""

chat_id = None


async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_id
    
    message = update.message
    
    if not message:
        return

    chat_id = message.chat_id

    if not message.text:
        return

    text = message.text.lower()

    if not any(word in text for word in allowed_words):
        try:
            await message.delete()
        except:
            pass


async def reminder_loop(app):
    global chat_id
    
    while True:
        if chat_id:
            try:
                await app.bot.send_message(chat_id=chat_id, text=REMINDER_TEXT)
            except:
                pass
        
        await asyncio.sleep(3600)  # 1 година


async def on_startup(app):
    asyncio.create_task(reminder_loop(app))


app = ApplicationBuilder().token(TOKEN).post_init(on_startup).build()

app.add_handler(MessageHandler(filters.TEXT, filter_messages))

print("Bot started")

app.run_polling()
