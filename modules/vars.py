#VIP BROTHERS
# Add your details here and then deploy by clicking on HEROKU Deploy button
import os
from os import environ

API_ID = int(environ.get("API_ID", "38498066"))
API_HASH = environ.get("API_HASH", "c9696114751feacdeb1b4487f5839a1a")
BOT_TOKEN = environ.get("BOT_TOKEN", "")
OWNER = int(environ.get("OWNER", "8703802029"))
CREDIT = "VIP BROTHERS"
AUTH_USER = os.environ.get('AUTH_USERS', '8703802029').split(',')
AUTH_USERS = [int(user_id) for user_id in AUTH_USER]
if int(OWNER) not in AUTH_USERS:
    AUTH_USERS.append(int(OWNER))
  
#WEBHOOK = True  # Don't change this
#PORT = int(os.environ.get("PORT", 8080))  # Default to 8000 if not set
