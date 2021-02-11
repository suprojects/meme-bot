from secrets import SUDO_USERS

from database import botchats, botusers
from telegram.ext import CommandHandler, Filters, MessageHandler
from utils import paste

def add_group(update, context):
    botchats.update_chat(update.effective_chat)


def botuserlist(update, context):

    msg = update.message.reply_text('🔄')

    all_ = botusers.bot_users()
    res = ""

    for user in all_: res += user["firstname"] + " - " + str(user["id"]) + "\n"

    msg.edit_text(paste.neko(res))


def chatlist(update, context):

    msg = update.message.reply_text('🔄')

    all_ = botchats.all_chats()
    res = ""

    for chat in all_: res += chat["title"] + " - " + str(chat["id"]) + "\n"

    msg.edit_text(paste.neko(res))


def stats(update, context):
    msg = update.message.reply_text('🔄')

    msg.edit_text(text = f'''
Stats of {context.bot.first_name}

👤 @{context.bot.username}
🆔 <code>{context.bot.id}</code>

🤖 Bot users: <code>{len(botusers.bot_users())}</code>
👥 Groups: <code>{len(botchats.all_chats())}</code>

''', parse_mode = 'HTML')


__handlers__ = [
    [CommandHandler("botusers", botuserlist, filters = Filters.user(SUDO_USERS), run_async=True)],
    [CommandHandler("botchats", chatlist, filters = Filters.user(SUDO_USERS), run_async=True)],
    [CommandHandler("botstats", stats, filters = Filters.user(SUDO_USERS), run_async=True)],

    [MessageHandler(Filters.all & Filters.chat_type.supergroup & ~Filters.forwarded & ~Filters.command, add_group, run_async=True)],
]
