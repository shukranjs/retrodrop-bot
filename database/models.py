from typing import Optional, Dict, Any
from datetime import datetime

from config.logger import logger
from .connection import get_db_connection

def create_table_if_not_exists() -> None:
    """
    Creates the 'users' table if it doesn't already exist in the database.
    """
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    try:
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
    except Exception as e:
        logger.error(f"Error creating table: {e}")
    finally:
        cursor.close()
        db_conn.close()

def create_user(user_id: int) -> None:
    """
    Inserts a new user into the 'users' table with default values.
    
    Args:
        user_id (int): The Telegram user ID of the new user.
    """
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    try:
        cursor.execute("INSERT INTO users (user_id, score, last_login, message_count) VALUES (%s, %s, %s, %s)", 
                       (user_id, 0, None, 0))
        db_conn.commit()
        logger.info(f"New user created with ID: {user_id}")
    except Exception as e:
        logger.error(f"Error inserting new user: {e}")
    finally:
        cursor.close()
        db_conn.close()

def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieves user data from the database based on their Telegram user ID.
    
    Args:
        user_id (int): The Telegram user ID.
    
    Returns:
        Optional[Dict[str, Any]]: A dictionary containing user data, or None if the user doesn't exist.
    """
    db_conn = get_db_connection()
    cursor = db_conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()
        logger.info(f"Fetched user data for ID: {user_id}")
        return user_data
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        return None
    finally:
        cursor.close()
        db_conn.close()

def update_score(user_id: int, points: int) -> None:
    """
    Updates the score of a user in the database.
    
    Args:
        user_id (int): The Telegram user ID.
        points (int): The points to add or subtract from the user's score.
    """
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    try:
        cursor.execute("UPDATE users SET score = score + %s WHERE user_id = %s", (points, user_id))
        db_conn.commit()
        logger.info(f"Updated score for user {user_id}: {points} points")
    except Exception as e:
        logger.error(f"Error updating score: {e}")
    finally:
        cursor.close()
        db_conn.close()

def update_last_login(user_id: int, last_login_date: datetime) -> None:
    """
    Updates the last login date of the user.
    
    Args:
        user_id (int): The Telegram user ID.
        last_login_date (datetime): The new login date to be updated.
    """
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    try:
        cursor.execute("UPDATE users SET last_login = %s WHERE user_id = %s", (last_login_date, user_id))
        db_conn.commit()
        logger.info(f"Updated last login for user {user_id}")
    except Exception as e:
        logger.error(f"Error updating last login: {e}")
    finally:
        cursor.close()
        db_conn.close()

def get_top_users(limit: int = 5) -> Optional[list]:
    """
    Retrieves the top users based on their score.
    
    Args:
        limit (int): The maximum number of top users to retrieve.
    
    Returns:
        Optional[list]: A list of top users, or None if there's an error.
    """
    db_conn = get_db_connection()
    cursor = db_conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users ORDER BY score DESC LIMIT %s", (limit,))
        top_users = cursor.fetchall()
        logger.info(f"Fetched top {limit} users by score.")
        return top_users
    except Exception as e:
        logger.error(f"Error fetching top users: {e}")
        return None
    finally:
        cursor.close()
        db_conn.close()
