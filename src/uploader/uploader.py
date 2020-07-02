#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/23.
import abc

import requests

from src.config import PGYConfig
from src.util import log


class Uploader(metaclass=abc.ABCMeta):
    def __init__(self, export_type):
        self.export_type = export_type

    def upload(self, app_path):
        export_type = self.export_type
        if export_type == 'export':
            return self._upload_export(app_path)
        elif export_type == 'pgy':
            return self._upload_pgy(app_path)
        elif export_type == 'appStore':
            return self._upload_app_store(app_path)
        else:
            log.debug('不支持的导出类型')
            return None

    @abc.abstractmethod
    def _upload_app_store(self, app_path):
        ...

    @abc.abstractmethod
    def _upload_export(self, app_path):
        ...

    @staticmethod
    def _upload_pgy(app_path):
        params = PGYConfig.pgy_config.copy()
        del params['url']
        files = {
            'file': open(app_path, 'rb')
        }
        log.info('正在上传：%s' % app_path)
        response = requests.post(PGYConfig.url, params=params, files=files)
        result = response.json()
        log.info('上传完成：%s' % result)
        return response.json()
