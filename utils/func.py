from utils.templates import template
from telegram import InlineKeyboardButton

def maketexts(textcount):

    texts = str(", ".join(["text" + str(i) for i in range(1, int(textcount) + 1)]))

    return texts

def btns(pages):

    a, i = int(0), int(0)
    keyboard, btnpage, btnrow = [], [], []

    for eachtempl in template:
        
        if a < pages:
            if i < 3:
                i += 1
                btnrow.append(InlineKeyboardButton(text = eachtempl, callback_data = f'templ_{eachtempl}'))
        
            else:
                btnpage.append(btnrow[:])
                btnrow.clear()
        
                i = 1
                btnrow.append(InlineKeyboardButton(text = eachtempl, callback_data = f'templ_{eachtempl}'))
                
                a += 1
            
        else:
            a = 0
            keyboard.append(btnpage[:])
            btnpage.clear()
            
            i += 1
            btnrow.append(InlineKeyboardButton(text = eachtempl, callback_data = f'templ_{eachtempl}'))       
    keyboard.append(btnpage)

    return keyboard


emotes = {
    1 : '1️⃣',
    2 : '2️⃣',
    3 : '3️⃣',
    4 : '4️⃣',
    5 : '5️⃣',
    6 : '6️⃣',
    7 : '7️⃣',
    8 : '8️⃣',
    9 : '9️⃣',
}

def navbtn(page, length):
    return [
        InlineKeyboardButton(text = '◀️', callback_data = f'page_{page - 1}'),
        InlineKeyboardButton(text = f'{emotes.get(int(page))} of {emotes.get(int(length))}', callback_data = f'currpage_{page}'),
        InlineKeyboardButton(text = '▶️', callback_data = f'page_{page + 1}'),
    ]