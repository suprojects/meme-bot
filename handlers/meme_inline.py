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
            input_message_content = InputTextMessageContent(f'Hey {update.inline_query.from_user.first_name} ✋, stop being so dumb 🗑 and read the popup messages before clicking @$#&!.'),
            thumb_url = THUMB_PIC,
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Available Meme Templates", url=create_deep_linked_url(context.bot.username, "memetempl", False))]])         
    )
]

    update.inline_query.answer(result, switch_pm_text = 'Available Meme Templates', switch_pm_parameter = 'memetempl', cache_time = 0)

def inlinetempl(update, context):

    qry = update.inline_query

    RawMemeTemplate = qry.query.replace('meme', '').strip()
    templ = template.get(RawMemeTemplate)

    if not templ:

        result = [
            InlineQueryResultArticle(
                id = uuid4(),
                title = f"Invalid Meme Template - {RawMemeTemplate}",
                description = f"'{RawMemeTemplate}' is not a Valid meme template.",
                input_message_content = InputTextMessageContent(f'{RawMemeTemplate} is not a template! What do you expect me to send here you noob? 🤡'),
                thumb_url = "https://telegra.ph/file/f13d453c19bf9beb3325c.png",
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Available Meme Templates", url=create_deep_linked_url(context.bot.username, "memetempl", False))]])
        )
    ]
        update.inline_query.answer(result, switch_pm_text = 'Available Meme Templates', switch_pm_parameter = 'memetempl', cache_time = 0)
        return


    result = [
        InlineQueryResultCachedPhoto(
            type = 'photo',
            id = uuid4(),
            photo_file_id = templ.get('help'),
            caption = f"Hey {escape(qry.from_user.first_name)}, you noob, stop clicking on the photo and give me some proper keywords!",
            parse_mode = 'HTML',
        ),

        InlineQueryResultArticle(
            id = uuid4(),
            title = f"Using template - {RawMemeTemplate}",
            description = f"Required texts: {templ.get('texts')}\nType the texts for the meme",
            input_message_content = InputTextMessageContent(f"Wae u gey {escape(qry.from_user.first_name)} 🏳️‍🌈? You neeed to give me the <code>{templ.get('texts')}</code> texts I need to put it in the meme <code>{RawMemeTemplate}</code>. Delet tis right now 🚮 and give me a proper symtax! 🤦‍♂️", parse_mode = 'HTML'),
            thumb_url = THUMB_PIC,
        ),
    ]
    
    qry.answer(result, cache_time = 0)



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
                input_message_content = InputTextMessageContent(f'{RawMemeTemplate} is not a template! What do you expect me to send here you noob? 🤡'),
                thumb_url = "https://telegra.ph/file/f13d453c19bf9beb3325c.png",
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Available Meme Templates", url=create_deep_linked_url(context.bot.username, "memetempl", False))]])
        )
    ]
        update.inline_query.answer(result, switch_pm_text = 'Available Meme Templates', switch_pm_parameter = 'memetempl', cache_time = 0)
        return


    texts = (qry.query.replace(qry.query.split()[0], '').replace(qry.query.split()[1], '').strip()).split(',')


    if int(len(texts)) != int(templ.get('texts')):

        result = [
            InlineQueryResultCachedPhoto(
                type = 'photo',
                id = uuid4(),
                photo_file_id = templ.get('help'),
                caption = f"I am once again asking for your support 💁‍♂️. Stop pressing the pic and <b>READ THE PROMPTS!</b>.",
                parse_mode = 'HTML',
            ),

            InlineQueryResultArticle(
                id = uuid4(),
                title = f"Using template - {RawMemeTemplate}",
                description = f"Required texts: {templ.get('texts')}\nGiven texts: {len(texts)}",
                input_message_content = InputTextMessageContent(f"❌ You game me <code>{len(texts)}</code> texts for the meme '<code>{RawMemeTemplate}</code>', but I need <code>{templ.get('texts')}</code>. Kindly delete this 🚮 repeat the process, but this time, read the prompts shown.", parse_mode = 'HTML'),
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
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = 'SU Projects', url = 'https://t.me/su_bots')]])
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
    if not search('^meme\s([^\s]+)\s\w.*$', update.chosen_inline_result.query): return
    
    qry = update.chosen_inline_result

    RawMemeTemplate = qry.query.split()[1].strip()
    templ = template.get(RawMemeTemplate)

    if not templ: return

    texts = (qry.query.replace(qry.query.split()[0], '').replace(qry.query.split()[1], '').strip()).split(',')

    if int(len(texts)) != int(templ.get('texts')): return

    context.bot.editMessageMedia(inline_message_id = qry.inline_message_id, media = InputMediaPhoto(make(templ.get('id'), texts)))


__handlers__= [

    [InlineQueryHandler(callback = inlineblank, pattern = ('^meme$'))],
    [InlineQueryHandler(callback = inlinetempl, pattern = ('^meme\s[^\s]\w*$'))],
    [InlineQueryHandler(callback = inlinememe, pattern = ('^meme\s([^\s]+)\s\w.*$'))],
    [ChosenInlineResultHandler(callback = editinline, run_async = True)],
]