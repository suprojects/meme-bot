from telegram.ext import CommandHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.utils import helpers
from utils.templates import template
from utils.func import maketexts
from html import escape

def help_pvt(update, context):
    usr,msg = update.message.from_user, update.message

    BUTTON_MARKUP = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="Our Channel 🔈", url="https://t.me/su_Bots"),
                InlineKeyboardButton(text="Discussion group 👥",url="https://t.me/su_Chats")
            ]
        ])

    msg.reply_text(text = f'''

❔ How to send memes ❓

You can generate memes using me in 👤 private or in a 👥 group (💬 Inline coming soon!).


<b>Meme Generation Format</b>:

<code>/meme</code> <code>{escape('<')}Keyword{escape('>')}</code> <code>text1, text2, text3 ...</code>\n(the number of texts the meme supports).
<b>Example</b>: <code>/meme bf text1, text2, text3</code>

To see the meme's example, use <code>/memehelp</code> <code>{escape('<')}Keyword{escape('>')}</code>.
<b>Example</b>: <code>/memehelp bf</code>

To see the available meme templates, tap 👉 /templates
''', parse_mode = 'HTML', reply_markup = BUTTON_MARKUP)


__handlers__ = [
    [CommandHandler("help", callback = help_pvt, filters=Filters.regex('^/help$') & Filters.chat_type.private, run_async=True)],
]