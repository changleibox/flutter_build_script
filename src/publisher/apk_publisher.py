#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/29.
from src.publisher import Publisher
from src.util import log


class ApkPublisher(Publisher):
    def __init__(self):
        super().__init__()

    def upload(self, app_path):
        log.debug('上传到应用市场功能暂不支持Android %s' % app_path)
