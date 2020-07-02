#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/23.
import os

import src.util as utils
from src.builder import Builder
from src.config import IOSBuildConfig, Paths
from src.uploader.ios_uploader import IOSUploader
from src.util.command import CommandBuilder


class IOSBuilder(Builder):
    __TARGET_NAME = 'Runner'
    __PODS_PATH = os.path.join('ios', 'Pods', 'Target Support Files', 'Pods-Runner')
    __JCORE_LIB = ' -l"jcore-ios-2.2.5"'
    __XCCONFIG_NAMES = [
        'Pods-Runner.debug.xcconfig',
        'Pods-Runner.profile.xcconfig',
        'Pods-Runner.release.xcconfig'
    ]

    def __init__(self):
        super(IOSBuilder, self).__init__(IOSUploader(), 'iOS')

    def build(self, build_type):
        return self.__xcodebuild_build(build_type)

    def release(self, build_type=IOSBuildConfig.build_type):
        return super(IOSBuilder, self).release(build_type)

    def __xcodebuild_build(self, build_type):
        assert build_type is not None
        build_type = build_type.lower()
        self.__pod_install()
        result = self._env_call(self.__flutter_build_command(build_type))
        if result != 0:
            self.__remove_jcore()
            return self.build(build_type)
        else:
            build_type = build_type.capitalize()
            self._env_call(self.__xcodebuild_clean_command(build_type))
            result = self._env_call(self.__xcodebuild_archive_command(build_type))
            if result == 0:
                result = self._env_call(self.__xcodebuild_export_archive_command(build_type))
            if result != 0 or not os.path.exists(Paths.ipa_path):
                raise ValueError('打包失败，请检查后重试')
            return Paths.ipa_path

    def __pod_install(self):
        self._env_call('cd ios && pod install')
        self.__remove_jcore()

    def __remove_jcore(self):
        for xcconfig_name in self.__XCCONFIG_NAMES:
            xcconfig_path = os.path.join(self._ROOT_PATH, self.__PODS_PATH, xcconfig_name)
            utils.file_replace(xcconfig_path, self.__JCORE_LIB, '')

    @staticmethod
    def __flutter_build_command(build_type):
        assert build_type, 'build_type 不能为空'
        return CommandBuilder('flutter build ios --%s' % build_type) \
            .append('tree-shake-icons', IOSBuildConfig.tree_shake_icons) \
            .append('target', IOSBuildConfig.target) \
            .append('flavor', IOSBuildConfig.flavor) \
            .append('pub', IOSBuildConfig.pub) \
            .append('build-number', IOSBuildConfig.build_number) \
            .append('build-name', IOSBuildConfig.build_name) \
            .append('split-debug-info', IOSBuildConfig.split_debug_info) \
            .append('obfuscate', IOSBuildConfig.obfuscate) \
            .append('dart-define', IOSBuildConfig.dart_define) \
            .append('performance-measurement-file', IOSBuildConfig.performance_measurement_file) \
            .append('simulator', IOSBuildConfig.simulator) \
            .append('codesign', IOSBuildConfig.codesign) \
            .to_command()

    @staticmethod
    def __xcodebuild_clean_command(build_type):
        assert build_type, 'build_type 不能为空'
        return CommandBuilder('xcodebuild clean', prefix='-') \
            .append('workspace', Paths.xcworkspace_path) \
            .append('scheme', Paths.target_name) \
            .append('configuration', build_type) \
            .to_command()

    @staticmethod
    def __xcodebuild_archive_command(build_type):
        assert build_type, 'build_type 不能为空'
        return CommandBuilder('xcodebuild archive', prefix='-') \
            .append('workspace', Paths.xcworkspace_path) \
            .append('scheme', Paths.target_name) \
            .append('configuration', build_type) \
            .append('archivePath', Paths.xcarchive_path) \
            .to_command()

    @staticmethod
    def __xcodebuild_export_archive_command(build_type):
        assert build_type, 'build_type 不能为空'
        export_options_name = IOSBuildConfig.export_options.get(build_type.lower())
        assert export_options_name, 'export_options_name 不能为空，请在配置文件设置你的exportOptionsPlist'
        export_options_plist_path = os.path.join(utils.root_path(), 'assets', export_options_name)
        return CommandBuilder('xcodebuild -exportArchive', prefix='-') \
            .append('archivePath', Paths.xcarchive_path) \
            .append('exportPath', Paths.ipa_export_path) \
            .append('exportOptionsPlist', export_options_plist_path) \
            .to_command()
