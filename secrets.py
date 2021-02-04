import os

if os.path.exists('tokens.py'):

    from tokens import *

    os.environ['BOT_TOKEN'] = BOT_TOKEN
    os.environ['LOG_ID'] = LOG_ID
    os.environ['IMGFLIP_URL'] = IMGFLIP_URL
    os.environ['IMGFLIP_USERNAME'] = IMGFLIP_USERNAME
    os.environ['IMGFLIP_PASSWORD'] = IMGFLIP_PASSWORD
    os.environ['HOMEPIC'] = HOMEPIC
    os.environ['THUMB_PIC'] = THUMB_PIC

IMGFLIP_URL = os.environ.get('IMGFLIP_URL')
BOT_TOKEN = os.environ.get("BOT_TOKEN")
SUDO_USERS = 1482759920,
LOG_CHAT = os.environ.get("LOG_ID")
IMGFLIP_USERNAME = os.environ.get("IMGFLIP_USERNAME")
IMGFLIP_PASSWORD = os.environ.get("IMGFLIP_PASSWORD")
HOMEPIC = os.environ.get("HOMEPIC")
THUMB_PIC = os.environ.get('THUMB_PIC')
