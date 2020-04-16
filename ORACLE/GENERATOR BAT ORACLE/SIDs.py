# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 10:57:12 2016

@author: MHolod

Module rewrite SIDs in file 
"""

import os
import sys



def analyze():
    """
        Function find tnsnames.ora and take dictionary
    """
    
    x = ''
    
    # fined tnsnames
    l_files = os.listdir()
    for i in range(len(l_files)):
        l_file = l_files[i].lower()
        if l_file.startswith("tnsnames.ora"):
            x = l_files[i]
            break
    if not x:
        print("Can't find tnsnames.ora")
        sys.exit()
    f = open(x, 'r')
    #l_ora = list()
    
    # read tnsnames
    d = dict()
    lines = f.readlines()
    l_symb = ['#', ' ', ')', '\n']
    desc = ''             ## description of SID
    prev = ''             ## previous SID
    for line in lines:
            
        if not line[0] in l_symb:
            if not prev == '':
                d[prev] = desc
            prev = line.split(' ')[0]
            desc = ''
        else:
            desc = desc + line
   # l_ora.sort()
    f.close()
    return x, d

def analyze_from_ini(tns_path):
    """
        Function find tnsnames.ora and take dictionary
        take path of tnsnames.ora file
        return list of SIDs
    """
    
    f = open(tns_path, 'r')
    #l_ora = list()
    
    # read tnsnames
    d = dict()
    lines = f.readlines()
    l_symb = ['#', ' ', ')', '\n']
    desc = ''             ## description of SID
    prev = ''             ## previous SID
    for line in lines:
            
        if not line[0] in l_symb:
            if not prev == '':
                d[prev] = desc
            prev = line.split(' ')[0]
            desc = ''
        else:
            desc = desc + line
   # l_ora.sort()
    f.close()
    return list(d.keys())

def analyze_from_ini_dict(tns_path):
    """
        Function find tnsnames.ora and take dictionary
        take path of tnsnames.ora file
        return dictionary of SIDs
    """
    
    f = open(tns_path, 'r')
    #l_ora = list()
    
    # read tnsnames
    d = dict()
    lines = f.readlines()
    l_symb = ['#', ' ', ')', '\n']
    desc = ''             ## description of SID
    prev = ''             ## previous SID
    for line in lines:
            
        if not line[0] in l_symb:
            if not prev == '':
                d[prev] = desc
            prev = line.split(' ')[0]
            desc = ''
        else:
            desc = desc + line
   # l_ora.sort()
    f.close()
    return d
    
    
def d_sort(f_name, d):
    """
        Function take dictionary of SIDs from tnsnames.ora and sort them   
    """
#    d_res = dict()
    l = list(d.keys())
#    l = list()
    
# upper registr of SIDs    
#    for i in range(len(l_from_dict)):
#        l.append(l_from_dict[i].upper())
        
    l.sort()
#    for i in range(len(l)):
#        d_res[l[i]] = d[l[i]]
#    input()
    
    # rewrite file
    f = open(f_name, 'w')
    for i in range(len(l)):
        header = l[i].upper() + ' = \n'
        f.write(header)
        f.write(d[l[i]])   
    f.close()
    
#    return d_res
        

def write_tns(f_name, d):
    """
        Function rewrite tnsnames.ora file of sorted files
        take name of tnsnames.ora file and dictionary of SIDs
    """
    f = open(f_name, 'w')
    for k, v in d.items():
        header = k + ' = \n'
        f.write(header)
        f.write(v + '\n')   
    f.close()


def find_tns_from_options():
    """
        Function find tnsnames.ora path from options.ini
        searching the type of OS
    """
    try:
        f = open('options.ini', 'r')
    except:
        print("Can't find file options.ini")
        sys.exit()
    while True:
        tns_line = f.readline()
        os_name = os.uname()[0]
        tns_name = tns_line.split('=')
        os_name_option = tns_name[0].split('_')[1]
        if  os_name_option == os_name:
            return tns_line.split('=')[-1]
            break

def walk_cycle():
    """
        Function walk of rewrite
    """
    tns_file = find_tns_from_options()
    d = analyze_from_ini_dict(tns_file)
    d_sort(tns_file, d)    

def init_cycle():
    """
        Function initialization of cycle
    """
    walk_cycle()
    walk_cycle()                    # twice cause can be SIDs in lower register

if __name__ == '__main__':
    init_cycle()
