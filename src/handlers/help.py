from telegram import Update
from telegram.ext import ContextTypes


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Я могу помочь с информацией по магистерским программам ИТМО.\n"
        "Доступные команды:\n"
        "/start — начать диалог и выбрать программу\n"
        "/help — справка по командам\n"
        "/courses — список всех курсов выбранной программы\n"
        "/info — описание выбранной программы\n"
        "/cancel — прервать текущий диалог\n"
        "Также задавайте вопросы по названиям курсов или вводите ‘Рекомендации’."
    )
    await update.message.reply_text(text)
