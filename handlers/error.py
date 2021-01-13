from secrets import LOG_CHAT
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.make import make

from utils.templates import template
from utils.syncfiles import sync


def error(update, context):

    try:
        
        if context.error.message.startswith("Wrong remote file identifier specified"):
            RawMemeTemplate = update.message.text.replace(update.message.text.split()[0] + ' ', '')
            MemeTemplate = template.get(RawMemeTemplate)

            texts = str(", ".join(["text" + str(i) for i in range(1, int(MemeTemplate.get('texts')) + 1)]))

            print((texts).split(','))

            examplepic = make(MemeTemplate.get('id'), texts.split(','))

            pic = update.message.reply_photo(examplepic, caption = f'<code> /meme {RawMemeTemplate} {str(texts)}</code>', parse_mode = 'HTML')

            template[RawMemeTemplate] = {'id': MemeTemplate.get('id'), 'texts': MemeTemplate.get('texts'), 'help': pic.photo[0].file_id}

            NewFileData = f'template = {template}'

            OldFile = open(f'utils/templates.py', 'w')
            OldFile.write(NewFileData)
            OldFile.close()

            sync()

            return

        elif context.error.message == "Conflict: terminated by other getUpdates request; make sure that only one bot instance is running":
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
    ["error",error],
]