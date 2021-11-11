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

import logging
import os
import re
from concurrent.futures import ProcessPoolExecutor, as_completed
from distutils.command.build_py import build_py
from distutils.core import setup

from Cython.Build import cythonize
from encryptpy.base import EncryptPyBase
from encryptpy.utils import TempDirContext, running_time

def get_package_dir(*args, **kwargs):
    return ""

# TODO ? 重写get_package_dir， 否则生成的so文件路径有问题
build_py.get_package_dir = get_package_dir

logger = logging.getLogger(__name__)

class SOEncryptPy(EncryptPyBase):
    """.so 加密python项目"""
   
    COMPILER_DIRECTIVES = {
        'language_level': 3,              # 语言版本
        'always_allow_keywords': True,    # 
        'annotation_typing': False        # 禁止强制类型验证
    }
        
    def encrypt(self, py_file):

        logger.info(f'file: {py_file} Execution starting')

        dir_name = os.path.dirname(py_file)
        file_name = os.path.basename(py_file)
        os.chdir(dir_name)

        with TempDirContext() as dc:

            setup(
                ext_modules=cythonize([file_name], quiet=True, compiler_directives=self.COMPILER_DIRECTIVES),
                script_args=['build_ext', '-t', dc, '--inplace']
            )

        self.del_step_file(py_file)

        logger.info(f'file: {py_file} Execution complete')
        
        return py_file, True

    def rename_so(self, filepath):
        """重命名.so文件"""

        if filepath.endswith('.so'):
            newname = re.sub("(.*)\..*\.(.*)", r"\1.\2", filepath)
            os.rename(filepath, newname)
            logger.info(f'Rename: {filepath}->{newname}')
    
    def del_step_file(self, py_file):
        """删除源文件与过程文件"""

        os.remove(py_file)

        if not self.keep_step:

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
    
    @running_time
    def execute(self):
        """加密执行
        1.拷贝项目
        2.加密文件
        3.删除源文件与中间文件
        4.对.so文件重命名
        """
        logger.info('Encryption start'.center(100, '*'))
        # copy input -> output
        self.copyproject()
        
        # encrypt py -> .so
        # del intermediate file .c
        tasks = []
        
        # 通过多进程解决同文件编译问题
        # TODO:由于进程创建销毁过程导致性能损耗问题，需要解决
        for filepath in self.gen_searchfiles():
            with ProcessPoolExecutor(max_workers=1) as pool:
                task = pool.submit(self.encrypt, filepath)
                tasks.append(task)
        
        for task in as_completed(tasks):
            try:
                re_file, rt = task.result()
                logger.info(f'file: {re_file} build success, RESULT: {rt}')
            except Exception as e:
                logger.error(f'unknown error: {e.__str__()}')
                
        # rename .so
        # for filepath in self.gen_search_refiles():
        #     self.rename_so(filepath)
        
        logger.info('Encryption end'.center(100, '*'))
