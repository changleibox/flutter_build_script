#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/23.
import abc
import os
import shutil

import requests

from src.config import PGYConfig, Paths
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

    @staticmethod
    def _upload_export(app_path):
        if not os.path.exists(Paths.export_dir):
            os.makedirs(Paths.export_dir)
        app_dir = os.path.dirname(app_path)
        export_dir = os.path.join(Paths.export_dir, os.path.basename(app_dir))
        if os.path.exists(export_dir):
            shutil.rmtree(export_dir)
        shutil.copytree(app_dir, export_dir)
        export_path = os.path.join(export_dir, os.path.basename(app_path))
        if os.path.exists(export_path):
            log.debug('已成功导出到：%s' % export_path)
        else:
            log.debug('导出失败，请稍后重试')

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
