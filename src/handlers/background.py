from telegram import Update
from telegram.ext import ContextTypes

QUERY = 2  # переход к общим вопросам по плану


async def collect_background(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    parts = text.split()
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        await update.message.reply_text(
            "Пожалуйста, введи три числа через пробел, например: «4 3 2»."
        )
        return QUERY - 1

    math, prog, ml = map(int, parts)
    context.user_data["background"] = {"math": math, "prog": prog, "ml": ml}

    await update.message.reply_text(
        "Отлично! Теперь можешь задавать вопросы по учебному плану "
        "или попросить рекомендации по элективам."
    )
    return QUERY
