# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 23:11:20 2016

@author: MHolod
"""

# In new versions:
#   use directory logs
#   generate file of mistakes
#   grouping invalides



import os
import os.path
#import datetime
import time


t_today = time.strftime("%H_%M_%S")                         # today date

ls = os.listdir()                               # list of log-files

l_logs = []              # list for logs

for i in range(len(ls)):
    if ls[i].endswith(".log") or ls[i].startswith("LOG_"):                       # if not py-script and txt-file
        l_logs.append(ls[i]) 
        
# print(l_logs)
        
        
f_analyze = open("progon_{0}".format(t_today), "wb")

for i in range(len(l_logs)):
    f_log = open(l_logs[i], "r")                    # open log-file
    
    # analyze name of file - cause output is bad
    ind_start = l_logs[i].index('Ext')
    ind_end = l_logs[i].index('.log')
    
    f_log_name = l_logs[i][ind_start:ind_end]
    print('-'*100)
    print(f_log_name)
    
    f_analyze.write(('-'*100).encode("utf-8"))
    f_analyze.write('\n'.encode("utf-8"))
    f_analyze.write(f_log_name.encode("utf-8"))
    
    # flag to print:
    f_print = False 
    
    # flags to define before and after
    f_before = True
    f_after = False
    # list of invals:
    l_invals_before = []
    l_invals_after = []
    while True:
        f_l = f_log.readline()
        
            
        # analyze date of progon
        if f_l.startswith('SQL*Plus: Release'):
            l_ind = f_l.index('Production')
            l_time_progon = f_l[l_ind:len(f_l)]
            print(l_time_progon.rstrip())
            f_analyze.write('\n'.encode("utf-8"))
            f_analyze.write(l_time_progon.encode("utf-8"))
            f_analyze.write('\n'.encode("utf-8"))
            continue
            
        # constraints:        
        if f_l.startswith('Регистрация'): continue
        if f_l.startswith('End'): continue
        if f_l.startswith('SGINV'): continue 
        if f_l.startswith('SVPLUGINSLOG'): continue
        if f_l.startswith('End'): continue           
        
        # before
        if f_l.startswith('Найдено инвалидов перед') and f_print == False:
            print('-'*50)
            print(f_l.rstrip())
            print('-'*50)
            
            f_analyze.write(('-'*50).encode("utf-8"))
            f_analyze.write('\n'.encode("utf-8"))
            f_analyze.write(f_l.encode("utf-8"))
            f_analyze.write(('-'*50).encode("utf-8"))
            f_analyze.write('\n'.encode("utf-8"))
            f_print = True
            continue
        if f_l.startswith('Begin'): 
            f_print = False            
            continue
        if f_print == True and not f_l == '\n' and not f_l.startswith('---'):
            print(f_l.rstrip())
            if f_before == True:
                l_invals_before.append(f_l.rstrip())
            else:
                l_invals_after.append(f_l.rstrip())
            continue
        
        
        # after
        if f_l.startswith('Найдено инвалидов после'):
            f_before = False
            # insert into analyze-file before list of invals
            for i in range(len(l_invals_before)):
                f_analyze.write(l_invals_before[i].encode("utf-8")) 
                f_analyze.write('\n'.encode("utf-8"))
            
            print('-'*50)
            print(f_l.rstrip())
            print('-'*50)
            
            f_analyze.write(('-'*50).encode("utf-8"))
            f_analyze.write('\n'.encode("utf-8"))
            f_analyze.write(f_l.encode("utf-8"))    
            f_analyze.write(('-'*50).encode("utf-8"))
            f_analyze.write('\n'.encode("utf-8"))
            f_print = True
            continue
        if f_l.startswith('End'): 
            f_print = False            
            continue

        if not f_l: 
            # insert into analyze-file before list of invals
            for i in range(len(l_invals_after)):
                f_analyze.write(l_invals_after[i].encode("utf-8"))
                f_analyze.write('\n'.encode("utf-8"))
            break
    print("\n")
    print(l_invals_before)
    print(l_invals_after)
    f_log.close()
    
    f_analyze.write('\n'.encode("utf-8"))

    # write to analyze-file
    

f_analyze.close()    
    