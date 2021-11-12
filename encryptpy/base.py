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

import logging

import os
import shutil
from abc import abstractmethod
from shutil import copytree, ignore_patterns
from typing import List

logger = logging.getLogger(__name__)

class EncryptPyBase:

    def __init__(self, 
            input: str, 
            output: str, 
            ignored: List = None,
            ignore_pf: List = None,
            *args, **kwargs) -> None:
        
        """
        * input_path : 输入路径 可以为文件夹 可以为文件
        * output_path ： 输出路径 必须为文件夹
        * ignored ：忽略的文件或文件夹，将不会copy到编译项目下
        * ignore_pf ：忽略的文件，将不会被加密，但是保存在编译目录下
        * keep_step: 保留中间过程文件
        """
        self.input = input
        self.output = output
        self.ignored = ignored
        self.ignore_pf = ignore_pf if ignore_pf else []
        self.max_workers = kwargs.get('max_workers', 8)
        self.keep_step =  kwargs.get('keep_step', False)

    
    def copyproject(self):
        """拷贝项目到目标文件夹"""

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

                # TODO: 希望支持正则法则
                if (not filename.endswith('.py') or 
                    filename in ['__init__.py'] or 
                    filename in self.ignore_pf):

                    logger.warning(f'Exclude file: {root}/{filename} not build')
                    continue
                
                yield path
    
    @abstractmethod
    def execute(self): pass
            
