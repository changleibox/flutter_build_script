#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/24.
from src.config import AndroidBuildConfig
from src.publisher import ApkPublisher
from src.uploader import Uploader
from src.util import log


class ApkUploader(Uploader):
    def __init__(self):
        super(ApkUploader, self).__init__(AndroidBuildConfig.export_type)
        self.__publisher = ApkPublisher()

    def _upload_app_store(self, app_path):
        return self.__publisher.upload(app_path)

    def _upload_export(self, app_path):
        log.debug('已成功导出到： %s' % app_path)
