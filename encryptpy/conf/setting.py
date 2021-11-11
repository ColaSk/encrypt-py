# -*- encoding: utf-8 -*-
'''
@File    :   setting.py
@Time    :   2021/11/11 11:38:25
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



class Setting:

    default_filter_config = {
        'filter': {
            'ignored': ['.git',' __pycache__', '.vscode', 'tests', 'migrations', '__pycache__'],
            'ignore_pf': ['server.py', 'config.py']
        }
    }
    pass

class EncryptType:
    so = '1'