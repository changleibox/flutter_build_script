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
        self.__line = prefix

    def append(self, k, v):
        if v is None:
            return self
        if type(v) == bool:
            if v:
                self.__command_args.append('%s%s' % (self.__line, k))
            else:
                self.__command_args.append('%sno-%s' % (self.__line, k))
        else:
            self.__command_args.append('%s%s %s' % (self.__line, k, v))
        return self

    def to_command(self):
        return ' '.join(self.__command_args)
