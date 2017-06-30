import os

try:
    DATABASE_URI = os.environ['CHAT_DATABASE_URI']
    # Get the Database uri from environment variable
except Exception as e:
    raise e

try:
    DB_NAME = os.environ['DB_NAME']
    # Gets Database name from environment Variable
except Exception as e:
    raise e

CHAT_DATABASE_URI = DATABASE_URI + '/' + DB_NAME
