from secrets import LOG_CHAT
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def error(update, context):

    try:
        if context.error.message == "Conflict: terminated by other getUpdates request; make sure that only one bot instance is running":
            return

        else:
            pass
    except:
        pass

    context.bot.send_message(chat_id = LOG_CHAT, text = (f"""

#{context.bot.username}

Error:
{context.error}

Update:
{update}

"""))

    try:
        if context.error.message == "Have no rights to send a message":
            update.message.chat.leave()

        else:
            update.message.reply_text("⚠ An unexpected error occured, the error report was forwarded to the developers.")  
    except:
        pass


__handlers__ = [
    ["error",error]
]