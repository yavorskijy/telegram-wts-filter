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

IMAGE_PATH = "banner.jpg"

chats = set()
last_reminders = {}


async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if not message:
        return

    chat_id = message.chat_id
    chats.add(chat_id)

    text = (message.text or message.caption or "").lower()

    if not any(word in text for word in allowed_words):
        try:
            await message.delete()
        except:
            pass


async def reminder_loop(app):
    while True:

        for chat_id in chats:
            try:

                # видаляємо попереднє нагадування
                if chat_id in last_reminders:
                    try:
                        await app.bot.delete_message(
                            chat_id=chat_id,
                            message_id=last_reminders[chat_id]
                        )
                    except:
                        pass

                # відправляємо нове
                with open(IMAGE_PATH, "rb") as photo:
                    msg = await app.bot.send_photo(
                        chat_id=chat_id,
                        photo=photo,
                        caption=REMINDER_TEXT
                    )

                # зберігаємо ID повідомлення
                last_reminders[chat_id] = msg.message_id

            except Exception as e:
                print(e)

        await asyncio.sleep(3600)


async def on_startup(app):
    asyncio.create_task(reminder_loop(app))


app = ApplicationBuilder().token(TOKEN).post_init(on_startup).build()

app.add_handler(MessageHandler(filters.ALL, filter_messages))

print("Bot started")

app.run_polling()
