import json
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest
from app_control import handle_in_app_actions

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! Xush kelibsiz. Qanday mahsulot yoki savolingiz bor, bemalol so'rashingiz mumkin.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text:
        return

    handled, response = handle_in_app_actions(user_text)

    if handled and response:
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("Kechirasiz, tushunmadim. Qaysi mahsulot haqida ma'lumot kerak edi?")

if __name__ == '__main__':
    # Render muhitidan tokenni olish
    bot_token = os.environ.get("TELEGRAM_TOKEN")
    
    if not bot_token:
        print("Xatolik: TELEGRAM_TOKEN topilmadi!")
        exit(1)

    print("🤖 NIKO Telegram boti ulanishga harakat qilmoqda...")
    
    custom_request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
    
    app = ApplicationBuilder().token(bot_token).request(custom_request).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 Bot muvaffaqiyatli ishga tushdi!")
    app.run_polling(drop_pending_updates=True)