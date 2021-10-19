# -*- encoding: utf-8 -*-
'''
@File    :   so_build.py
@Time    :   2021/10/18 14:41:13
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib

import os
import logging
import sys
import traceback
import re
import shutil

from typing import Union, List
from utils import TempDirContext
from distutils.core import setup
from Cython.Build import cythonize
from encryptpy.base import EncryptPyBase

logger = logging.getLogger(__name__)

class SOEncryptPy(EncryptPyBase):
    """.so 加密python项目"""

    COMPILER_DIRECTIVES = {
        'language_level': 3, 
        'always_allow_keywords': True, 
        'annotation_typing': False
    }
        
    def encrypt(self, py_file):

        dir_name = os.path.dirname(py_file)
        file_name = os.path.basename(py_file)
        os.chdir(dir_name)

        with TempDirContext() as dc:

            setup(
                ext_modules=cythonize([file_name], quiet=True, compiler_directives=self.COMPILER_DIRECTIVES),
                script_args=['build_ext', '-t', dc, '--inplace']
            )

            logger.info(f'Success: {py_file} build success')

    def rename_so(self, filepath):
        """重命名.so文件"""

        if filepath.endswith('.so'):
            newname = re.sub("(.*)\..*\.(.*)", r"\1.\2", filepath)
            os.rename(filepath, newname)
            logger.info(f'Rename: {filepath}->{newname}')
    
    def del_step_file(self, py_file):
        """删除源文件与过程文件"""

        os.remove(py_file)

        if py_file.endswith('.py'):
            c_file = py_file.replace('.py', '.c')
        else:
            c_file = py_file.replace('.pyx', '.c')

        if os.path.exists(c_file):
            os.remove(c_file)
    
    def gen_search_refiles(self):
        """搜索需要重命名的.so文件"""

        for root, _, files in os.walk(self.output):
            
            for filename in files:
                path = os.path.join(root, filename)
                if not filename.endswith('.so'):
                    continue
                yield path

    def execute(self):
        """加密执行
        1.拷贝项目
        2.加密文件
        3.删除源文件与中间文件
        4.对.so文件重命名
        """

        # copy input -> output
        self.copyproject()
        
        # encrypt py -> .so
        # del intermediate file .c
        for filepath in self.gen_searchfiles():
            self.encrypt(filepath)
            self.del_step_file(filepath)
        
        # rename .so
        for filepath in self.gen_search_refiles():
            self.rename_so(filepath)