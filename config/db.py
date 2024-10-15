from os import getenv


DB_CONFIG = {
    'host': getenv('MYSQL_HOST'),
    'user': getenv('MYSQL_USER'),
    'password': getenv('MYSQL_PASSWORD'),
    'database': getenv("MYSQL_DATABASE")
}


BOT_TOKEN = getenv('BOT_TOKEN')

