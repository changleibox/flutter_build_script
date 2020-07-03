#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/28.
import os

from src.config import PGYConfig, DingtalkConfig, Paths
from src.plugin import DingtalkChatbot
from src.util import utils, log


class ChatbotHelper(object):
    def __init__(self):
        self.chatbot = DingtalkChatbot()
        with open(os.path.join(Paths.assets_dir, 'description.md'), 'r', encoding='utf-8') as file:
            self.mark_down_text = file.read()

    def notify(self, result_dict):
        if len(result_dict) == 0:
            return
        mark_down_texts = self.__resolve_mark_down_text(result_dict)
        for name, mark_down_text in mark_down_texts.items():
            result = self.chatbot.send_markdown(
                title=DingtalkConfig.title,
                text=mark_down_text,
                is_at_all=DingtalkConfig.is_at_all,
                at_mobiles=DingtalkConfig.at_mobiles,
                at_dingtalk_ids=DingtalkConfig.at_dingtalk_ids,
                is_auto_at=DingtalkConfig.is_auto_at,
            )
            log.info('%s 通知成功：%s' % (name, result))

    def __resolve_mark_down_text(self, result_dict):
        mark_down_texts = dict()

        for name, result in result_dict.items():
            data = result['data']

            mark_down_params = {
                'appName': data.get('buildName'),
                'platform': name,
                'buildShortcutUrl': data.get('buildShortcutUrl'),
                # 'buildIcon': data.get('buildIcon'),
                'buildVersion': data.get('buildVersion'),
                'buildBuildVersion': data.get('buildBuildVersion'),
                'buildFileSize': utils.convert_fuke_size(data.get('buildFileSize')),
                'buildUpdated': utils.convert_time(data.get('buildUpdated')),
                'buildQRCodeURL': data.get('buildQRCodeURL'),
                '_api_key': PGYConfig.api_key,
                'buildKey': data.get('buildKey'),
                'buildPassword': PGYConfig.build_password,
            }
            mark_down_text = self.mark_down_text.format(**mark_down_params)
            mark_down_texts[name] = mark_down_text

        return mark_down_texts
