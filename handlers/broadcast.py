from database import botusers, botchats
from telegram.ext import CommandHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, error
from secrets import SUDO_USERS


def broadcast(update, context):
    msg = update.message

    text = msg.text[msg.entities[0]['length'] + 1:]

    users = botusers.bot_users()

    update.message.reply_text(f"Broadcasting message to {len(users)} chats 📤\n\n{text}")

    success, failed, total = int(0), int(0), int(0)

    for user in users:

        try:
            context.bot.send_message(user['id'], text)
            success += 1

        except error.Unauthorized:
            botusers.remove_user(user['id'])
            failed += 1

        total += 1

    update.message.reply_text(f"Broadcast Complete 📤\n\n🔢 Chats Count: <code>{len(users)}</code> chats\n💬 Total attempts: <code>{total}</code> chats\n✅ Successfully sent: <code>{success}</code> chats\n❌ Failed (Blocked by user): <code>{failed}</code> chats", parse_mode = 'HTML')

def group_broadcast(update, context):
    msg = update.message

    text = msg.text[msg.entities[0]['length'] + 1:]

    chats = botchats.all_chats()

    update.message.reply_text(f"Broadcasting message to {len(chats)} Groups 📤\n\n{text}")

    success, failed, total = int(0), int(0), int(0)

    for chat in chats:

        try:
            context.bot.send_message(chat['id'], text)
            success += 1

        except error.BadRequest:
            botchats.remove_chats(chat['id'])
            failed += 1

        total += 1

    update.message.reply_text(f"Broadcast Complete 📤\n\n🔢 Groups Count: <code>{len(chats)}</code> chats\n💬 Total attempts: <code>{total}</code> chats\n✅ Successfully sent: <code>{success}</code> chats\n❌ Failed (Kicked from group): <code>{failed}</code> chats", parse_mode = 'HTML')


__handlers__ = [
    [CommandHandler('broadcast', broadcast, filters= Filters.user(SUDO_USERS), run_async= True)],
    [CommandHandler('grpbroadcast', group_broadcast, filters= Filters.user(SUDO_USERS), run_async= True)],
]