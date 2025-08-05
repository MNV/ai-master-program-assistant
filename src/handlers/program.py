import logging
from telegram import Update
from telegram.ext import ContextTypes
from parsers.downloader import download_plan
from parsers.pdf_parser import parse_study_plan

logger = logging.getLogger(__name__)  # ← получаем логгер для этого модуля

BACKGROUND = 1

URLS = {
    "1": "https://abit.itmo.ru/program/master/ai",
    "2": "https://abit.itmo.ru/program/master/ai_product",
}


async def choose_program(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text.strip()
    if choice not in URLS:
        await update.message.reply_text("Пожалуйста, отправь «1» или «2».")
        return BACKGROUND - 1

    # Скачиваем и парсим учебный план
    url = URLS[choice]
    pdf_path = download_plan(url, output_dir="data/raw")
    courses = parse_study_plan(pdf_path)

    # ---- ДЕБАГ: выводим полностью распарсенные курсы ----
    logger.debug("=== Parsed courses for program %s: ===", choice)
    for c in courses:
        logger.debug("Parsed course name:  %s", c)
    # -----------------------------------------------------

    context.user_data["courses"] = courses
    context.user_data["program_choice"] = choice

    await update.message.reply_text(
        "Отлично! Теперь расскажи немного о своём бэкграунде:\n"
        "- уровень математики (1–5)\n"
        "- уровень программирования (1–5)\n"
        "- опыт в ML (1–5)\n\n"
        "Напиши три числа через пробел, например: «4 3 2»."
    )
    return BACKGROUND
