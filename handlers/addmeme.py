from telegram.ext import CommandHandler, Filters
from secrets import SUDO_USERS
from utils.templates import template
from utils.make import make

def new(update, context):
    msg = update.message

    if msg.text == '/addmeme':
        msg.reply_text('WTF Brah? WDYM? Which template to add 🤦‍♂️? Noob 😑.')
        return

    RawText = msg.text.replace('/addmeme ', '')

    RawNewMemeTemplate = RawText.split()[0]

    NewMemeTemplate = RawNewMemeTemplate.split(',')
    
    if len(NewMemeTemplate) != 3:
        msg.reply_text(f'''
Are you noob? Give me <code>3</code> params separated by a comma. You gave me <code>{len(NewMemeTemplate)}</code>. What am I to do with this?\n
<code>Shortname</code>, <code>Meme ID</code>, <code>Number of Boxes</code>''', parse_mode = 'HTML')
        return

    msg.reply_text(f'''

Adding new meme template:

Shortname: <code>{NewMemeTemplate[0]}</code>
Meme ID: <code>{NewMemeTemplate[1]}</code>
Number of fields: <code>{NewMemeTemplate[2]}</code>

''', parse_mode = 'HTML')
    
    texts = (", ".join(["text" + str(i) for i in range(1, int(NewMemeTemplate[2]) + 1)])).split(',')

    sentphoto = update.message.reply_photo(make(NewMemeTemplate[1], texts))

    template[NewMemeTemplate[0]] = {'id': NewMemeTemplate[1], 'texts': NewMemeTemplate[2], 'help': sentphoto.photo[0].file_id}

    NewFileData = f'template = {template}'

    OldFile = open('utils/templates.py', 'w')
    OldFile.write(NewFileData)
    OldFile.close()

def remove(update, context):
    msg = update.message

    RawText = msg.text.replace('/rmmeme ', '')
    RmMemeTemplate = RawText.split()[0]

    template.pop(RmMemeTemplate)

    NewFileData = f'template = {template}'

    OldFile = open('utils/templates.py', 'w')
    OldFile.write(NewFileData)
    OldFile.close()

def install(update, context):
    update.message.reply_to_message.document.get_file().download(custom_path = 'utils/templates.py')

    import sys
    import os
    os.execv(sys.executable, ['python'] + sys.argv)
    

__handlers__ = [
    [CommandHandler("addmeme", callback = new, filters=Filters.user(SUDO_USERS), run_async=True)],
    [CommandHandler("rmmeme", callback = remove, filters=Filters.user(SUDO_USERS), run_async=True)],
    [CommandHandler("install", callback = install, filters=Filters.user(SUDO_USERS) & Filters.reply, run_async=True)],
]
    