import os

try:
    SECRET_KEY = os.environ["SECRET_KEY"]
    # Get the secret key from the environment variable
except Exception as e:
    raise e

# SETUP mail-server using environment variables
# export all in your running environment.
# This will automatically fetch value and provide
# to app
try:
    MAIL_SERVER = os.environ["MAILSERVER"]
    # Mail Server
    MAIL_USERNAME = os.environ["MAILUSERNAME"]
    # User Name
    MAIL_PASSWORD = os.environ["MAILPASSWORD"]
    # User Password
    MAIL_PORT = os.environ["PORT"]
    # port for SSL or TSL which ever is true
    MAIL_USE_SSL = True
    # For SSL connection
    # Need SSl Certificate
    MAIL_USE_TSL = False
    # For TSL
except Exception as e:
    raise e
    # Raises exception if any error is caused

try:
    serializer = os.environ['serial']
except Exception as e:
    raise e
