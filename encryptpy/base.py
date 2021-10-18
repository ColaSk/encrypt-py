# -*- encoding: utf-8 -*-
'''
@File    :   base.py
@Time    :   2021/10/18 14:43:47
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import re
import os
import logging

from shutil import copytree, ignore_patterns
import shutil
from typing import Union, List
from abc import abstractmethod

logger = logging.getLogger(__name__)

class EncryptPyBase:

    def __init__(self, 
            input: str, 
            output: str, 
            ignored: List = None) -> None:
        
        """
        * input_path : 输入路径 可以为文件夹 可以为文件
        * output_path ： 输出路径 必须为文件夹
        * ignored ：忽略的文件
        """
        self.input = input
        self.output = output
        self.ignored = ignored
    
    def copyproject(self):

        if os.path.exists(self.output):
            shutil.rmtree(self.output)

        return copytree(self.input, 
                        self.output, 
                        ignore=ignore_patterns(*self.ignored), 
                        dirs_exist_ok=True)
    
    def gen_searchfiles(self):
        """搜索可被加密的文件"""

        for root, _, files in os.walk(self.output):
            
            for filename in files:
                path = os.path.join(root, filename)
                if not filename.endswith('.py') or filename in ['__init__.py']:
                    logger.warning(f'Exclude file: {root}/{filename} not build')
                    continue
                yield path
    
    @abstractmethod
    def execute(self): pass
            
