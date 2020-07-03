#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/30.
import os

from src.util import utils


class Paths(object):
    assets_dir = os.path.join(utils.root_path(), 'assets')
    # 临时文件夹
    tmp_dir = os.path.join(utils.root_path(), 'tmp')
    # 输出文件夹，包括导出的apk和ipa
    outputs_dir = os.path.join(tmp_dir, 'outputs')
    # 存放项目源码
    sources_dir = os.path.join(tmp_dir, 'sources')

    config_template_path = os.path.join(assets_dir, 'configs.json')
    config_path = os.path.join(assets_dir, 'configs.yaml')
