from telegram.ext import Updater
from secrets import BOT_TOKEN, SUDO_USERS

updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher

from os import path

if not path.exists('utils/templates.py'):
    templfile = open('utils/templates.py', 'w+')
    templfile.write("template = {}")
    templfile.close()

if __name__ == "__main__":
    import sys
    import os
    from threading import Thread
    from telegram.ext import CommandHandler, Filters
    from handlers import all_handlers
    from secrets import SUDO_USERS
    import logging

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

    logger = logging.getLogger(__name__)

    for arg in sys.argv:
        if "-r" in arg:
            for SUDO_USER in SUDO_USERS:
                updater.bot.send_message(
                    SUDO_USER, arg.replace("-r", ""))

    def stop_and_restart(name):
        updater.stop()
        os.system("git pull")
        args = sys.argv
        for i in range(len(args)):
            if "-r" in args[i]:
                del args[i]
        os.execl(sys.executable, sys.executable, *args,
                 f"Bot restarted successfully. Initialted by -r{name}.")

    def restart(update, context):
        update.message.reply_text("Bot is restarting...")
        Thread(
            target=stop_and_restart,
            args=(update.message.from_user.first_name,)
        ).start()

    for handler in all_handlers:
        if len(handler) == 2:
            if handler[0] == "error":
                dp.add_error_handler(
                    handler[1]
                )
                pass
            else:
                dp.add_handler(
                    handler[0],
                    handler[1]
                )
        else:
            dp.add_handler(
                handler[0]
            )

    dp.add_handler(
        CommandHandler("r", restart, filters=Filters.user(SUDO_USERS))
    )

    updater.start_polling(clean=True)
    updater.idle()
