#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/30.
import os
import shutil

from src.config import GitConfig, PathConfig
from src.util import command, utils


class GitHelper(object):
    def __init__(self):
        self.__remote = GitConfig.remote
        self.__branch = GitConfig.branch
        self.__local_path = PathConfig.root_path
        self.__username = GitConfig.username
        self.__password = GitConfig.password
        self.__email = GitConfig.email

    def credential_helper(self):
        return self.__git_env_call('git config --global credential.helper store')

    def set_infos(self):
        self.__git_env_call('git config --global user.name \'{}\''.format(self.__username))
        self.__git_env_call('git config --global user.email \'{}\''.format(self.__password))
        self.__git_env_call('git config --global user.password \'{}\''.format(self.__password))

    def init(self):
        return command.call('git init %s' % self.__local_path)

    def clone(self):
        if os.path.exists(self.__local_path) and not os.path.exists(PathConfig.yaml_path):
            shutil.rmtree(self.__local_path)
        if not os.path.exists(self.__local_path):
            return command.call('git clone -b %s %s %s' % (self.__branch, self.__remote, self.__local_path))
        return 0

    def pull(self):
        if not os.path.exists(self.__local_path):
            utils.print_path_not_exist(self.__local_path)
            return -1
        self.__git_env_call('git status && git log --stat')
        # 更新 检出分支 并拉取最新代码，cwd为git目录
        result = self.__git_env_call('git fetch --all')
        if result == 0:
            result = self.__git_env_call('git reset --hard origin/%s' % self.__branch)
        if result == 0:
            result = self.__git_env_call('git checkout %s' % self.__branch)
        if result == 0:
            result = self.__git_env_call('git pull')
        return result

    def __git_env_call(self, cmd):
        return command.call(cmd, cwd=self.__local_path)
