# -*- encoding: utf-8 -*-
'''
@File    :   encrypt.py
@Time    :   2021/09/06 18:45:48
@Author  :   sk 
@Version :   1.0
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import os
import logging
import re
import shutil

from typing import Union, List
from utils import searchpyfile, copyfile, TempDirContext
from distutils.core import setup
from Cython.Build import cythonize

logger = logging.getLogger(__name__)
class EncryptionPy(object):

    def __init__(self, 
                 input_path: str, 
                 output_path: str, 
                 ignored: Union[List, str, None] = None) -> None:
        
        """
        TODO: 暂时支持路径
        * input_path : 输入路径 可以为文件夹 可以为文件
        * output_path ： 输出路径 必须为文件夹
        * ignored ：忽略的文件
        """ 
        
        assert (input_path != output_path), "The input path is the same as the output path"

        assert not os.path.isfile(output_path), "The output path is a file"
        
        # 绝对路径
        self._input_path = os.path.abspath(input_path)
        self._output_path = os.path.abspath(output_path)
        self._ignored = ignored

        if os.path.exists(self._output_path):
            shutil.rmtree(self._output_path)

    def __copyfiles(self, files_path, dst_path):
        rt = []
        for file_path in files_path:
            dst_file_path = file_path.replace(self._input_path, dst_path)
            path_split = dst_file_path.split('/')
            path = '/'.join(path_split[0:-1])
            os.makedirs(path, exist_ok=True)
            logger.debug(f"copy file: {file_path}, dst file: {dst_file_path}")
            copyfile(file_path, dst_file_path)
            rt.append(dst_file_path)
        return rt
    
    def __filterfile(self, files_path, ignored):
    
        def match(pattern, string, flags=0):
            return re.search(pattern, string, flags=0)

        rt = []

        for file_path in files_path:
            if isinstance(ignored, str):
                if match(ignored, file_path):
                    continue
            elif isinstance(ignored, list):
                is_continue = False
                for i in ignored:
                    if match(i, file_path):
                        is_continue = True
                        break
                if is_continue:
                    continue
            rt.append(file_path)
        return rt
    
    def __deletedfile(self, files_path):
        pass
    
    # ? 还存在一定问题, 后续更改
    def __encrypt(self, files_path):
        encrypted_py = []

        with TempDirContext() as td:
            total_count = len(files_path)
            for i, py_file in enumerate(files_path):
                try:
                    dir_name = os.path.dirname(py_file)
                    file_name = os.path.basename(py_file)

                    os.chdir(dir_name)

                    logger.debug("正在加密 {}/{},  {}".format(i + 1, total_count, file_name))

                    setup(
                        ext_modules=cythonize([file_name], quiet=True, language_level=3),
                        script_args=["build_ext", "-t", td, "--inplace"],
                    )

                    encrypted_py.append(py_file)
                    logger.debug("加密成功 {}".format(file_name))

                except Exception as e:
                    logger.exception("加密失败 {} , error {}".format(py_file, e))
                    temp_c = py_file.replace(".py", ".c")
                    if os.path.exists(temp_c):
                        os.remove(temp_c)

            return encrypted_py

    def encrypt(self):
        """加密接口
        *基本流程
        *1.搜索需要加密的所有文件路径
        *2.过滤掉需要排除的文件或路径
        *3.路径编译加密
        """
        logger.info(f"input path: {self._input_path}")
        logger.info(f"output path: {self._output_path}")
        
        # 搜索python文件
        files = searchpyfile(self._input_path)
        
        # 过滤python文件
        files = self.__filterfile(files, self._ignored)

        # 拷贝文件到目标文件夹
        dst_files = self.__copyfiles(files, self._output_path)

        # 加密文件
        # encrtptfiles = self.__encrypt(dst_files)

        logger.info(f"dst path files: {dst_files}")
        # logger.info(f"encrtptfiles: {encrtptfiles}")

    
    def test(self):
        files = searchpyfile(self._input_path)
        logger.info(f"dst path files: {files}")