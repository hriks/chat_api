 import os
 
 try:
     CHAT_DATABASE_URI = os.environ['CHAT_DATABASE_URI']
 except Exception as e:
     raise e
