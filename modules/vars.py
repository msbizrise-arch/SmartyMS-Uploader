#VIP BROTHERS
# Add your details here and then deploy by clicking on HEROKU Deploy button
import os
from os import environ

API_ID = int(environ.get("API_ID", "22480303"))
API_HASH = environ.get("API_HASH", "61e5cc94bc5e6318643707054e54caf4")
BOT_TOKEN = environ.get("BOT_TOKEN", "")
OWNER = int(environ.get("OWNER", "8500852075"))
CREDIT = "VIP BROTHERS"
AUTH_USER = os.environ.get('AUTH_USERS', '8500852075').split(',')
AUTH_USERS = [int(user_id) for user_id in AUTH_USER]
if int(OWNER) not in AUTH_USERS:
    AUTH_USERS.append(int(OWNER))
  
#WEBHOOK = True  # Don't change this
#PORT = int(os.environ.get("PORT", 8080))  # Default to 8000 if not set
