# coding: utf-8


import os
import re
import shutil
from fabric.api import local

try:
    # Py2
    import simpleyaml as yaml
    prj_name = '{name}.jms'.format(name=str(raw_input('Enter masher name: ')))
except:
    # Py3
    import yaml
    prj_name = '{name}.jms'.format(name=str(input('Enter masher name: ')))

d_opt = yaml.load(open('options.yaml'))
cur_dir = os.getcwd()
src_dir = d_opt['gen']['src_dir'] if d_opt['gen']['src_dir'].find(':') > -1 else os.getcwd() + '\\' + d_opt['gen']['src_dir'].rstrip('\\') + '\\'
jcl_dir = d_opt['gen']['jcl_dir'] if d_opt['gen']['jcl_dir'].find(':') > -1 else os.getcwd() + '\\' + d_opt['gen']['jcl_dir'].rstrip('\\') + '\\'
out_dir = d_opt['gen']['out_dir'] if d_opt['gen']['out_dir'].find(':') > -1 else os.getcwd() + '\\' + d_opt['gen']['out_dir'].rstrip('\\') + '\\'

############ decorators ###############

def exe_jcl(f):
    """
        Decorator for execute into 1 git-directory
    """
    
    def wrapper(*args, **kwargs):

        def_dir = os.getcwd()

        shutil.copy(cur_dir + r'\xml\start_jcl.xml', src_dir)
        shutil.copy(cur_dir + r'\xml\end_jcl.xml', src_dir)
        shutil.copy(cur_dir + r'\xml\question.xml', src_dir)

        os.chdir(src_dir)
        f(*args, **kwargs)

        path = os.path.abspath(os.path.dirname(__file__))
        os.chdir(path)

        os.remove(src_dir + '\\start_jcl.xml')
        os.remove(src_dir + '\\end_jcl.xml')
        os.remove(src_dir + '\\question.xml')

        os.chdir(def_dir)

    return wrapper

def exe_jms(f):
    """
        Decorator for execute into 1 git-directory
    """
    
    def wrapper(*args, **kwargs):
        
        # copy xml-files for project
        shutil.copy(r'xml\start_prj.xml', jcl_dir)
        shutil.copy(r'xml\end_prj.xml', jcl_dir)
        shutil.copy(r'xml\hotpot_prj.xml', jcl_dir)
        

        os.chdir(jcl_dir)
        f(*args, **kwargs)

        path = os.path.abspath(os.path.dirname(__file__))
        os.chdir(path)

        os.remove(jcl_dir + '\\start_prj.xml')
        os.remove(jcl_dir + '\\end_prj.xml')
        os.remove(jcl_dir + '\\hotpot_prj.xml')

    return wrapper

############ end decorators ###############

@exe_jcl
def gen_jcl():
    """
        Generate jcl-files by src-files
    """
    l_files = [x for x in os.listdir('.') if x.rpartition('.')[-1].lower() in d_opt['jcl']['extension']]
    path = os.getcwd()

    for i in range(len(l_files)):
        with open(l_files[i], 'r') as f:
            # get result file
            name = l_files[i].rpartition('.')[0]
            l_comments = get_com_list(l_files[i].rpartition('.')[-1])
            lines = get_jcl(f.read(), name, l_comments)
            write_jcl(l_files[i].rpartition('.')[0] + '.jcl', lines)
    os.chdir(path)
    

def write_jcl(file_name, code):
    """
        Write result jcl
    """
    path = os.getcwd()
    os.chdir(jcl_dir)
    with open(file_name, 'w') as f:
            f.write(code)
    os.chdir(path)

def get_jcl(code, name, l_comments):
    res = ''
    with open('start_jcl.xml', 'r') as f:
        content = f.read()
        cur_title = re.findall(r'<title>.*</title>', content)[0]
        content = content.replace(cur_title, '<title>{0}</title>'.format(name))
        cur_dc_title = re.findall(r'<dc:title>.*</dc:title>', content)[0]
        content = content.replace(cur_dc_title, '<dc:title>{0}</dc:title>'.format(name))
        res = res + content

        # add questions
        code = add_questions(code, l_comments)

    res = res + code.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;').replace('    ', '&nbsp;&nbsp;&nbsp;&nbsp;')
    with open('end_jcl.xml', 'r') as f:
        res = res + f.read()
    return res

