from secrets import THUMB_PIC, HOMEPIC as homepic

from uuid import uuid4
from ast import literal_eval as convert
from html import escape
from re import search

from telegram import InlineQueryResultArticle, InlineQueryResultCachedPhoto, InputTextMessageContent, InputMediaPhoto
from telegram.ext import InlineQueryHandler, ChosenInlineResultHandler

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, Filters, CallbackQueryHandler

from telegram.utils.helpers import create_deep_linked_url

from utils.templates import template
from utils.func import maketexts, btns, navbtn, emotes
from utils.make import make


def inlineblank(update, context):

    result = [
        InlineQueryResultArticle(
            id = uuid4(),
            title = "Generate Meme",
            description = "Type in a meme template.",
            input_message_content = InputTextMessageContent('❌ Invalid action'),
            thumb_url = THUMB_PIC,
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Available Meme Templates", url=create_deep_linked_url(context.bot.username, "memetempl", False))]])         
    )
]

    update.inline_query.answer(result, switch_pm_text = 'Available Meme Templates', switch_pm_parameter = 'memetempl')

def inlinetempl(update, context):

    qry = update.inline_query

    RawMemeTemplate = qry.query.split()[1].strip()
    templ = template.get(RawMemeTemplate)

    if not templ:

        result = [
            InlineQueryResultArticle(
                id = uuid4(),
                title = f"Invalid Meme Template - {RawMemeTemplate}",
                description = f"'{RawMemeTemplate}' is not a Valid meme template.",
                input_message_content = InputTextMessageContent(f'{RawMemeTemplate} is not a template!'),
                thumb_url = "https://telegra.ph/file/f13d453c19bf9beb3325c.png",
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Available Meme Templates", url=create_deep_linked_url(context.bot.username, "memetempl", False))]])
        )
    ]
        update.inline_query.answer(result, switch_pm_text = 'Available Meme Templates', switch_pm_parameter = 'memetempl')
        return


    result = [
        InlineQueryResultCachedPhoto(
            type = 'photo',
            id = uuid4(),
            photo_file_id = templ.get('help'),
            caption = '❌ Invalid action',
            parse_mode = 'HTML',
        ),

        InlineQueryResultArticle(
            id = uuid4(),
            title = f"Using template - {RawMemeTemplate}",
            description = f"Required texts: {templ.get('texts')}\nType the texts for the meme",
            input_message_content = InputTextMessageContent('❌ Invalid action'),
            thumb_url = THUMB_PIC,
        ),
    ]
    
    qry.answer(result, switch_pm_text = f"Template - '{RawMemeTemplate}'", switch_pm_parameter = f'memehelp_{RawMemeTemplate}')



def inlinememe(update, context):
    qry = update.inline_query

    RawMemeTemplate = qry.query.split()[1].strip()
    templ = template.get(RawMemeTemplate)


    if not templ:

        result = [
            InlineQueryResultArticle(
                id = uuid4(),
                title = f"Invalid Meme Template - {RawMemeTemplate}",
                description = f"'{RawMemeTemplate}' is not a Valid meme template.",
                input_message_content = InputTextMessageContent('❌ Invalid action'),
                thumb_url = "https://telegra.ph/file/f13d453c19bf9beb3325c.png",
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Available Meme Templates", url=create_deep_linked_url(context.bot.username, "memetempl", False))]])
        )
    ]
        update.inline_query.answer(result, switch_pm_text = 'Available Meme Templates', switch_pm_parameter = 'memetempl')
        return


    texts = (qry.query.replace(qry.query.split()[0], '').replace(qry.query.split()[1], '').strip()).split(',')


    if int(len(texts)) != int(templ.get('texts')):

        result = [
            InlineQueryResultCachedPhoto(
                type = 'photo',
                id = uuid4(),
                photo_file_id = templ.get('help'),
                caption = ('❌ Invalid action'),
                parse_mode = 'HTML',
            ),

            InlineQueryResultArticle(
                id = uuid4(),
                title = f"Using template - {RawMemeTemplate}",
                description = f"Required texts: {templ.get('texts')}\nGiven texts: {len(texts)}",
                input_message_content = InputTextMessageContent('❌ Invalid action'),
                thumb_url = THUMB_PIC,
            ),
        ]

        qry.answer(result, cache_time = 0)
        return


    result = [
        InlineQueryResultCachedPhoto(
            type = 'photo',
            id = uuid4(),
            photo_file_id = templ.get('help'),
            caption = ('🔄 Working on it 🔄'),
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = '🔄 Creating. Please Wait... 🤡', url = 'https://t.me/su_bots')]]),
        ),

        InlineQueryResultArticle(
            id = uuid4(),
            title = f"Meme ready",
            description = f"Your meme {RawMemeTemplate} is ready. Click on the above image to send your meme.",
            input_message_content = InputTextMessageContent("❌ You shouldn't have clicked on me. Please read the help next time."),
            thumb_url = 'https://telegra.ph/file/3af5249604a7dbf5416be.jpg',
        ),
    ]

    qry.answer(result, cache_time = 0)


def editinline(update, context):
    
    if not search('^meme\s([^\s]+)\s\w.*$', update.chosen_inline_result.query) or not update.chosen_inline_result.inline_message_id: return

    qry = update.chosen_inline_result

    RawMemeTemplate = qry.query.split()[1].strip()
    templ = template.get(RawMemeTemplate)

    if not templ: return

    texts = (qry.query.replace(qry.query.split()[0], '').replace(qry.query.split()[1], '').strip()).split(',')

    if int(len(texts)) != int(templ.get('texts')): return

    context.bot.editMessageMedia(inline_message_id = qry.inline_message_id, media = InputMediaPhoto(make(templ.get('id'), texts)))


__handlers__= [

    [InlineQueryHandler(callback = inlineblank, pattern = ('^meme$'), run_async = True)],
    [InlineQueryHandler(callback = inlinetempl, pattern = ('^meme\s[^\s]\w*$'), run_async = True)],
    [InlineQueryHandler(callback = inlinememe, pattern = ('^meme\s([^\s]+)\s\w.*$'), run_async = True)],
    [ChosenInlineResultHandler(callback = editinline, run_async = True)],
]