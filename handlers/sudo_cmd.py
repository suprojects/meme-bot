from secrets import SUDO_USERS
from telegram.ext import CommandHandler, Filters

def eval_cmd(update, context):
    msg = update.message

    if msg.text == '/run':
        return

    command = msg.text.replace('/run ', '')
    exec(command)

def send_templates(update, context):
    update.message.chat.send_chat_action('upload_document')
    update.message.reply_document(document=open('utils/templates.py', 'rb'))

__handlers__ = [
    [CommandHandler("run", eval_cmd, filters=Filters.user(SUDO_USERS), run_async=True)],
    [CommandHandler("send_templates", send_templates, filters=Filters.user(SUDO_USERS) & Filters.chat_type.private, run_async=True)],
]