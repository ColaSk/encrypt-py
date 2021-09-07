# -*- encoding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2021/09/06 18:44:56
@Author  :   sk 
@Version :   1.0
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''
# here put the import lib
import os
import shutil
import re
from typing import List, Union
import utils


def copytree(src_path, dst_path):
    pass

def copyfile(src_file, dst_file):
    return shutil.copyfile(src_file, dst_file)

def searchpyfile(src_path: str, ignored: Union[List, str, None] = None):
    """[summary]

    Args:
        src_path (str): 输入路径
        ignored (Union[List, str, None], optional): [支持正则表达式]. Defaults to None.

    Returns:
        [type]: [文件路径数组]
    """
    def match(pattern, string, flags=0):
        return re.search(pattern, string, flags=0)

    rt = []
    for path, _, files in os.walk(src_path):
        for file in files:
            
            if not file.endswith('.py'):
                continue

            file_path = os.path.join(path, file)

            if ignored:
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

