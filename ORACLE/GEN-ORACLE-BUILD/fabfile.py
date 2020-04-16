# coding: utf-8


# coding: utf-8

"""
   Build's generator
"""

from fabric.api import task
from os import getcwd, listdir, chdir
from os.path import isdir, sep, basename, dirname
import sys

cur_dir = getcwd()

l_not_use = ['SQLsystem', 'Log', 'Metka', 'Jobs', 'Java', 'Owner', 'Package', 'Procedure']
l_not_use_obj = ['INSTALL.SQL', 'UNINSTALL.SQL']

# fullfill in process of generation
l_inst_obj = []

@task
def gen_build(src_dir:src_dir):
	"""
		Generate build install/uninstall
	"""
	s_in = 'INSTALL'
	s_un = 'UNINSTALL'

	for obj in listdir(src_dir):
		obj_path = src_dir + sep + obj
		if isdir(obj_path) and obj not in l_not_use:
			# gen installs.sql
			try:
				inst_path = obj_path + sep + s_in
				chdir(inst_path)
				gen_script(inst_path, s_in)
			except:
				pass
			chdir(src_dir)

			# gen uninstall.sql
			try:
				uninst_path = obj_path + sep + s_un
				chdir(uninst_path)
				gen_script(uninst_path, s_un)
			except:
				pass

			chdir(src_dir)

def gen_script(dir, name):
	"""
		Generate install.sql
	"""
	base_dir = basename(dirname(dir))
	with open('{}.SQL'.format(name), 'w') as f:
		f.write(r'SPOOL .\LOG\{}\{}.LOG'.format(name, base_dir))
		f.write('\n\n')
		f.write('SET DEFINE OFF\n\n')
		for obj in listdir(dir):
			if obj.upper() not in l_not_use_obj:
				f.write('prompt \n')
				f.write('prompt \n')
				f.write('prompt ' + '='*30 + '\n')
				f.write('prompt \n')
				f.write('@@{}\n\n'.format(obj))

				l_inst_obj.append(base_dir)
		f.write('SET DEFINE ON\n\n')
		f.write('SPOOL OFF')

def gen_inst_bat()
	"""
		Generate install.bat
	"""
	with open('install.bat', 'w') as f:
		f.write('--Запускаем инициализацию параметров\n')
		f.write('@CONFIG.INI;\n\n\n')

		### TODO: block must be if we have system or rules changes 
		f.write('-'*66 + '\n')
		f.write('--Выдача прав\n')
		f.write('-'*66 + '\n\n\n')
		f.write('--Подключение к БД\n')
		f.write('CONNECT &USR_SYS/&PWD_SYS@&SID AS SYSDBA;\n\n')
		f.write('--Запоминаем переменные окружения\n')
		f.write('STORE SET TO_INSTALL_PARAM.SQL REPLACE;\n\n')
		f.write('--Устанавливаем параметр\n')
		f.write('@TO_INSTALL_PARAM.SQL;\n\n')
		f.write('--Выдача прав пользователю\n')
		f.write(r'@.\Owner\INSTALL\INSTALL.SQL;')
		f.write('\n\n')
		f.write('--Отключение\n')
		f.write('DISCONNECT;\n\n')
		f.write()
		f.write()


def gen_uninst_bat()
	"""
		Generate uninstall.bat
	"""
	with open('uninstall.bat', 'w') as f:
		f.write()

def clean_build():
	
	pass