from telegram import Update
from telegram.ext import ContextTypes
from handlers.common import cancel


async def courses_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    courses = context.user_data.get("courses")
    if not courses:
        await update.message.reply_text(
            "Сначала выбери программу командой /start."
        )
        return
    # Группируем по семестрам
    semesters = {}
    for c in courses:
        semesters.setdefault(c['semester'], []).append(c)
    # Вывод
    lines = []
    for sem in sorted(semesters):
        lines.append(f"Семестр {sem}:")
        for c in semesters[sem]:
            lines.append(f"- {c['name']} ({c['type']})")
    # Telegram ограничивает длину сообщения, разбиваем на части по 4000 символов
    text = "\n".join(lines)
    for chunk in [text[i:i + 4000] for i in range(0, len(text), 4000)]:
        await update.message.reply_text(chunk)
