# -*- coding: utf-8 -*-

import cx_Oracle
import os
import re
import subprocess
import os.path

def exec_sql(cols, table, sql, d, d_val):
    """
    Generate script for insert data
    :param cols: list of columns
    :param table: name of table
    :param sql: sql-script
    :param d: direcotry
    :param d_val: directory of values
    :return: list of insert rows for script
    """
    l = list()          # result list
    con = cx_Oracle.connect('system/ora123@XE')
    cur = con.cursor()
    cur.execute(sql)
    for res in cur:
        res = list(res)
        ls = list()
        for i in range(len(res)):
            d_val[i] = str(res[i])
            ls.append(str(res[i]))
        res = ls
        val = treat_data(d, res, d_val)        # combine data
        sql_ins = gen_insert(cols, table, val)
        l.append(sql_ins)
        # print(sql_ins)
    cur.close()
    con.close()
    l_res = list()
    for j in range(len(l)):
        s = l[j]
        s = s.replace('None', 'Null')
        l_res.append(s)
    return l_res

def treat_data(d, ls, d_val):
    # dictionary[name_of_column] = data_type
    # ls = values of 1 row in order of dictionary
    res = list()        # result list
    i = 0               # iterator of list ls
    var = ''            # variable to add to result
    for j in range(len(ls)):
        if d[j][1] == 'NUMBER':
            var = "{0}".format(d_val[j])  # if it is a number - nothing to add
        elif d[j][1] == 'VARCHAR2':
            var = "'{0}'".format(d_val[j])       # if it is a string - add quotes
        elif d[j][1] == 'DATE':
            var = redo_date(d_val[j])          # if it's a date - treat in function
        elif d[j][0].find('ID'):
            var = "'{0}'".format(d_val[j])  # if contain 'ID'
        else:
            if d_val[j] == 'None':              # change to 'Null'
                var = 'Null'
            else:
              var = d_val[j].replace('None', 'Null')
        res.append(var)
        i = i + 1
    return ', '.join(res)


def redo_date(val):
    """
    Treat value of date type
    :param val: value of date string
    :return: treaten value of date type like TO_DATE('17-06-2003', 'dd-MM-yyyy')
    """
    ls = val.split('-')          # split as '-'

    dop = ls[2].split(' ')[0]
    res = ls[0] + '-' + ls[1] + '-' + dop
    n = len(ls[0])
    if n == 4:                  # if len of number of first member 4 then 'yyyy-MM-dd'
        ch = "TO_DATE('{0}', 'YYYY-MM-DD')".format(res)
        return ch
    else:
        ch = "TO_DATE('{0}', 'DD-MM-YYYY')".format(res)
        return ch


def take_col(table):
    """
    Take columns for chosen table
    :param table: name of table
    :return: dictionary name_of_column - data type
    :return: cols - string of columns separated by ,
    """
    l = list()
    d = dict()
    d_val = dict()
    l_v = list()
    con = cx_Oracle.connect('system/ora123@XE')
    cur = con.cursor()
    # cur.execute("select column_name from USER_TAB_COLUMNS utc where utc.TABLE_NAME = upper('employees')")

    cur.execute("""
                  select utc.column_name
                        , utc.data_type
                  from USER_TAB_COLUMNS utc
                  where utc.TABLE_NAME = upper('{0}')""".format(table))
    i = 0
    for result in cur:
        l_k = list()
        l.append(result[0])
        l_k.append(result[0])
        l_k.append(result[1])
        d[i] = l_k
        l_v.append(i)
        i = i + 1

    cur.close()
    con.close()
    d_val.fromkeys(l_v)
    return ', '.join(l), d, d_val

def gen_insert(cols, table, val):
    ins = '(' + cols + ')'
    sql = """INSERT INTO {0}{1} VALUES ({2});""".format(table, ins, val)
    return sql

def gen_sel(cols, table):
    sql = """SELECT {0} FROM {1}""".format(cols, table)
    return sql

def take_tables(table_name):
    """

    :param table_name:
    :return:
    """
    l = list()          # list of result tables
    con = cx_Oracle.connect('system/ora123@XE')
    cur = con.cursor()
    cur.execute("""
                    Select distinct col.TABLE_NAME
                    From all_constraints ac,
                         All_Cons_Columns col,
                         all_cons_columns mine
                    Where ac.TABLE_NAME = Upper('{0}')
                          And ac.r_CONSTRAINT_NAME = col.CONSTRAINT_NAME
                          And ac.CONSTRAINT_NAME = mine.CONSTRAINT_NAME
    """.format(table_name))
    for res in cur:
        l.append(res[0])
    cur.close()
    con.close()
    return l

def take_ora_path_re():
    """
    Take path of oracle
    :return:
    """
    ls = os.environ['PATH'].split(r';')
    for i in range(len(ls)):
        l_new = ls[i].split(r'\\')
        for j in range(len(l_new)):
            if re.findall(r'ora\w+', l_new[j]):
                return ls[i]

def find_tnsnames_ora():
    """
    Find abspath tnsnames.ora
    :return:
    """
    path = take_ora_path_re()
    subprocess.call('cd {0}'.format(path), shell = True)            # change directory

    # find grandfather of current direcotry
    ls = path.split('\\')
    l = ls[:-3]
    res_path = '\\'.join(l)
    # print(os.path.abspath(os.curdir))) ->  C:\oraclexe\app\oracle\product

    os.chdir(res_path)      # change current directory to grandfather

    # find tnsnames.ora
    l_res = list()
    out = subprocess.check_output('dir /b /s *tns*.*', shell = True)
    out_list = out.split('\r\n')
    for i in range(len(out_list)):
        l_each = out_list[i].split('\\')            # split each path of file
        # if last element is tnsnames.ora -> take him

        try:
            s_sample = l_each[-2].upper()
            if s_sample == 'SAMPLE':                # of it is just example - continue
                continue
        except:
            pass
        for k in range(len(l_each)):
            tns_val = l_each[-1]        # name of file with extension
            l_tns = tns_val.split('.')
            first_arg = l_tns[0]
            second_arg = l_tns[-1]
            if first_arg.upper() == 'TNSNAMES' and second_arg.upper() == 'ORA':
                l_res.append(out_list[i])
    set_l_res = set(l_res)
    l_res = list(set_l_res)
    return l_res

