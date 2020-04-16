# -*- coding: utf-8 -*-


import os
import os.path
import subprocess



file = 'boostnote.json'
dirs = {
    'java': '/home/mcold/Dropbox/boosts/java boosts/notes',
    'linux': '/home/mcold/Dropbox/boosts/linux boosts/notes',
    'oracle': '/home/mcold/Dropbox/boosts/oracle boosts/notes',
    'postgres': '/home/mcold/Dropbox/boosts/postgres boosts/notes',
    'python': '/home/mcold/Dropbox/boosts/python boosts/notes',
    'sqlite': '/home/mcold/Dropbox/boosts/sqlite boosts/notes',
    'svn': '/home/mcold/Dropbox/boosts/svn boosts/notes',
    'work': '/home/mcold/Dropbox/boosts/work boosts/notes',
    'useful': '/home/mcold/Dropbox/boosts/useful boosts/notes'
}

def take_file_dir(d_dir):
    """
    Function take names of files with snippets from directories
    :return:
    """
    ls = os.listdir(path=d_dir)
    l_snips = list()
    for i in range(len(ls)):
        if ls[i].endswith(".cson"):
            l_snips.append(ls[i])
    return l_snips

def take_files():
    """
    Take file .json
    :return: list of snippets
    """
    ls = os.listdir()
    l_snips = list()
    for i in range(len(ls)):
        if ls[i].endswith(".json"):
            l_snips.append(ls[i])
    return l_snips

def take_snips(file):
    """
    Function return
    :param l_snips:
    :return: headers of snips
    """
    d = dict()
    try:
        f = open(file, "r")
        bStart = False
        val = ''
        while True:
            line = f.readline()
            # line = line.strip()
            if line.startswith('    {'):
                continue
            if line.startswith('    }'):
                continue
            if bStart == True:
                val = val + line
            if split_str_1(line) == 'folders':
                bStart = True

            if split_str_1(line) == 'name':
                k = split_str_2(line)
                d[k] = val
                val = ''
            if line == '':
                break
        f.close()
        return d
    except:
        pass
    return d



def split_str_2(line):
    """
    Take second element of split from string with type:'       "name": "Programs py"'
    :param line:
    :return:
    """
    l = line.split(':')
    ll = l[1].strip()
    name = ll[1:-1]
    return name

def split_str_1(line):
    """
    Take second element of split from string with type:'       "name": "Programs py"'
    :param line:
    :return:
    """
    l = line.split(':')
    ll = l[0].strip()
    name = ll[1:-1]
    return name



## Сортировка и запись
def sort_write(d, file):
    l = list()
    for k in d:
        l.append(k)
    l.sort()
    try:
        f = open(file, "wb")
        f.write('{\n'.encode("utf-8"))
        f.write('  "folders": [\n'.encode("utf-8"))
        for i in range(len(l)):
            f.write('    {\n'.encode("utf-8"))
            f.write(d[l[i]].encode("utf-8"))
            if not i == len(l)-1:
                f.write('    },\n'.encode("utf-8"))
            else:
                f.write('    }\n'.encode("utf-8"))
        f.write('  ],\n'.encode("utf-8"))
        f.write('  "version": "1.0"\n'.encode("utf-8"))
        f.write('}'.encode("utf-8"))
        f.close()
    except:
        pass

def cycle():
    for i in dirs:
        subprocess.call('cd "{0}"'.format(dirs[i]), shell=True)
        d = take_snips('{0}/boostnote.json'.format(dirs[i]))
        sort_write(d, '{0}/boostnote.json'.format(dirs[i]))

if __name__ == '__main__':
    d = take_snips(file)
    sort_write(d, file)