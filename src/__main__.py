#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/23.
import sys

from src.builder import ApkBuilder
from src.builder import IOSBuilder
from src.helper import ChatbotHelper, GitHelper
from src.util import log


def __global_excepthook(exctype, value, traceback):
    if exctype == KeyboardInterrupt:
        log.error('\n\n****** 程序被手动停止 ******')
        return
    sys.__excepthook__(exctype, value, traceback)


def _run():
    git_helper = GitHelper()
    result = git_helper.clone()
    if result == 0:
        result = git_helper.pull()
    if result != 0:
        log.error('代码拉取失败，请稍后尝试')
        return

    builders = [
        ApkBuilder(),
        IOSBuilder(),
    ]
    result_dict = dict()
    for builder in builders:
        result = builder.release()
        if result is None or result['code'] != 0:
            continue
        result_dict[builder.name()] = result

    if len(result_dict) > 0:
        chatbot_helper = ChatbotHelper()
        chatbot_helper.notify(result_dict)


if __name__ == '__main__':
    sys.excepthook = __global_excepthook
    _run()
