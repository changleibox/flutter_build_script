#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/23.
import abc

from src.config import PathConfig
from src.util import command


class Builder(metaclass=abc.ABCMeta):
    _ROOT_PATH = PathConfig.root_path
    _BUILD_PATH = PathConfig.build_path

    def __init__(self, name, uploader):
        self.name = name
        self.uploader = uploader

    @abc.abstractmethod
    def build(self, build_type):
        ...

    def clean(self):
        self._env_call('flutter clean')

    def pub_get(self):
        self._env_call('flutter pub get')

    def upload(self, app_path):
        assert self.uploader is not None
        return self.uploader.upload(app_path)

    def release(self, build_type=None):
        self.clean()
        self.pub_get()
        result = self._run_build_runner()
        if result == 0:
            app_path = self.build(build_type)
            if app_path:
                response = self.upload(app_path)
                return response

    def _run_build_runner(self):
        return self._env_call('flutter packages pub run build_runner build --delete-conflicting-outputs')

    @staticmethod
    def _env_call(cmd):
        return command.call(cmd, cwd=PathConfig.root_path)
