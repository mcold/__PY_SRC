# -*- coding: utf-8 -*-

import m_useful_v2
import m_Oracle_v2

"""
    Main module of program
    Generate data from DB with input user's name of table 
    Useful just for Python ver. 2
"""

def input_data():
    """
    Input connect data to DB
    :return:
    """
    login = m_useful_v2.input_var('login', 'system')
    password = m_useful_v2.input_var('password', 'ora123')
    SID = m_useful_v2.input_var('SID', 'XE')
    table = m_useful_v2.input_var('table', 'employees')
    return login, password, SID, table

def cr_directories():
    """
    Create directories
    :param func: function
    :return: execute function
    """
    m_useful_v2.cr_dir('options')
    m_useful_v2.cr_dir('output')


def write_preins_string(table, res_table_script_name):
    """
    print into insert script string about table
    :param table: table name
    :param res_table_script_name: name of result table insert script
    :return: None
    """
    f = open("output\INS_{0}.sql".format(res_table_script_name), "ab")  # open file for write
    s_string = "\n-- INSERT DATA INTO TABLE {0}\n\n".format(table.upper())
    f.write(s_string.encode("utf-8"))
    f.close()


@m_useful_v2.clear_screen
def gen_script(table_name, l_ins, res_table_script_name):
    f = open("output\INS_{0}.sql".format(table_name), "ab")  # open file for write
    for i in range(len(l_ins)):
        f.write(l_ins[i].encode("utf-8"))
        f.write('\n'.encode("utf-8"))
    f.close()

def cycle_gen_ins_script(login , password, SID, table, res_table_script_name):
    ### create directories
    cr_directories()

    cols, d, d_val = m_Oracle_v2.take_col(table)
    sql = m_Oracle_v2.gen_sel(cols, table)
    ls = list()
    ls = m_Oracle_v2.exec_sql(cols, table, sql, d, d_val)
    gen_script(res_table_script_name, ls, res_table_script_name)

def gen_script_rel_tables(login, password, SID, table):
    """
    Execute generation of insert-scripts into insert sql script for tables reliable to current
    :param table: table name
    :return: None
    """
    l_tables = m_Oracle_v2.take_tables(table)   ### take list of reliable tables
    cr_directories()
    try:
        f = open("output\INS_{0}.sql".format(table), "ab")  # open file for append
    except:
        f = open("output\INS_{0}.sql".format(table), "wb")  # open file for append
    for i in range(len(l_tables)):
        if not l_tables[i].upper() == table.upper():
            write_preins_string(l_tables[i], table)  ### write prelude of table
            cycle_gen_ins_script(login, password, SID, l_tables[i], table)
    f.close()
    return l_tables

def gen_data():
    """
    Generate data for table
    :return: file of script
    """
    login, password, SID, table = input_data() ### take data for connect
    l_tables = gen_script_rel_tables(login, password, SID, table)  ### gen insert data of reliable tables
    write_preins_string(table, table)         ### write prelude for main table
    ### if table not in l_tables:       ### if table not in list of reliable tables
    cycle_gen_ins_script(login, password, SID, table, table)    ### gen insert data of table

def cycle_gen_data():
    """
    Execute cycle of generation of scripts with data
    :return:
    """
    while True:
        gen_data()
        m_useful_v2.ch_continue()


if __name__ == '__main__':
    cycle_gen_data()






