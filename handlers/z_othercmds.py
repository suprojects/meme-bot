from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import InlineQueryHandler
from telegram.utils.helpers import create_deep_linked_url

from secrets import THUMB_PIC, HOMEPIC as homepic

from uuid import uuid4

def errorinline(update, context):

    result = [
        InlineQueryResultArticle(
            id = uuid4(),
            title = 'Unknown Command',
            description = "(╯°□°）╯︵ ┻━┻)",
            input_message_content = InputTextMessageContent("❌ Unrecognized Command"),
            thumb_url = 'https://telegra.ph/file/f13d453c19bf9beb3325c.png',
        ),
    ]

    update.inline_query.answer(result, cache_time = 0)



def blackinline(update, context):

    result = [
        InlineQueryResultArticle(
            id = uuid4(),
            title = f"Generate memes",
            description = f"Type 'meme' to generate a meme",
            input_message_content = InputTextMessageContent("💬 Inline Meme Generation help"),
            thumb_url = THUMB_PIC,
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = 'Click here', url = create_deep_linked_url(context.bot.username, 'help_inlinememe', False))]]),
        ),
    ]

    update.inline_query.answer(result, cache_time = 0)



__handlers__ = [
    [InlineQueryHandler(callback = errorinline, pattern = ('^'), run_async = True)],
    [InlineQueryHandler(callback = blackinline, run_async = True)],
]