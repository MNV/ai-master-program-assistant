from telegram import Update
from telegram.ext import ContextTypes

PROGRAM = 0  # переход в состояние выбора программы


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = (
        "👋 Привет! Я помогу тебе разобраться в магистерских программах.\n\n"
        "Выбери, пожалуйста, программу:\n"
        "1️⃣ AI\n"
        "2️⃣ AI Product\n\n"
        "Отправь «1» или «2»."
    )
    await update.message.reply_text(text)
    return PROGRAM
