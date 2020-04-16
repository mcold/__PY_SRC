# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 13:37:24 2016

@author: MHolod

generate bat file in order which you choice
"""

## filter just on extension with .bts and releases          -- now just not .py and .txt
## add possibility on sys progon
## choose from service names
## choose only from list
## choose big or small BTK/btk

import os
import os.path
import sys
#import datetime
import time
import SIDs


t_today = time.strftime("%H_%M_%S")                         # today date



ls = os.listdir(os.path.abspath(os.curdir))                               # list of files
ext = ".cmd"                                    # extension for result file
#name_file = "progon"                            # zero name of file
d = dict()                                      # in this dictionary write names of files

# Example:
# sqlplus "BTK/BTK@GlobalDBMain" @.bts >> LOG_.log

def clear_screen():
    """
        Function clear sceen in depend of OS
    """
    if os.uname()[0] == 'Linux':
        os.system('clear')
    if os.uname()[0] == 'Windows':
        clear_screen()

def ins_db():
    clear_screen()
    DB_name = str(input("Name of DataBase: "))

    while DB_name == None:                                                      # check name of DataBase
        DB_name = str(input("Enter correct name of DataBase: "))
    return DB_name
    
def ch_elem_ls_name(ls, name_elem):
    """
        Function user choose element from list
        take list and name of element
    """
    clear_screen()                           # clear screen  
    l_i = [] 
    d = dict()
    for i, j in enumerate(ls):                  # enumeration output values
            print('\t' + str(i) +" " +  str(j))
            print('\n')
            l_i.append(i)
            d[i] = j
    while True:
        try:
            u_ch = input('\n\tChoose number of %s: ' % name_elem)
            try:
                u_ch = int(u_ch)
                if u_ch in l_i:
                    return d[u_ch]
            except:
                if u_ch == 'exit' or u_ch == 'quit':
                    sys.exit()
                else:
                    try:
                        for i in range(len(ls)):
                            str_elem = ls[i].lower()
                            u_ch_low = u_ch.lower()
                            if str_elem.startswith(u_ch_low):
                                return ls[i]
                    except:
                        ch_elem_ls_name(ls, name_elem())
        except:
            pass

def ch_db_tns():
    """
        Function choose SID from tnsnames.ora
    """
    tns_file = SIDs.find_tns_from_options()         # take path of tnsnames.ora
    l = SIDs.analyze_from_ini(tns_file)             # take list of SIDs from tnsnames.ora
    DB_name = ch_elem_ls_name(l, 'SID')
    return DB_name




def case_BTK():
    clear_screen()
    try:
        user = input("Print user-name (default 'btk')")
    except:
        user = 'btk'
        return user

def ins_scr_name():
    clear_screen()   
    try:
        script_name = str(input("Name for bat-file (default 'progon'): "))
        return script_name
    except:
        script_name = 'progon'
        return script_name
    
def l_files():
    l_scripts = []              # list for scripts

    for i in range(len(ls)):
        if not ls[i].split('.')[-1].lower() in ('py', 'txt', 'cmd', 'bat', 'ora', 'ini') and not ls[i] in ('logs', '__pycache__'):
            l_scripts.append(ls[i])
#        if not ls[i].endswith(".py") and not ls[i].endswith(".txt") and not ls[i].endswith(".cmd") and not ls[i].endswith(".bat") and not ls[i] in ('logs', '__pycache__')  and not ls[i].endswith(".ini"):                       # if not py-script and txt-file
#            l_scripts.append(ls[i])                                                         # take just files that need in different list
    return l_scripts
    

def cr_dir_log():
    """
        Function create directory "logs"
    """
    if not os.path.exists("logs"):
        os.mkdir("logs")
        
def cycle(l_scripts, script_name, DB_name, user, f):
    """
        Function is cycle of print scripts and output 1 record to bat-file
    """
    clear_screen()
    for i in range(len(l_scripts)):
        d[i] = l_scripts[i]
    #f = open("{0}{1}".format(script_name, ext), "wb")              # open file for write
    for k, v in d.items():
        print(str(k) + " " + v)
    print("\nEnter number of file: (to exit - print quit) \n")
    try:    
        n_l = input()
        if n_l == 'quit':
            clear_screen()
        while d.get(int(n_l)) == None:
            print("\nEnter number of file: (to exit - print quit) \n")
            n_l = input()
        l_num = d.pop(int(n_l))
        #l_split = l_num.split(".")
        #l_num = "sqlplus " + '\"' + user + "/" + user + "@" + DB_name + '\"' + " "  + "@" + l_split[0] + "_" + t_today + "." + l_split[-1] + ">> logs\LOG_" + l_split[0] + ".log"
        l_num = "sqlplus " + '\"' + user + "/" + user + "@" + DB_name + '\"' + " "  + "@" + l_num + " >> logs\LOG_" + l_num + ".log"
        l_num = l_num + "\n"
        f.write(l_num.encode("utf-8"))
    except:
        f.close() 
        sys.exit()
    #f.close()
    ls = list()
    for k in d.keys():
        ls.append(d[k])
    cycle(ls, script_name, DB_name, user, f)
    
    
    

def gen_bat(l_scripts, script_name, DB_name, user):
    clear_screen()
    for i in range(len(l_scripts)):
        d[i] = l_scripts[i]

    l_dict = d.__len__()

    f = open("{0}{1}".format(script_name, ext), "wb")              # open file for write
    
    for k, v in d.items():
        print(str(k) + " " + v)
 
    while l_dict:
        print("\n")
        for k, v in iter(d.items()):
            print(str(k) + " " + v)
            try:    
                print("\nEnter number of file: (to exit - print quit)\n")
                n_l = (input())
                if not n_l.isdigit():
                    sys.exit()
                if n_l == 'quit':
                    sys.exit()
                if n_l.startswith('quit'):
                    sys.exit()    
                l_num = d.pop(int(n_l))
    
                l_split = l_num.split(".")     
    
                l_num = "sqlplus " + '\"' + user + "/" + user + "@" + DB_name + '\"' + " "  + "@" + l_split[0] + "_" + t_today + "." + l_split[-1] + ">> logs\LOG_" + l_split[0] + ".log"
                l_num = l_num + "\n"
                f.write(l_num.encode("utf-8"))
                l_dict = l_dict - 1
                
            except:
                f.close() 
                sys.exit()
                continue
        print("\n")
    
    f.close()
    
    

if __name__ == '__main__':
    cr_dir_log()             # create directory
    DB_name = ch_db_tns()
    script_name = ins_scr_name()
    user = case_BTK()
    l_scripts = l_files()
    f = open("{0}{1}".format(script_name, ext), "wb")              # open file for write
    cycle(l_scripts, script_name, DB_name, user, f)
    f.close()
     