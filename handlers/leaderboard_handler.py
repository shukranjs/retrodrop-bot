from os import getenv

from telegram import Update
from telegram.ext import ContextTypes

from config.logger import logger
from database.models import get_top_users
from utils.helpers import get_user_id_from_channel

CHAT_ID = getenv("CHAT_ID")


async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /leaderboard command, showing the top 5 users by score.

    Args:
        update (Update): The Telegram update containing user information.
        context (ContextTypes.DEFAULT_TYPE): The callback context from telegram.ext.
    """
    user = update.effective_user
    if user is None:
        logger.info("No user information available in this update.")
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="Unable to identify you. Please start the bot with /start.",
        )
        return

    user_id = await get_user_id_from_channel(update, context, CHAT_ID)

    top_users = get_top_users(limit=5)
    print("top_users", top_users)
    logger.info(f"toppp {top_users}")
    if top_users:
        leaderboard_text = "🏆 *Leaderboard:*\n\n"
        for idx, top_user in enumerate(top_users, start=1):
            leaderboard_text += (
                f"{idx}. User {top_user['user_id']} - {top_user['score']} points\n"
            )

        await context.bot.send_message(
            chat_id=CHAT_ID, text=leaderboard_text, parse_mode="Markdown"
        )
        logger.info(f"Displayed leaderboard to user {user_id}.")
    else:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="There was an error fetching the leaderboard.",
        )
        logger.error(f"Error fetching leaderboard data for user {user_id}.")
