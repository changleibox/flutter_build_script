#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/7/2.
import sys

from src.builder import ApkBuilder
from src.builder import IOSBuilder
from src.config import configs
from src.helper import ChatbotHelper, GitHelper
from src.util import log, utils


class LaunchHelper(object):
    @staticmethod
    def launch():
        sys.excepthook = LaunchHelper.__global_excepthook

        log.info(configs.name)
        log.info(configs.description)

        configs.check_configs()

        if configs.git_enable:
            utils.print_procossing('开始拉取代码')
            git_helper = GitHelper()
            result = git_helper.clone()
            if result == 0:
                result = git_helper.pull()
            if result != 0:
                log.error('代码拉取失败，请稍后尝试')
                return

        builders = list()
        if configs.android_enable:
            builders.append(ApkBuilder())
        if configs.ios_enable:
            builders.append(IOSBuilder())

        if len(builders) == 0:
            log.error('请在配置文件设置需要构建的类型')
            return

        result_dict = dict()
        for builder in builders:
            utils.print_procossing('开始构建%s' % builder.name)
            result = builder.release()
            if result is None or result['code'] != 0:
                continue
            result_dict[builder.name] = result

        if len(result_dict) > 0:
            utils.print_procossing('构建完成，正在通知测试人员')
            chatbot_helper = ChatbotHelper()
            chatbot_helper.notify(result_dict)
        else:
            log.error('构建失败，请检查后重试')

    @staticmethod
    def __global_excepthook(exctype, value, traceback):
        if exctype == KeyboardInterrupt:
            utils.print_procossing('程序被动终止')
            return
        sys.__excepthook__(exctype, value, traceback)
