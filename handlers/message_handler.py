from config.logger import logger
from telegram import Update
from telegram.ext import ContextTypes
from database.models import get_user, update_score

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles incoming messages. Users can earn or lose points based on message content.
    
    Args:
        update (Update): The Telegram update containing message content.
        context (ContextTypes.DEFAULT_TYPE): The callback context from telegram.ext.
    """
    user = update.effective_user
    message = update.message.text.lower()
    user_data = get_user(user.id)

    if user_data:
        if message in ("gm", "gn", "spam"):
            # Penalize for spammy messages
            update_score(user.id, -1)
            await update.message.reply_text("Please avoid spammy messages. You've been penalized 1 point.")
            logger.info(f"User {user.id} penalized for sending spam message.")
        elif len(message) > 10:
            # Reward for meaningful messages
            update_score(user.id, 1)
            await update.message.reply_text("Great message! You've earned 1 point.")
            logger.info(f"User {user.id} rewarded for sending a meaningful message.")
