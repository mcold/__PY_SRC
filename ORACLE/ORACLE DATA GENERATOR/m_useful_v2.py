# -*- coding: utf-8 -*-

import os
import sys

"""
    Useful just for Python ver. 2
"""

def cls_screen():
    """
        Function clear sceen in depend of OS
    """
    os.system('cls')

def clear_screen(func):
    """
        Clear sceen in depend of OS
    """
    def wrapper():
        if os.uname()[0] == 'Linux':
            os.system('clear')
        if os.uname()[0] == 'Windows':
            os.system('cls')
        func()
    return func


# @clear_screen
def input_var(var_name, def_val):
    cls_screen()
    """
    Input user value of variable
    :param var_name: nameo of var
    :param def_var: default value
    :return:
    """
    res = str(raw_input("Enter {0} (default = {1}): ".format(var_name, def_val)))
    if res in (None, '', '\n'):             # if nothing return default value
        res = def_val
    return res

def cr_dir(dirname):
    """
        Function create directory "logs"
    """
    if not os.path.exists("{0}".format(dirname)):
        os.mkdir("{0}".format(dirname))

# @clear_screen
def ch_continue():
    """
        Function define to continue for user in any cycle
    """
    cls_screen()
    x = raw_input('\n\tDo you want to continue?(y or n) ')
    if x.startswith('y') or x.startswith('Y') or x == '':
        print()
    else:
        sys.exit()


if __name__ == "__main__":
        ### Tests
    # test_func_print()
    print(input_var('my_var', 111))