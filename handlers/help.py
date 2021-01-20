from telegram.ext import CommandHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.utils import helpers
from utils.templates import template
from utils.func import maketexts
from html import escape


def memehelp(update, context):

    meme_help = InlineKeyboardButton(text="Meme Template Help", url=helpers.create_deep_linked_url(context.bot.username, "memehelp", False))

    usr, msg = update.message.from_user, update.message

    RawText = msg.text[int(msg.entities[0].length + 1):]

    if RawText == '':
        BUTTON_MARKUP = InlineKeyboardMarkup([[meme_help],[InlineKeyboardButton("OK", callback_data=(f"delete_{usr.id}"))]]) if msg.chat.type != 'private' else InlineKeyboardMarkup([[meme_help]])
        msg.reply_text(text = 'Read the Meme help', reply_markup = BUTTON_MARKUP)
        return


    RawMemeTemplate = RawText.split()[0]
    MemeTemplate = template.get(RawMemeTemplate)

    if not MemeTemplate:
        delete_button = InlineKeyboardButton("OK", callback_data=(f"delete_{usr.id}"))
        BUTTON_MARKUP = InlineKeyboardMarkup([[delete_button]]) if msg.chat.type != 'private' else None
        msg.reply_text(text = (f"<code>{RawMemeTemplate}</code> is not a valid Meme Template. Send me a valid Meme Template."), parse_mode = 'HTML', reply_markup = BUTTON_MARKUP)
        return

    texts = maketexts(MemeTemplate.get('texts'))

    BUTTON_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton("OK", callback_data=(f"delete_{usr.id}"))]]) if msg.chat.type != 'private' else None
    msg.reply_photo(MemeTemplate.get('help'), caption = f'<code>/meme {RawMemeTemplate} {texts}</code>', parse_mode = 'HTML', reply_markup = BUTTON_MARKUP)


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
<b>Example</b>: <code>/meme bf text1, text2</code>

To see the meme's example, use <code>/memehelp</code> <code>{escape('<')}Keyword{escape('>')}</code>.
<b>Example</b>: <code>/memehelp bf</code>

To see the available meme templates, tap 👉 /templates
''', parse_mode = 'HTML', reply_markup = BUTTON_MARKUP)


def help_templates(update, context):

    helptemplate = str()

    for eachtemplate in template:
        helptemplate = str(helptemplate) + '\n' + '<code>' + str(eachtemplate) + '</code>' + ' - ' + str(template.get(eachtemplate).get('texts')) + ' texts'
    
    update.message.reply_text(text = f'Available Meme templates:\n{helptemplate}\n\nTo get an example of the meme, send /memehelp <code>{escape("<")}Template{escape(">")}</code>', parse_mode = 'HTML')

def templates_group(update, context):
    meme_help = InlineKeyboardButton(text="Meme Template Help", url=helpers.create_deep_linked_url(context.bot.username, "memehelp", False))
    usr, msg = update.message.from_user, update.message

    BUTTON_MARKUP = InlineKeyboardMarkup([[meme_help]])
    msg.reply_text(text = 'See the available Meme templates', reply_markup = BUTTON_MARKUP)

__handlers__ = [
    
    [CommandHandler("memehelp", callback = memehelp, run_async=True)],
    [CommandHandler("help", callback = help_pvt, filters=Filters.regex('^/help$') & Filters.chat_type.private, run_async=True)],
    [CommandHandler("templates", callback = templates_group, filters=Filters.chat_type.group, run_async=True)],
]