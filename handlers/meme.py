from telegram.ext import CommandHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from utils import make
from utils.templates import template
from html import escape
from telegram.utils import helpers


def MakeMeme(update, context):

    meme_template = InlineKeyboardButton(text="Meme Template Help", url=helpers.create_deep_linked_url(context.bot.username, "memehelp", False))
   
    msg,usr,cht = update.message, update.message.from_user, update.message.chat

    if msg.text == '/meme':
        BUTTON_MARKUP = InlineKeyboardMarkup([[meme_template],[InlineKeyboardButton("OK", callback_data=(f"delete_{usr.id}"))]]) if cht.type != 'private' else InlineKeyboardMarkup([[meme_template]])
        msg.reply_text(text = "What meme you wanna make?", parse_mode = 'HTML', reply_markup = BUTTON_MARKUP)
        return

    RawText = msg.text.replace('/meme ', '')
    RawMemeTemplate = RawText.split()[0]
    MemeTemplate = template.get(RawMemeTemplate)

    if not MemeTemplate:
        BUTTON_MARKUP = InlineKeyboardMarkup([[meme_template],[InlineKeyboardButton("OK", callback_data=(f"delete_{usr.id}"))]]) if cht.type != 'private' else InlineKeyboardMarkup([[meme_template]])
        msg.reply_text(text = (f"<code>{RawMemeTemplate}</code> is not a valid Meme Template.\nSend me a valid Meme Template."), parse_mode = 'HTML', reply_markup = BUTTON_MARKUP)
        return


    MemeID = int(MemeTemplate.get('id'))
    RawMemeText = RawText.replace(RawMemeTemplate, '')


    if RawMemeText == '':
        BUTTON_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton("OK", callback_data=(f"delete_{usr.id}"))]]) if cht.type != 'private' else None
        msg.reply_text(text = (f"Give me <code>{MemeTemplate.get('texts')}</code> texts separated by a comma."), parse_mode = 'HTML', reply_markup = BUTTON_MARKUP)
        return


    MemeText = RawMemeText.split(',')


    if (len(MemeText) != int(MemeTemplate.get('texts'))):
        BUTTON_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton("OK", callback_data=(f"delete_{usr.id}"))]]) if cht.type != 'private' else None
        update.message.reply_text(text = (f"Give me <code>{MemeTemplate.get('texts')}</code> texts separated by a comma.\nYou gave me <code>{len(MemeText)}</code>."), parse_mode = 'HTML', reply_markup = BUTTON_MARKUP)
        return

    if cht.get_member(user_id = context.bot.id).can_delete_messages and cht.type != 'private': msg.delete()

    update.message.chat.send_chat_action('upload_photo')

    if msg.reply_to_message and cht.type != 'private':
        msg.reply_to_message.reply_photo(make.make(MemeID, MemeText), caption = f'By: <a href="tg://user?id={usr.id}">{escape(usr.first_name)}</a>', parse_mode = 'HTML')
        return

    msg.reply_photo(make.make(MemeID, MemeText), caption = f'By: <a href="tg://user?id={usr.id}">{escape(usr.first_name)}</a>', parse_mode = 'HTML', quote = False)
    return

__handlers__ = [
    [CommandHandler("meme", callback = MakeMeme, run_async=True)],

]