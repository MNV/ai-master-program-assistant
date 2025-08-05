import os
from dotenv import load_dotenv
import logging

from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from handlers.start import start, PROGRAM
from handlers.program import choose_program, BACKGROUND
from handlers.background import collect_background, QUERY
from handlers.query import answer_query, RECOMMEND
from handlers.recommendations import recommend_electives
from handlers.common import cancel
from handlers.help import help_command
from handlers.courses import courses_command
from handlers.info import info_command


def main():
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set in the environment")

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    app = Application.builder().token(token).build()

    # Простые команды вне Conversation
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("courses", courses_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CommandHandler("cancel", cancel))

    # ConversationHandler для диалога:
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PROGRAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_program)],
            BACKGROUND: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_background)],
            QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_query)],
            RECOMMEND: [MessageHandler(filters.Regex(r"(?i)рекоменд"), recommend_electives)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)

    app.run_polling()


if __name__ == "__main__":
    main()
