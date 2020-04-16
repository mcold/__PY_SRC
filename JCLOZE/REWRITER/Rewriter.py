# coding: utf-8

"""
    Rewrite html-files for hotkeys usability
"""

import os
import re


def rewrite():
    """
        Rewrite files
    """
    for f in [x for x in os.listdir('.') if x.rpartition('.')[-1] in ['htm', 'html']]:
        with open(f, 'r') as file:
            content = file.read().replace('<body onload="StartUp()" id="TheBody" >', 
            '<body onload="StartUp()" id="TheBody" onkeyup="hotkey(event)">').replace('ShowMessage(Output);',
            '//ShowMessage(Output);').replace('ShowMessage(GiveHint);',
            '//ShowMessage(GiveHint);')
            # get pattern for replacement change location to page
            try:
                l_files = [x + '.htm' for x in re.findall('onclick="location=\'(\w+)', content) if x not in ['index']]
                next_file = l_files[0]
                hotkey_func = '\n\
                function hotkey(event){\n\
                    if (event.keyCode == 191) {ShowHint();}    // ?\n\
                    if (event.keyCode == 19) {CheckAnswers();} // Pause\n\
                    if (event.keyCode == 36){location=\'index.htm\';} // Home\n\
                }\n\
                '
                content = content.replace('//-->', hotkey_func)
            except:
                hotkey_func = '\n\
                function hotkey(event){\n\
                    if (event.keyCode == 191) {ShowHint();}    // ?\n\
                    if (event.keyCode == 19) {CheckAnswers();} // Pause\n\
                    if (event.keyCode == 36){location=\'index.htm\';} // Home\n\
                }\n\
                '
                content = content.replace('//-->', hotkey_func)
        with open(f, 'w') as file:
            file.write(content)


if __name__ == '__main__':
    rewrite()