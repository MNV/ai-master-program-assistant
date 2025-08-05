from telegram import Update
from telegram.ext import ContextTypes

RECOMMEND = 3  # если вопрос переходит к рекомендациям


async def answer_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.message.text.lower()
    courses = context.user_data.get("courses", [])

    # Поиск по названию (вхождение подстроки)
    matches = [c for c in courses if query in c["name"].lower()]
    if not matches:
        await update.message.reply_text(
            "Не нашёл по запросу. Попробуй уточнить название курса."
        )
        return RECOMMEND - 1

    # Формируем ответ без полей credits/hours
    resp_lines = []
    for c in matches:
        line = f"- {c['semester']} семестр: {c['name']} ({c['type']})"
        resp_lines.append(line)
    resp = "Найденные курсы:\n" + "\n".join(resp_lines)

    await update.message.reply_text(resp)
    # Предложить рекомендации
    await update.message.reply_text(
        "Если хочешь получить рекомендации по выборным дисциплинам, напиши 'Рекомендации'."
    )
    return RECOMMEND
