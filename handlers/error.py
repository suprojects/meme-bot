from secrets import LOG_CHAT
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def error(update, context):

    try:
        if context.error.message == "Conflict: terminated by other getUpdates request; make sure that only one bot instance is running":
            return

        elif context.error.message == "Have no rights to send a message":
            update.message.chat.leave()
            return

        elif context.error.message == "Not enough rights to send photos to the chat":
            update.message.reply_text("I cannot send images here 🖼. How can you expect me to send a meme (which is obviously a pic)!\nI am leaving tis dum group.\n\nAnd here is a offer you can't (and should never) refuse:\n\n1. Enable permissions to send photos.\n2. Make me an admin\n3. Don't make memes in your life!")
            update.message.chat.leave()
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


__handlers__ = [
    ["error",error]
]