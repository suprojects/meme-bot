from telegram import MessageEntity
from telegram.ext import CallbackQueryHandler
from telegram.utils import helpers

def delete(update, context):
    query, user, chat, msg = update.callback_query, update.effective_user, update.effective_chat, update.effective_message

    inituser = int(update.callback_query.data.replace('delete_', ''))

    if user.id == inituser or chat.get_member(user_id = user.id).status in ("creator", "administrator"):

        if chat.get_member(user_id = context.bot.id).can_delete_messages and msg.reply_to_message:
            update.effective_message.reply_to_message.delete()

        query.message.delete()

    else:
        query.answer(text = "This is not your reply ✋", show_alert=True)
    

__handlers__ = [
    [CallbackQueryHandler(callback = delete, pattern = "^delete_", run_async=True)],
    ]
