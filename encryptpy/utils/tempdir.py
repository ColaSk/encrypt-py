# -*- encoding: utf-8 -*-
'''
@File    :   tempdir.py
@Time    :   2021/09/07 14:25:54
@Author  :   sk 
@Version :   1.0
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import shutil
import tempfile

from contextlib import ContextDecorator

class TempDirContext(ContextDecorator):
    """临时文件夹
    """    

    def __init__(self, 
                 suffix=None, 
                 prefix=None, 
                 dir=None) -> None:
        
        """
        * suffix : 后缀
        * prefix : 前缀
        * dir : 文件夹路径
        """        

        self.suffix = suffix
        self.prefix = prefix
        self.dir = dir
       
    
    def __enter__(self):
        self.dir_name = tempfile.mkdtemp(
                self.suffix, self.prefix, self.dir
            )
        return self.dir_name
    
    def __exit__(self, exc_type, exc_value, traceback):
        shutil.rmtree(self.dir_name)
