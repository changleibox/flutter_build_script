#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/24.

from src.config import IOSBuildConfig
from src.publisher import IOSPublisher
from src.uploader import Uploader
from src.util import log


class IOSUploader(Uploader):
    def __init__(self):
        super(IOSUploader, self).__init__(IOSBuildConfig.export_type)
        self.__publisher = IOSPublisher()

    def _upload_app_store(self, app_path):
        build_type = IOSBuildConfig.build_type
        if build_type.lower() == 'release':
            self.__publisher.upload(app_path)
        else:
            log.debug('%s方式不支持上传到AppStore' % build_type)
