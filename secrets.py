import os

if os.path.exists('tokens.py'):

    from tokens import *

    os.environ['BOT_TOKEN'] = BOT_TOKEN
    os.environ['SUDO_USERS'] = SUDO_USERS
    os.environ['LOG_ID'] = LOG_ID
    os.environ['IMGFLIP_URL'] = IMGFLIP_URL
    os.environ['IMGFLIP_USERNAME'] = IMGFLIP_USERNAME
    os.environ['IMGFLIP_PASSWORD'] = IMGFLIP_PASSWORD

IMGFLIP_URL = os.environ.get('IMGFLIP_URL')
BOT_TOKEN = os.environ.get("BOT_TOKEN")
SUDO_USERS = int(os.environ.get("SUDO_USERS"))
LOG_CHAT = os.environ.get("LOG_ID")
IMGFLIP_USERNAME = os.environ.get("IMGFLIP_USERNAME")
IMGFLIP_PASSWORD = os.environ.get("IMGFLIP_PASSWORD")
