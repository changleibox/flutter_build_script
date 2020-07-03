#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/28.
import os
import sys
import time
import zipfile

from src.util import log


def file_replace(file, old, new):
    """
    替换文件中的制定内容

    :param file: 文件
    :param old: 原有内容
    :param new: 需要替换成的内容
    """
    with open(file, 'r+', encoding='utf-8') as f:
        data = ''
        for line in f:
            if old in line:
                line = line.replace(old, new)
            data += line
        f.seek(0)
        f.write(data)
        f.truncate()


def zip_dir(dirname, zipfilename):
    """
    压缩文件夹

    :param dirname: 文件夹路径
    :param zipfilename: 压缩文件路径
    """

    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
    zf = zipfile.ZipFile(zipfilename, 'w', zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]  # print arcname
        zf.write(tar, arcname)
    zf.close()


def convert_fuke_size(size):
    size = int(size)
    kb = 1024
    mb = kb * 1024
    gb = mb * 1024
    tb = gb * 1024

    if size >= tb:
        return "%.1f TB" % float(size / tb)
    if size >= gb:
        return "%.1f GB" % float(size / gb)
    if size >= mb:
        return "%.1f MB" % float(size / mb)
    if size >= kb:
        return "%.1f KB" % float(size / kb)


def convert_time(datetime_str):
    minute = 60  # 1分钟
    hour = 60 * minute  # 1小时
    day = 24 * hour  # 1天
    month = 31 * day  # 月
    year = 12 * month  # 年

    struct_time = time.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    timestamp = time.time() - time.mktime(struct_time)
    if timestamp > year:
        return '%s年前' % int(timestamp / year)
    if timestamp > month:
        return '%s月前' % int(timestamp / month)
    if timestamp > day:
        return '%s天前' % int(timestamp / day)
    if timestamp > hour:
        return '%s小时前' % int(timestamp / hour)
    if timestamp > minute:
        return '%s分钟前' % int(timestamp / minute)
    return '刚刚'


def root_path():
    # 判断调试模式
    debug_vars = dict((a, b) for a, b in os.environ.items() if a.find('IPYTHONENABLE') >= 0)
    # 根据不同场景获取根目录
    if len(debug_vars) > 0:
        """当前为debug运行时"""
        path = sys.path[2]
    elif getattr(sys, 'frozen', False):
        """当前为exe运行时"""
        path = os.getcwd()
    else:
        """正常执行"""
        path = sys.path[1]
    return path


def print_path_not_exist(path):
    log.error('\nFAILURE: Build failed with an exception.\n')
    log.normal('* What went wrong:')
    log.normal('The specified project directory \'{}\' does not exist.'.format(path))


def print_procossing(text):
    log.error('\n\n****** %s ******' % text)


if __name__ == '__main__':
    print(convert_fuke_size(71025065))
    print(convert_time('2020-06-29 14:57:00'))
    print(root_path())
