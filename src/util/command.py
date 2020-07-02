#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/29.
import subprocess


def call(cmd, cwd=None):
    return subprocess.call(cmd, shell=True, cwd=cwd)


class CommandBuilder(object):
    def __init__(self, command_header, prefix='--'):
        self.__command_args = list()
        self.__command_args.append(command_header)
        self.__prefix = prefix

    def append(self, k, v, prefix=None):
        if v is None:
            return self
        prefix = prefix if prefix else self.__prefix
        assert prefix, '请设置prefix'
        if type(v) == bool:
            if v:
                self.__command_args.append('%s%s' % (prefix, k))
            else:
                self.__command_args.append('%sno-%s' % (prefix, k))
        else:
            self.__command_args.append('%s%s %s' % (prefix, k, v))
        return self

    def to_command(self):
        return ' '.join(self.__command_args)
