from telegram.ext import CommandHandler, CallbackQueryHandler,   Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.utils import helpers
from utils.templates import template
from utils.func import maketexts
from html import escape

def help_pvt(update, context):
    
    name = escape(update.message.from_user.first_name if update.message else update.callback_query.message.chat.first_name)

    help_text = f"""
Hello {name} 👋. I am the bot 🤖 that is going to take over the world 🌍 soon, real soon...

You should already know about me, but no don't worry if you don't. Ill give you a second chance.

I am the {context.bot.first_name}, the untimate Meme Madness. I can generate 🆒 memes 4 u ╰(*°▽°*)╯

Nothing much, just tap on these button you see below. You know... 🔽🔽🔽 theeese buttons. 
"""

    BUTTONS = [
        [InlineKeyboardButton(text = '🤡 Meme Generator', callback_data = 'help_meme')],
        [InlineKeyboardButton(text = '🐤 Fake Tweet Generator', callback_data = 'help_tweet')],
        [InlineKeyboardButton(text = '🙅‍♂️ DO NOT CLICK ELSE THINGS WILL BREAK', callback_data = 'help_support')],
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


def support(update, context):

    BUTTONS = [
        [
            InlineKeyboardButton(text = '👥 Amazing Community', url = 'https://t.me/su_Chats'),
            InlineKeyboardButton(text = '🔈 More Projects', url = 'https://t.me/su_Bots'),
        ],
    ]

    help_text = 'Congratulations 🎉! You have found out our secret headquarters 🏢. Let this be a secret 🤐. Do not tell any spies out there 🤫! You are invited to join our secret community. Who-hoo 🥳!'

    if update.callback_query:
        BUTTONS.append([InlineKeyboardButton(text = '🔙 Go Back', callback_data = 'help_home')])
        update.callback_query.answer('Shhhh 🤫', show_alert = True)
        update.callback_query.edit_message_text(text = help_text, reply_markup = InlineKeyboardMarkup(BUTTONS))

    else: update.message.reply_text(text = help_text, reply_markup = BUTTONS)



__handlers__ = [
    [CommandHandler("help", callback = help_pvt, filters=Filters.regex('^/help$') & Filters.chat_type.private, run_async=True)],
    [CallbackQueryHandler(pattern = "^help_home$", callback = help_pvt, run_async=True)],
    
    [CallbackQueryHandler(pattern = "^help_meme$", callback = help_meme, run_async=True)],

    [CallbackQueryHandler(pattern = "^help_inlinememe$", callback = help_inlinememe, run_async=True)],
    [CommandHandler("start", callback = help_inlinememe, filters=Filters.regex('help_inlinememe') & Filters.chat_type.private, run_async=True)],
    
    [CallbackQueryHandler(pattern = "^help_tweet$", callback = help_tweet, run_async=True)],

    [CallbackQueryHandler(pattern = "^help_support$", callback = support, run_async=True)],
]