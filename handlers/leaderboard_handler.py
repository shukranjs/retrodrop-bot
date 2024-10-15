from telegram import Update
from telegram.ext import ContextTypes

from config.logger import logger
from database.models import get_top_users


async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /leaderboard command, showing the top 5 users by score.

    Args:
        update (Update): The Telegram update containing user information.
        context (ContextTypes.DEFAULT_TYPE): The callback context from telegram.ext.
    """
    top_users = get_top_users(limit=5)

    if top_users:
        leaderboard_text = "Leaderboard:\n"
        for user in top_users:
            leaderboard_text += f"User {user['user_id']} - {user['score']} points\n"

        await update.message.reply_text(leaderboard_text)
        logger.info("Displayed leaderboard to the user.")
    else:
        await update.message.reply_text("There was an error fetching the leaderboard.")
        logger.error("Error fetching leaderboard data.")
