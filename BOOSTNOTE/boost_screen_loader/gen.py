# coding: utf-8

"""
    Generator of boost-notes for pile of screens
"""

import json
import os
import shutil
import time
import glob


boost_dir = ''
attach_dir = boost_dir + 'attachments\\'
screen_dir = boost_dir + 'screens\\'
folder_name = '__SERT_MAIL.RU__'
name_dir = 'my_screen_dir'
note_dir = boost_dir + 'notes\\'
new_dir = attach_dir + name_dir
counter = 0



def gen_attachments():
    """
        Generate attachments
    """
    os.chdir(boost_dir)
    for screen in os.listdir(screen_dir):
        os.chdir(attach_dir)
        try:
            os.mkdir(name_dir)
        except:
            pass
        try:
            shutil.copy(screen_dir + screen, new_dir)
        except:
            pass
    os.chdir(boost_dir)

def gen_attach_dir(screen, dir_name):
    """
        Generate attach direction
    """
    os.chdir(attach_dir)
    new_dir = dir_name.rpartition('.')[0]
    try:
        os.mkdir(new_dir)
    except:
        pass
    try:
        shutil.copy(screen_dir + screen, new_dir + '\\' + screen)
    except:
        pass
    os.chdir(boost_dir)

def gen_name_note(screen_name):
    """
        Generate name of new note
    """
    name = screen_name.rpartition('.')[0]
    return name + '_' + str(time.time()).replace('.', '') + '.cson'

def gen_notes():
    """
        Generate notes
    """
    for screen in os.listdir(screen_dir):
        cson_name = gen_name_note(screen)
        note = get_note(screen, folder_name, cson_name)
        gen_attach_dir(screen, cson_name)
        with open(note_dir + os.sep + cson_name, 'w') as f:
            f.write(note)

def get_note(screen_name, folder_name, cson_name):
    """
        Get note by screen name
    """
    global counter
    counter = counter + 1
    note = ''
    cur_time = get_cur_time()
    folder_key = get_boost_key(folder_name)
    title_name = str(counter) + '_' + folder_name
    note = note + 'createdAt: "{0}"\n'.format(cur_time)
    note = note + 'updatedAt: "{0}"\n'.format(cur_time)
    note = note + 'type: "MARKDOWN_NOTE"\n'
    note = note + 'folder: "{0}"\n'.format(folder_key)
    note = note + 'title: "{0}"\n'.format(title_name)
    note = note + 'tags: []\n'
    note = note + "content: '''\n#### {0}\n![{1}](:storage\\\\{2}\\\\{1})\n'''\n".format(title_name, screen_name, cson_name.rpartition('.')[0])
    note = note + 'linesHighlighted: []\n'
    note = note + 'isStarred: false\n'
    note = note + 'isTrashed: false\n'
    return note

def get_boost_key(folder_name):
    """
        Get boost directory key by name
    """
    os.chdir(boost_dir)
    with open("boostnote.json", "r") as read_file:
        data = json.load(read_file)
    
    for folder in data['folders']:
        if folder['name'] == folder_name:
            return folder['key']


def get_cur_time():
    """
        Get time in format: yyyy-mm-ddThh:mi:ss.ms
        like: "2019-09-17T16:33:09.930Z"
    """
    t = time.localtime()
    if len(str(t.tm_mon)) == 1:
        s_month = '0' + str(t.tm_mon)
    else:
        s_month = str(t.tm_mon)
    return str(t.tm_year) + '-' + s_month + '-' + str(t.tm_mday) + 'T' + str(t.tm_hour) + ':' + str(t.tm_min) + ':' + str(t.tm_sec) + '.000Z'

def clean_dir(dir):
    files = glob.glob(dir)
    for f in files:
        os.remove(f)

def get_name_of_screen_folder(folder_name):
    return folder_name.split('_')[0] + '.jpg'

def dir_is_empty(dir):
    """
        Define if direction is empty
    """
    if len(os.listdir(dir)) == 0:
        return True
    else:
        return False


def return_screens():
    """
        IF screen absent - return from screen folder
    """
    for folder in [x for x in os.listdir(attach_dir) if x.find('_') > -1 and dir_is_empty(attach_dir + x)]:
        screen_name = get_name_of_screen_folder(folder)
        shutil.copy(screen_dir + screen_name, attach_dir + folder)

def main():
    """
        Main procedure
    """
    gen_attachments()
    os.chdir(boost_dir)

if __name__ == "__main__":
    main()
