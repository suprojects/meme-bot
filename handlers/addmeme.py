from telegram.ext import CommandHandler, Filters
from secrets import SUDO_USERS
from helpers.templates import template

def new(update, context):
    msg = update.message

    if msg.text == '/addmeme':
        msg.reply_text('WTF Brah? WDYM? Which template to add 🤦‍♂️? Noob 😑.')
        return

    RawText = msg.text.replace('/addmeme ', '')

    RawNewMemeTemplate = RawText.split()[0]

    NewMemeTemplate = RawNewMemeTemplate.split(',')
    
    if len(NewMemeTemplate) != 4:
        msg.reply_text(f'''
Are you noob? Give me <code>4</code> params separated by a comma. You gave me <code>{len(NewMemeTemplate)}</code>. What am I to do with this?\n
<code>Shortname</code>, <code>Meme ID</code>, <code>Number of Boxes</code>, <code>Example Meme</code>''', parse_mode = 'HTML')
        return

    msg.reply_text(f'''

Adding new meme to template:

Shortname: <code>{NewMemeTemplate[0]}</code>
Meme ID: <code>{NewMemeTemplate[1]}</code>
Number of fields: <code>{NewMemeTemplate[2]}</code>
Example meme: <code>{NewMemeTemplate[3]}</code>

''', parse_mode = 'HTML')
    
    template[NewMemeTemplate[0]] = {'id': NewMemeTemplate[1], 'texts': NewMemeTemplate[2], 'help': NewMemeTemplate[3]}

    NewFileData = f'template = {template}'

    OldFile = open('helpers/templates.py', 'w')
    OldFile.write(NewFileData)
    OldFile.close()

__handlers__ = [
    [CommandHandler("addmeme", callback = new, filters=Filters.user(SUDO_USERS), run_async=True)],
]
