import mysql.connector
from mysql.connector import MySQLConnection
from config.db import DB_CONFIG

def get_db_connection() -> MySQLConnection:
    """
    Establish and return a connection to the MySQL database.

    Returns:
        MySQLConnection: A connection object to interact with the MySQL database.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise
