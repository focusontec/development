#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Date  : 2018/1/23
# @Author: lsj
# @File  : base.py
# @Desc  : 工具类：基础常用
"""

import bisect
import functools
import hashlib
import logging
import random
import re
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool


# 计算MD5值
def get_md5_value(src):
    md5 = hashlib.md5()
    md5.update(src)
    return md5.hexdigest()


# 计算sha1值
def get_sha1_value(src):
    sha1 = hashlib.sha1()
    sha1.update(src)
    return sha1.hexdigest()


# 明文密码加密
def get_pwd_value(src):
    temp = get_md5_value(src) + src
    return get_sha1_value(temp)


# 简易多进程，用法类似map
def map_pool_process(func, iterable):
    pool = Pool()
    pool.map(func, iterable)
    pool.close()
    pool.join()
    pass


# 简易多线程，用法类似map
def map_pool_thread(func, iterable):
    pool = ThreadPool()
    pool.map(func, iterable)
    pool.close()
    pool.join()
    pass


# 异常捕获装饰器
def try_except_log(arg=None):
    # 带参数的装饰器
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            try:
                return func(*args, **kw)
            except Exception as e:
                if isinstance(arg, logging.Logger):
                    arg.error('{}==>{}'.format(type(e), e))
                else:
                    print('{}==>{}'.format(type(e), e))
                print(args)

        return wrapper

    if callable(arg):
        return decorator(arg)
    return decorator


# 驼峰命名转换蛇形（下划线）命名
def hump_to_line(name):
    name = re.sub(pattern=r'([A-Za-z])([0-9])', repl=r'\1_\2', string=name)
    name = re.sub(pattern=r'([0-9])([A-Za-z])', repl=r'\1_\2', string=name)
    name = re.sub(pattern=r'([a-z])([A-Z])', repl=r'\1_\2', string=name)
    name = re.sub(pattern=r'([A-Z])([A-Z])([a-z])', repl=r'\1_\2\3', string=name)
    return name.strip('_').lower()
    pass


# 加权随机算法，时间复杂度是O（n）
def weight_choice(weight):
    """
    计算权重总和sum，然后在1到sum之间随机选择一个数R，之后遍历整个集合，统计遍历的项的权重之和，如果大于等于R，就停止遍历，选择遇到的项。
    :param weight: list对应的权重序列
    :return:选取的值在原列表里的索引
    """
    t = random.randint(0, sum(weight) - 1)
    for i, val in enumerate(weight):
        t -= val
        if t < 0:
            return i


# 加权随机算法，时间复杂度是O(logN)
def weight_choice2(weight):
    """
    可以先对原始序列按照权重排序。这样遍历的时候，概率高的项可以很快遇到，减少遍历的项。
    （因为rnd递减的速度最快(先减去最大的数)）
    这样提高了平均选取速度，但是原序列排序也需要时间。
    先搞一个权重值的前缀和序列，然后再生成一个随机数t，用二分法来从这个前缀和序列里找
    :param weight: list对应的权重序列
    :return:选取的值在原列表里的索引
    """
    weight_sum = []
    _sum = 0
    for a in weight:
        _sum += a
        weight_sum.append(_sum)
    t = random.randint(0, _sum - 1)
    return bisect.bisect_right(weight_sum, t)
