#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/29.
from src.config import AppStoreConfig
from src.publisher import Publisher
from src.util import command, log


class IOSPublisher(Publisher):
    def __init__(self):
        super().__init__()
        self.apple_id = AppStoreConfig.apple_id
        self.api_key = AppStoreConfig.api_key
        self.api_issuer = AppStoreConfig.api_issuer
        self.type = AppStoreConfig.type
        self.output_format = AppStoreConfig.output_format

    def upload(self, app_path):
        log.debug('正在上传到AppStore……')
        result = self._validate_app(app_path)
        if result == 0:
            result = self._upload_app(app_path)
        if result == 0:
            log.debug('上传成功')
        else:
            log.debug('上传失败')

    def _validate_app(self, app_path):
        return command.call(
            'xcrun altool --validate-app -f %s -t %s -apiKey %s -apiIssuer %s --output-format %s' % (
                app_path, self.type, self.api_key, self.api_issuer, self.output_format))

    def _upload_app(self, app_path):
        return command.call(
            'xcrun altool --upload-app -f %s -t %s -apiKey %s -apiIssuer %s --output-format %s' % (
                app_path, self.type, self.api_key, self.api_issuer, self.output_format))
