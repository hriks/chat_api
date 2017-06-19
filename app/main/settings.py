import os

try:
    SECRET_KEY = os.environ["SECRET_KEY"]
    # Get the secret key from the environment variable
except Exception as e:
    raise e
