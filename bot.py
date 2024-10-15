import logging
from typing import Optional, Dict, Any
import mysql.connector
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from datetime import datetime

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Database connection
db_conn = mysql.connector.connect(
    host="localhost",
    user="retrodrop",
    password="12345",
    database="retrodropsystem"
)

def create_table_if_not_exists() -> None:
    """
    Creates the 'users' table if it doesn't already exist in the database.
    """
    try:
        cursor = db_conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            score INT DEFAULT 0,
            last_login DATE,
            message_count INT DEFAULT 0
        )
        """)
        db_conn.commit()
        logger.info("Users table checked/created successfully.")
    except mysql.connector.Error as err:
        logger.error(f"Error creating table: {err}")

create_table_if_not_exists()

def create_user(user_id: int) -> None:
    """
    Inserts a new user into the 'users' table with default values.
    
    Args:
        user_id (int): The Telegram user ID of the new user.
    """
    try:
        cursor = db_conn.cursor()
        cursor.execute("INSERT INTO users (user_id, score, last_login, message_count) VALUES (%s, %s, %s, %s)", 
                       (user_id, 0, None, 0))
        db_conn.commit()
        logger.info(f"New user created with ID: {user_id}")
    except mysql.connector.Error as err:
        logger.error(f"Error inserting new user: {err}")

def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieves user data from the database based on their Telegram user ID.
    
    Args:
        user_id (int): The Telegram user ID.
    
    Returns:
        Optional[Dict[str, Any]]: A dictionary containing user data, or None if the user doesn't exist.
    """
    try:
        cursor = db_conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()
        logger.info(f"Fetched user data for ID: {user_id}")
        return user_data
    except mysql.connector.Error as err:
        logger.error(f"Error fetching user: {err}")
        return None

def update_score(user_id: int, points: int) -> None:
    """
    Updates the score of a user in the database.
    
    Args:
        user_id (int): The Telegram user ID.
        points (int): The points to add or subtract from the user's score.
    """
    try:
        cursor = db_conn.cursor()
        cursor.execute("UPDATE users SET score = score + %s WHERE user_id = %s", (points, user_id))
        db_conn.commit()
        logger.info(f"Updated score for user {user_id}: {points} points")
    except mysql.connector.Error as err:
        logger.error(f"Error updating score: {err}")

async def start(update: Update, context) -> None:
    """
    Handles the /start command, welcoming the user and creating a new entry in the database if needed.
    
    Args:
        update (Update): The Telegram update containing user information.
        context: The callback context.
    """
    user = update.effective_user
    if not get_user(user.id):
        create_user(user.id)
    
    await update.message.reply_text(f"Hello {user.first_name}, welcome to the Retrodrop Bot!")
    logger.info(f"User {user.id} started the bot.")

async def score(update: Update, context) -> None:
    """
    Handles the /score command, showing the user's current score.
    
    Args:
        update (Update): The Telegram update containing user information.
        context: The callback context.
    """
    user = update.effective_user
    user_data = get_user(user.id)
    if user_data:
        await update.message.reply_text(f"Your current score is: {user_data['score']}")
        logger.info(f"User {user.id} checked their score.")
    else:
        await update.message.reply_text("Please start the bot with /start.")

async def login(update: Update, context) -> None:
    """
    Handles the /login command. The user earns 5 points for logging in once per day.
    
    Args:
        update (Update): The Telegram update containing user information.
        context: The callback context.
    """
    user = update.effective_user
    user_data = get_user(user.id)
    if user_data:
        last_login = user_data['last_login']
        today = datetime.now().date()
        if last_login != today:
            update_score(user.id, 5)
            cursor = db_conn.cursor()
            cursor.execute("UPDATE users SET last_login = %s WHERE user_id = %s", (today, user.id))
            db_conn.commit()
            await update.message.reply_text("You have successfully logged in and earned 5 points!")
            logger.info(f"User {user.id} logged in and earned 5 points.")
        else:
            await update.message.reply_text("You have already logged in today.")
            logger.info(f"User {user.id} attempted to log in again today.")
    else:
        await update.message.reply_text("Please start the bot with /start.")

async def handle_message(update: Update, context) -> None:
    """
    Handles incoming messages. Users can earn or lose points based on message content.
    
    Args:
        update (Update): The Telegram update containing message content.
        context: The callback context.
    """
    user = update.effective_user
    message = update.message.text.lower()
    user_data = get_user(user.id)
    if user_data:
        if message in ("gm", "gn", "spam"):
            update_score(user.id, -1)
            await update.message.reply_text("Please avoid spammy messages. You've been penalized 1 point.")
            logger.info(f"User {user.id} penalized for sending spam message.")
        elif len(message) > 10:
            update_score(user.id, 1)
            await update.message.reply_text("Great message! You've earned 1 point.")
            logger.info(f"User {user.id} rewarded for sending a valuable message.")

async def leaderboard(update: Update, context) -> None:
    """
    Handles the /leaderboard command, showing the top 5 users by score.
    
    Args:
        update (Update): The Telegram update containing user information.
        context: The callback context.
    """
    cursor = db_conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users ORDER BY score DESC LIMIT 5")
    top_users = cursor.fetchall()
    
    leaderboard_text = "Leaderboard:\n"
    for user in top_users:
        leaderboard_text += f"User {user['user_id']} - {user['score']} points\n"
    
    await update.message.reply_text(leaderboard_text)
    logger.info("Displayed leaderboard to the user.")

# Telegram bot setup
bot_token = '7990831985:AAHT_HT5BLPOC8isJFAooPpAvdeygR10rQM'
app = ApplicationBuilder().token(bot_token).build()

# Command and message handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("score", score))
app.add_handler(CommandHandler("login", login))
app.add_handler(CommandHandler("leaderboard", leaderboard))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Start polling
if __name__ == '__main__':
    logger.info("Bot is starting.")
    app.run_polling()
