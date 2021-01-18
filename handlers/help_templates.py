from telegram.ext import Filters, CommandHandler, CallbackQueryHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from utils.templates import template
from utils.func import maketexts, btns, emotes, navbtn

from secrets import HOMEPIC


def templatelist(update, context):

    rawkeyboard = btns(5)
    keyboard = rawkeyboard[0]

    keyboard.append(navbtn(1, len(rawkeyboard)))

    BUTTONS = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        update.callback_query.message.edit_media(media = InputMediaPhoto(media = homepic, caption = 'Select the meme template to see the usage and the meme example', parse_mode = 'HTML'), reply_markup = BUTTONS)
        return

    update.message.reply_photo(homepic, caption = 'Select the meme template to see the usage and the meme example', reply_markup = BUTTONS)


def templ(update, context):
    qry = update.callback_query

    helptempl = qry.data.replace('templ_', '')
    MemeTemplate = template.get(helptempl)
    try:
        texts = maketexts(MemeTemplate.get('texts'))

    except AttributeError:
        qry.answer(f"Template '{helptempl}' was either removed, or is missing.", show_alert = True)
        return

    qry.edit_message_media(media = InputMediaPhoto(media = MemeTemplate.get('help'), caption = f'<code>/meme {helptempl} {texts}</code>', parse_mode = 'HTML'), reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = '🔙', callback_data = 'templist')]]))
    
    qry.answer()


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
            qry.answer(text = "✋ Switched to page {}".format(emotes.get(1) if page > len(rawkeyboard) else emotes.get(len(rawkeyboard))), show_alert = True)

        except:
            qry.answer(text = 'No more pages', show_alert = True)

        return


    keyboard = rawkeyboard[page - 1]

    keyboard.append(navbtn(page, len(rawkeyboard)))

    try:
        qry.edit_message_reply_markup(reply_markup = InlineKeyboardMarkup(keyboard))
        qry.answer(text = f"Switced to page {emotes.get(page)}")

    except:
        qry.answer(text = 'No more pages', show_alert = True)

    



def currpage(update, context): update.callback_query.answer(text = f"Showing page {emotes.get(int(update.callback_query.data.replace('currpage_', '')))}", show_alert = True)

__handlers__ = [

    [CommandHandler('templates', callback = templatelist, filters = Filters.chat_type.private, run_async = True)],
    [CallbackQueryHandler(pattern = "^templ_", callback = templ, run_async=True)],
    [CallbackQueryHandler(pattern = "^templist$", callback = templatelist, run_async=True)],
    [CallbackQueryHandler(pattern = "^page_", callback = navigate, run_async=True)],
    [CallbackQueryHandler(pattern = "^currpage_", callback = currpage, run_async=True)],
]