def add_questions(code, l_com):
    """
        Add question
    """
    res = ''

    # TODO: if not line start with comment
    l_lines = code.split('\n')
    for i in range(len(l_lines)):
        line = l_lines[i]
        
        for x in range(len(l_com)):
            com = l_com[x]
            if line.find(com) > 0:
                l_line_com = line.split(com)
                code = l_line_com[0]
                clue = l_line_com[-1].strip()

                quest = get_question(code, clue)

                res = res + quest + '\n'
            else:
                res = res + l_lines[i] + '\n'
    return res

def get_question(code, clue):
    """
        Get question xml
    """
    res = ''

    # form code
    c_code = code.strip()
    ind = code.index(c_code)
    s_add = code[0:ind].replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;').replace('    ', '&nbsp;&nbsp;&nbsp;&nbsp;')

    with open('question.xml', 'r') as f:
        content = f.read()
        cur_text = re.findall(r'<text>.*</text>', content)[0]
        content = content.replace(cur_text, '<text>{0}</text>'.format(c_code))
        cur_clue = re.findall(r'<clue>.*</clue>', content)[0]
        content = content.replace(cur_clue, '<clue>{0}</clue>'.format(clue))
        res = res + s_add + content
    return res



def get_com_list(ext):
    """
        Get comments of extension
    """
    l_com = list()
    if ext in d_opt['jcl']['extension']:
        if ext == 'py':
            l_com = ['#']
        if ext == 'java':
            l_com = ['//']
        if ext == 'sql':
            l_com = ['--', '/*', '*/']
    return l_com
        

# TODO: change name of project on name of directory
@exe_jms
def gen_prj():
    """
        Generate masher
    """
    l_files = [x for x in os.listdir('.') if x.endswith('.jcl')]
    global prj_name

    hotpot_file_list = ''

    # form hotpot_content
    for i in range(len(l_files)):
        cur_file_name = l_files[i].split('.')[0] + '.jcl'
        try:
            next_file_name = l_files[i+1].split('.')[0] + '.jcl'
        except:
            next_file_name = ''
        hotpot_content = get_hotpot_file(cur_file_name, next_file_name)
        hotpot_file_list = hotpot_file_list + hotpot_content

    res_content = ''
    with open('start_prj.xml', 'r') as f:
        content = f.read() 
        res_content = res_content + content
    res_content = res_content + hotpot_file_list
    with open('end_prj.xml', 'r') as f:
        content = f.read() 

        cur_output_folder = re.findall(r'<output-folder>.*</output-folder>', content)[0]
        new_output_folder = out_dir
        content = content.replace(cur_output_folder, '<output-folder>{0}</output-folder>'.format(new_output_folder))

        cur_source_folder = re.findall(r'<source-folder>.*</source-folder>', content)[0]
        new_source_folder = jcl_dir
        content = content.replace(cur_source_folder, '<source-folder>{0}</source-folder>'.format(new_source_folder))

        res_content = res_content + content
    
    # form masher
    with open(jcl_dir + prj_name, 'w') as f:
        f.write(res_content)



def get_hotpot_file(name_file, next_name_file):
    """
        Get hotpot file for jcl-file
    """
    with open('hotpot_prj.xml', 'r') as f:
        content = f.read()
        cur_data_file_name = re.findall(r'<data-file-name>.*</data-file-name>', content)[0]
        new_data_file_name = jcl_dir + '\\' + name_file
        content = content.replace(cur_data_file_name, '<data-file-name>{0}</data-file-name>'.format(new_data_file_name))

        cur_output_file_name = re.findall(r'<output-file-name>.*</output-file-name>', content)[0]
        new_output_file_name = name_file.replace('jcl', 'htm')
        content = content.replace(cur_output_file_name, '<output-file-name>{0}</output-file-name>'.format(new_output_file_name))

        cur_next_ex_file_name = re.findall(r'<next-ex-file-name>.*</next-ex-file-name>', content)[0]
        new_next_ex_file_name = next_name_file.replace('jcl', 'htm')
        content = content.replace(cur_next_ex_file_name, '<next-ex-file-name>{0}</next-ex-file-name>'.format(new_next_ex_file_name))
    return content

def run_jms():
    """
        Run masher
    """
    global prj_name
    masher_com = '"{masher}" {prj_name}'.format(masher=d_opt['jms']['masher'], prj_name=prj_name)
    local(masher_com)

if __name__ == "__main__":
    gen_jcl()
    gen_prj()
    run_jms()