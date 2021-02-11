try:
    from config import *

except ImportError:
    pass

import os

SUDO_USERS = list(map(int, os.environ.get("SUDO_USERS").split()))
IMGFLIP_URL = os.environ.get('IMGFLIP_URL')
BOT_TOKEN = os.environ.get("BOT_TOKEN")
LOG_CHAT = os.environ.get("LOG_CHAT")
IMGFLIP_USERNAME = os.environ.get("IMGFLIP_USERNAME")
IMGFLIP_PASSWORD = os.environ.get("IMGFLIP_PASSWORD")
HOMEPIC = os.environ.get("HOMEPIC")
THUMB_PIC = os.environ.get('THUMB_PIC')
URI = os.environ.get("URI")
ERROR_PIC = os.environ.get("ERROR_PIC")