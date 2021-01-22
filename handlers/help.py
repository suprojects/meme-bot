from telegram.ext import CommandHandler, CallbackQueryHandler,   Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.utils import helpers
from utils.templates import template
from utils.func import maketexts
from html import escape

def help_pvt(update, context):
    
    help_text = 'Tap on the buttons to see the help menu 😉.'

    BUTTONS = [
        [InlineKeyboardButton(text = '🤡 Meme Generator', callback_data = 'help_meme')],
        [InlineKeyboardButton(text = '🐤 Fake Tweet Generator', callback_data = 'help_tweet')]
    ]

    if update.callback_query:
        update.callback_query.edit_message_text(text = help_text, reply_markup = InlineKeyboardMarkup(BUTTONS))
        return

    update.message.reply_text(text = help_text, reply_markup = InlineKeyboardMarkup(BUTTONS))


def help_meme(update, context):

    help_text = f'''
❔ How to send memes ❓

You can send custom memes using me in 👤 private, a 👥 group.


<b>Meme Generation Format</b>:

<code>/meme</code> <code>{escape('<')}Keyword{escape('>')}</code> (the number of texts the meme supports).
<b>Example</b>: <code>/meme bf text1, text2, text3</code>

To see the meme's example, use <code>/memehelp</code> <code>{escape('<')}Keyword{escape('>')}</code>.
<b>Example</b>: <code>/memehelp bf</code>

To see the available meme templates, tap 👉 /templates
'''

    if update.callback_query:
        BUTTONS = [
            [InlineKeyboardButton(text = '💬 Inline Mode', callback_data = 'help_inlinememe')],
            [InlineKeyboardButton(text = '🔙 Go back', callback_data = 'help_home')],
        ]

        update.callback_query.edit_message_text(text = help_text, reply_markup = InlineKeyboardMarkup(BUTTONS), parse_mode = 'HTML')
        update.callback_query.answer()
        return

    update.message.reply_text(text = help_text, parse_mode = 'HTML')


def help_inlinememe(update, context):

    help_text = f'''

❔ How to use inline mode ❓

You can also send memes using me by 💬 Inline mode.
    

<b>Inline Meme Generation Format</b>:

<code>@{context.bot.username}</code> <code>meme</code> <code>template</code> <code>(the number of texts the meme supports)</code>

<b>Example</b>: <code>@{context.bot.username} meme drake text1, text2</code>
'''

    BUTTONS = [
        [InlineKeyboardButton(text = '💬 Try Inline', switch_inline_query_current_chat = f'meme drake Using Meme Generator websites, Create your own meme by using @{context.bot.username}')],
    ]

    if update.callback_query:

        BUTTONS.extend([
            [InlineKeyboardButton(text = '👤 Normal Mode', callback_data = 'help_meme')],
            [InlineKeyboardButton(text = '🔙 Go back', callback_data = 'help_home')],
        ])

        update.callback_query.edit_message_text(text = help_text, parse_mode = 'HTML', reply_markup = InlineKeyboardMarkup(BUTTONS))
        update.callback_query.answer()

    else: update.message.reply_text(help_text, parse_mode = 'HTML', reply_markup = InlineKeyboardMarkup(BUTTONS))



def help_tweet(update, context):
    update.callback_query.answer('Coming Soon 🔄', show_alert = True)


__handlers__ = [
    [CommandHandler("help", callback = help_pvt, filters=Filters.regex('^/help$') & Filters.chat_type.private, run_async=True)],
    [CallbackQueryHandler(pattern = "^help_home$", callback = help_pvt, run_async=True)],
    
    [CallbackQueryHandler(pattern = "^help_meme$", callback = help_meme, run_async=True)],

    [CallbackQueryHandler(pattern = "^help_inlinememe$", callback = help_inlinememe, run_async=True)],
    [CommandHandler("start", callback = help_inlinememe, filters=Filters.regex('help_inlinememe') & Filters.chat_type.private, run_async=True)],
    
    [CallbackQueryHandler(pattern = "^help_tweet$", callback = help_tweet, run_async=True)],
]