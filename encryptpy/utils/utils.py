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

import logging
from datetime import datetime
from functools import wraps

logger = logging.getLogger(__name__)

def running_time(func):
    @wraps(func)
    def inner(*args, **kwargs):
        curr_time = datetime.now()
        rt = func(*args, **kwargs)
        run_time = (datetime.now()-curr_time).seconds
        logger.info(f'{func.__name__} running time: {run_time}')
        return rt
    return inner
