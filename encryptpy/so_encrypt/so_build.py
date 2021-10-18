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

    COMPILER_DIRECTIVES = {
        'language_level': 3, 
        'always_allow_keywords': True, 
        'annotation_typing': False
    }

    def delete_files(self, py_file: str):
        """删除原 .py .pyx 文件"""

        try:
            os.remove(py_file)

            if py_file.endswith('.py'):
                c_file = py_file.replace('.py', '.c')
            else:
                c_file = py_file.replace('.pyx', '.c')
            if os.path.exists(c_file):
                os.remove(c_file)

        except Exception as exc:
            pass
        
    def encrypt(self, py_file):
        try:
            dir_name = os.path.dirname(py_file)
            file_name = os.path.basename(py_file)
            os.chdir(dir_name)

            with TempDirContext() as dc:

                setup(
                    ext_modules=cythonize([file_name], quiet=True, compiler_directives=self.COMPILER_DIRECTIVES),
                    script_args=['build_ext', '-t', dc, '--inplace']
                )

                logger.info(f'Success: {py_file} build success')

        except Exception as exc:

            logger.error(f'Fail: {py_file} build fail: {traceback.format_exc()}')

        # return py_file
    
    def rename_so(self, filepath):
        if filepath.endswith('.so'):
            newname = re.sub("(.*)\..*\.(.*)", r"\1.\2", filepath)
            os.rename(filepath, newname)
    
    def del_step_file(self, py_file):

        os.remove(py_file)

        if py_file.endswith('.py'):
            c_file = py_file.replace('.py', '.c')
        else:
            c_file = py_file.replace('.pyx', '.c')
        if os.path.exists(c_file):
            os.remove(c_file)
    
    def gen_search_refiles(self):
        """搜索可被加密的文件"""
        for root, _, files in os.walk(self.output):
            
            for filename in files:
                path = os.path.join(root, filename)
                if not filename.endswith('.so'):
                    continue
                yield path

    def execute(self):
        self.copyproject()
        for filepath in self.gen_searchfiles():
            self.encrypt(filepath)
            self.del_step_file(filepath)
        
        for filepath in self.gen_search_refiles():
            self.rename_so(filepath)