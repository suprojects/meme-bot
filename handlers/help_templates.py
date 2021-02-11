from telegram.ext import Filters, CommandHandler, CallbackQueryHandler, Filters
from telegram.utils import helpers
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from utils.templates import template
from utils.func import maketexts, btns, emotes, navbtn
from ast import literal_eval as convert
from secrets import HOMEPIC as homepic
from database import botusers


def templates_group(update, context):
    meme_help = InlineKeyboardButton(text="Meme Template Help", url=helpers.create_deep_linked_url(context.bot.username, "memetempl", False))
    usr, msg = update.message.from_user, update.message

    BUTTON_MARKUP = InlineKeyboardMarkup([[meme_help]])
    msg.reply_text(text = 'See the available Meme templates', reply_markup = BUTTON_MARKUP)



def memetemplhelp(update, context):

    meme_help = InlineKeyboardButton(text="Meme Template Help", url=helpers.create_deep_linked_url(context.bot.username, "memetempl", False))

    usr, msg = update.message.from_user, update.message

    if msg.text.startswith('/start'): RawText = msg.text.replace('/start memehelp_', '')

    else: RawText = msg.text[int(msg.entities[0].length + 1):]

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

    BUTTON_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton("OK", callback_data=(f"delete_{usr.id}"))]]) if msg.chat.type != 'private' else '' if msg.text.startswith('/start memehelp_') else InlineKeyboardMarkup([[InlineKeyboardButton("Switch to Inline ↩️", switch_inline_query = (f"meme {RawMemeTemplate}"))]])
    sentmsg = msg.reply_photo(MemeTemplate.get('help'), caption = f'<code>/meme {RawMemeTemplate} {texts}</code>', parse_mode = 'HTML', reply_markup = BUTTON_MARKUP)

    if msg.text.startswith('/start memehelp_') and msg.chat.type == 'private':
        sentmsg.edit_reply_markup(reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Return to chat ↩️", switch_inline_query = (f"meme {RawMemeTemplate}"))]]))


def templatelist(update, context):

    rawkeyboard = btns(5)
    keyboard = rawkeyboard[0]

    keyboard.append(navbtn(1, len(rawkeyboard)))

    BUTTONS = InlineKeyboardMarkup(keyboard)

    update.message.reply_photo(homepic, caption = 'Select the meme template to see the usage and the meme example', reply_markup = BUTTONS)

    botusers.new_user(update.message.from_user)


def templ(update, context):

    keyboard = convert(str(update.callback_query.message.reply_markup)).get('inline_keyboard')

    page = int((keyboard[-1][1].get('callback_data')).replace('currpage_', ''))

    qry = update.callback_query

    helptempl = qry.data.replace('templ_', '')
    MemeTemplate = template.get(helptempl)

    try:
        texts = maketexts(MemeTemplate.get('texts'))

    except AttributeError:
        qry.answer(f"Template '{helptempl}' was either removed, or is missing.", show_alert = True)
        return

    BUTTONS = [
        [InlineKeyboardButton(text = 'Switch to Inline mode ↩️', switch_inline_query = f"meme {helptempl}")],
        [InlineKeyboardButton(text = '🔙', callback_data = f'templist_{page}')],
    ]

    qry.edit_message_media(media = InputMediaPhoto(media = MemeTemplate.get('help'), caption = f'<code>/meme {helptempl} {texts}</code>', parse_mode = 'HTML'), reply_markup = InlineKeyboardMarkup(BUTTONS))  
    qry.answer()



def navback(update, context):

    page = int(update.callback_query.data.replace('templist_', ''))

    rawkeyboard = btns(5)
    keyboard = rawkeyboard[page - 1]

    keyboard.append(navbtn(page, len(rawkeyboard)))

    update.callback_query.message.edit_media(media = InputMediaPhoto(media = homepic, caption = 'Select the meme template to see the usage and the meme example', parse_mode = 'HTML'), reply_markup = InlineKeyboardMarkup(keyboard))
    update.callback_query.answer()



def navigate(update, context):
    qry = update.callback_query
    page = int(qry.data.replace('page_', ''))
    
    rawkeyboard = btns(5)


    if page not in range(1, len(rawkeyboard) + 1):

        if page > len(rawkeyboard):
            keyboard = rawkeyboard[0]
            nav = navbtn(1, len(rawkeyboard))

        elif page < len(rawkeyboard):
            keyboard = rawkeyboard[-1]
            nav = navbtn(len(rawkeyboard), len(rawkeyboard))

        else:
            qry.answer("Page does not exist", show_alert = True)
            return

        keyboard.append(nav)

        try:
            qry.edit_message_reply_markup(reply_markup = InlineKeyboardMarkup(keyboard))
            qry.answer(text = "✋ Switched to page {}".format(emotes.get(1) if page > len(rawkeyboard) else emotes.get(len(rawkeyboard))), show_alert = False)

        except:
            qry.answer(text = 'No more pages', show_alert = True)

        return


    keyboard = rawkeyboard[page - 1]

    keyboard.append(navbtn(page, len(rawkeyboard)))

    try:
        qry.edit_message_reply_markup(reply_markup = InlineKeyboardMarkup(keyboard))
        qry.answer()

    except:
        qry.answer(text = 'No more pages', show_alert = True)




def currpage(update, context): update.callback_query.answer(text = f"Showing page {emotes.get(int(update.callback_query.data.replace('currpage_', '')))}", show_alert = True)




__handlers__ = [

    [CommandHandler('templates', callback = templatelist, filters = Filters.chat_type.private, run_async = True)],
    [CommandHandler("templates", callback = templates_group, filters=Filters.chat_type.group, run_async=True)],
    [CommandHandler("start", templatelist, Filters.chat_type.private & Filters.regex('memetempl'), pass_args=False)],
    [CommandHandler("memehelp", callback = memetemplhelp, run_async=True)],

    [CommandHandler("start", filters = Filters.regex('memehelp_'), callback = memetemplhelp, pass_args = True, run_async=True)],

    [CallbackQueryHandler(pattern = "^templ_", callback = templ, run_async=True)],
    [CallbackQueryHandler(pattern = "^templist_", callback = navback, run_async=True)],
    [CallbackQueryHandler(pattern = "^page_", callback = navigate, run_async=True)],
    [CallbackQueryHandler(pattern = "^currpage_", callback = currpage, run_async=True)],
]