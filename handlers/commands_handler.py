from config import logger
from telegram import Update
from telegram.ext import ContextTypes
from database.models import create_user, get_user, update_score, update_last_login
from datetime import datetime

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /start command, welcoming the user and creating a new entry in the database if needed.
    
    Args:
        update (Update): The Telegram update containing user information.
        context (ContextTypes.DEFAULT_TYPE): The callback context from telegram.ext.
    """
    user = update.effective_user
    if not get_user(user.id):
        create_user(user.id)
    
    await update.message.reply_text(f"Hello {user.first_name}, welcome to the Retrodrop Bot!")
    logger.info(f"User {user.id} started the bot.")

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /login command. The user earns 5 points for logging in once per day.
    
    Args:
        update (Update): The Telegram update containing user information.
        context (ContextTypes.DEFAULT_TYPE): The callback context from telegram.ext.
    """
    user = update.effective_user
    user_data = get_user(user.id)
    
    if user_data:
        last_login = user_data['last_login']
        today = datetime.now().date()

        if last_login != today:
            update_score(user.id, 5)
            update_last_login(user.id, today)
            await update.message.reply_text("You have successfully logged in and earned 5 points!")
            logger.info(f"User {user.id} logged in and earned 5 points.")
        else:
            await update.message.reply_text("You have already logged in today.")
            logger.info(f"User {user.id} attempted to log in again today.")
    else:
        await update.message.reply_text("Please start the bot with /start.")

async def score(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /score command, showing the user's current score.
    
    Args:
        update (Update): The Telegram update containing user information.
        context (ContextTypes.DEFAULT_TYPE): The callback context from telegram.ext.
    """
    user = update.effective_user
    user_data = get_user(user.id)
    
    if user_data:
        await update.message.reply_text(f"Your current score is: {user_data['score']}")
        logger.info(f"User {user.id} checked their score.")
    else:
        await update.message.reply_text("Please start the bot with /start.")
