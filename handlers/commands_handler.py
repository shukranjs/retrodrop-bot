from datetime import datetime
from os import getenv

from telegram import Update
from telegram.ext import ContextTypes

from config.logger import logger
from database.models import (create_user, get_user, update_last_login,
                             update_score)
from utils.helpers import get_user_id_from_channel

CHAT_ID = getenv("CHAT_ID")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /start command, welcoming the user and creating a new entry in the database if needed.
    """
    user_id = await get_user_id_from_channel(update, context, CHAT_ID)
    if not await get_user(user_id):
        await create_user(user_id)
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=f"Hello {update.effective_message.from_user.first_name}, welcome to the Retrodrop Bot!",
    )
    logger.info(f"User {user_id} started the bot.")


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /login command. The user earns 5 points for logging in once per day.
    """
    user_id = await get_user_id_from_channel(update, context, CHAT_ID)
    user_data = await get_user(user_id)

    if user_data:
        last_login = user_data["last_login"]
        today = datetime.now().date()

        if last_login != today:
            await update_score(user_id, 5)
            await update_last_login(user_id, today)
            await context.bot.send_message(
                chat_id=CHAT_ID,
                text="You have successfully logged in and earned 5 points!",
            )
            logger.info(f"User {user_id} logged in and earned 5 points.")
        else:
            await context.bot.send_message(
                chat_id=CHAT_ID,
                text="You have already logged in today.",
            )
            logger.info(f"User {user_id} attempted to log in again today.")
    else:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="Please start the bot with /start.",
        )


async def score(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /score command, showing the user's current score.
    """
    user_id = await get_user_id_from_channel(update, context, CHAT_ID)
    user_data = await get_user(user_id)  # Ensure this is awaited if async

    if user_data:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=f"Your current score is: {user_data['score']}",
        )
        logger.info(f"User {user_id} checked their score.")
    else:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="Please start the bot with /start.",
        )
