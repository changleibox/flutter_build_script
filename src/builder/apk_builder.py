#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/23.
import os

from src.builder import Builder
from src.config import AndroidBuildConfig, Paths
from src.uploader import ApkUploader
from src.util import CommandBuilder


class ApkBuilder(Builder):
    def __init__(self):
        super(ApkBuilder, self).__init__('Android', ApkUploader())

    def build(self, build_type):
        assert build_type is not None
        result = self._env_call(self.__flutter_build_command(build_type))
        if result == 0:
            return os.path.join(Paths.apk_export_path, 'app-%s.apk' % build_type)
        else:
            raise ValueError('打包失败，请检查后重试')

    def release(self, build_type=AndroidBuildConfig.build_type):
        return super(ApkBuilder, self).release(build_type)

    @staticmethod
    def __flutter_build_command(build_type):
        assert build_type, 'build_type 不能为空'
        return CommandBuilder('flutter build apk --%s' % build_type) \
            .append('tree-shake-icons', AndroidBuildConfig.tree_shake_icons) \
            .append('target', AndroidBuildConfig.target) \
            .append('flavor', AndroidBuildConfig.flavor) \
            .append('pub', AndroidBuildConfig.pub) \
            .append('build-number', AndroidBuildConfig.build_number) \
            .append('build-name', AndroidBuildConfig.build_name) \
            .append('split-debug-info', AndroidBuildConfig.split_debug_info) \
            .append('obfuscate', AndroidBuildConfig.obfuscate) \
            .append('dart-define', AndroidBuildConfig.dart_define) \
            .append('performance-measurement-file', AndroidBuildConfig.performance_measurement_file) \
            .append('shrink', AndroidBuildConfig.shrink) \
            .append('target-platform', AndroidBuildConfig.target_platform) \
            .append('split-per-abi', AndroidBuildConfig.split_per_abi) \
            .append('track-widget-creation', AndroidBuildConfig.track_widget_creation) \
            .to_command()
