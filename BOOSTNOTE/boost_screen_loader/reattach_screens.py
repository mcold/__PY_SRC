# coding: utf-8


import time
import gen
import shutil
import os
import glob

def test():
    return str(time.time()).replace('.', '')


import time

def test2():
    """
        Get time in format: yyyy-mm-ddThh:mi:ss.ms
        like: "2019-09-17T16:33:09.930Z"
    """
    t = time.localtime()
    return str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday) + 'T' + str(t.tm_hour) + ':' + str(t.tm_min) + ':' + str(t.tm_sec) + '.0000'


if __name__ == "__main__":
    print(gen.return_screens())
