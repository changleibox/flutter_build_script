#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/28.
import sys


class ProgressBar:
    def __init__(self, count=0, total=0, width=50):
        """
        控制台输出进度条

        :param count: 当前进度
        :param total: 总的进度
        :param width: 显示宽度
        """
        self.count = count
        self.total = total
        self.width = width

    def move(self):
        """
        当前进度加1
        """
        self.count += 1

    def log(self, s):
        """
        在控制台打印

        :param s: 显示的日志
        """
        sys.stdout.write(' ' * (self.width + 9) + '\r')
        sys.stdout.flush()
        print(s)
        progress = self.width * self.count / self.total
        sys.stdout.write('{0:3}/{1:3}: '.format(self.count, self.total))
        sys.stdout.write('#' * int(progress) + '-' * int(self.width - progress) + '\r')
        if progress == self.width:
            sys.stdout.write('\n')
        sys.stdout.flush()
