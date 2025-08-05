from telegram import Update
from telegram.ext import ContextTypes
from parsers.html_parser import get_program_info


def program_url_from_choice(choice: str) -> str:
    URLS = {
        "1": "https://abit.itmo.ru/program/master/ai",
        "2": "https://abit.itmo.ru/program/master/ai_product",
    }
    return URLS.get(choice)


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    choice = context.user_data.get("program_choice")
    if not choice:
        await update.message.reply_text(
            "Сначала выбери программу командой /start."
        )
        return
    url = program_url_from_choice(choice)
    info = get_program_info(url)
    text = f"<b>{info.get('title')}</b>\n\n{info.get('description')}"
    await update.message.reply_text(text, parse_mode="HTML")
