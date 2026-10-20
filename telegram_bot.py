import json
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest
from app_control import handle_in_app_actions

CONFIG_FILE = "settings.json"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def load_or_request_token():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                token = data.get("bot_token")
                if token:
                    return token
        except Exception:
            pass

    print("=" * 60)
    print("🤖 NIKO BIZNES YORDAMCHISI — TELEGRAM SOZLAMALARI")
    print("=" * 60)
    token = input("Iltimos, Telegram Bot Tokeningizni kiriting: ").strip()

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"bot_token": token}, f, ensure_ascii=False, indent=4)

    print("✅ Token saqlandi! Bot ulanmoqda...\n")
    return token

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
    bot_token = load_or_request_token()
    print("🤖 NIKO Telegram boti ulanishga harakat qilmoqda...")
    
    # Timeout vaqtini 30 sekundga cho'zamiz
    custom_request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
    
    app = ApplicationBuilder().token(bot_token).request(custom_request).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 Bot muvaffaqiyatli ishga tushdi!")
    app.run_polling()
