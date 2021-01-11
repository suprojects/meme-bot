from telegram.ext import CommandHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from html import escape

def start(update, context):
    usr,msg = update.message.from_user, update.message

    msg.reply_text(text = f'''

Hello <a href="tg://user?id={usr.id}">{escape(usr.first_name)}</a> 👋. I am a really cool Memer bot 😎.

I can generate memes for you 🤩!

Send /help to know more.
''', parse_mode = 'HTML')


def start_group(update, context):
    update.message.reply_text(text = f'Alive and ready to generate memes!', reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🆒", callback_data=(f"delete_{update.message.from_user.id}"))]]))


__handlers__ = [
    [CommandHandler("start", callback = start, filters = Filters.chat_type.private & Filters.regex('^/start$'), run_async=True)],
    [CommandHandler("start", callback = start_group, filters = Filters.chat_type.groups, run_async=True)],
]
