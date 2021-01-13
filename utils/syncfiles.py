from shutil import copyfile
from secrets import TEMPLATES_DIR
from os import remove

def sync():
    open(f'{TEMPLATES_DIR}/templates.py', 'w').close()
    copyfile("utils/templates.py", f'{TEMPLATES_DIR}/templates.py')