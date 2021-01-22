from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import InlineQueryHandler
from telegram.utils.helpers import create_deep_linked_url

from secrets import THUMB_PIC, HOMEPIC as homepic

from uuid import uuid4

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
    [InlineQueryHandler(callback = blackinline, run_async = True)],
]