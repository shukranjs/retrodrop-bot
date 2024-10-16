from os import getenv

from telegram import Update
from telegram.ext import ContextTypes

from config.logger import logger
from database.models import get_user, update_score
from utils.helpers import get_user_id_from_channel

CHAT_ID = getenv("CHAT_ID")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles incoming messages and channel posts. Users can earn or lose points based on message content.

    Args:
        update (Update): The Telegram update containing message or channel post content.
        context (ContextTypes.DEFAULT_TYPE): The callback context from telegram.ext.
    """
    # Get the message
    user_id =  await get_user_id_from_channel(update, context, CHAT_ID)

    # Get the message text
    post_text = (
        update.effective_message.text.lower() if update.effective_message.text else ""
    )

    user = get_user(user_id)
    if user:
        if post_text in ("gm", "gn", "spam"):
            update_score(user["user_id"], -1)
            await context.bot.send_message(
                chat_id=CHAT_ID,
                text="Please avoid spammy messages. You've been penalized 1 point.",
            )

        elif len(post_text) > 10:
            logger.info(f"Message is longer than 10 characters: {post_text}")
            update_score(user["user_id"], 1)
            await context.bot.send_message(
                chat_id=CHAT_ID, text="Great message! You've earned 1 point."
            )
            logger.info(f"User {user['user_id']} rewarded for meaningful message.")
