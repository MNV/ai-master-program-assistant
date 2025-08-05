from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler


async def recommend_electives(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    bg = context.user_data.get("background", {})
    courses = context.user_data.get("courses", [])

    # Фильтруем элективные курсы
    electives = [c for c in courses if c.get("type", "").lower() == "электив"]
    if not electives:
        await update.message.reply_text("Не нашёл элективных курсов для рекомендаций.")
        return ConversationHandler.END

    # Для простоты берём первые 3 электива
    recs = electives[:3]
    lines = [f"- {c['name']} (семестр {c['semester']})" for c in recs]
    text = "Рекомендованные элективы:\n" + "\n".join(lines)

    await update.message.reply_text(text)
    await update.message.reply_text("Если нужно ещё что-то — пиши! 🎓")
    return ConversationHandler.END
