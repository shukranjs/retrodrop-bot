from config.logger import setup_logger
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers.commands_handler import start, login, score
from handlers.message_handler import handle_message
from handlers.leaderboard_handler import leaderboard
from config.db import BOT_TOKEN
# from dotenv import load_dotenv

# Load environment variables from .env file
if __name__ == '__main__':
    # load_dotenv()
    setup_logger()
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("score", score))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling
    app.run_polling()
