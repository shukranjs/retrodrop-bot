from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from config.db import BOT_TOKEN
from config.logger import setup_logger
from database.models import create_table_if_not_exists
from handlers.commands_handler import login, score, start
from handlers.leaderboard_handler import leaderboard
from handlers.message_handler import handle_message


if __name__ == "__main__":
    create_table_if_not_exists()
    setup_logger()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register handlers

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("score", score))
    app.add_handler(CommandHandler("leaderboard", leaderboard))

    # Start polling
    app.run_polling()
