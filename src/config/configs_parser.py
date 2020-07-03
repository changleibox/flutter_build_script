#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/30.
import json
import os

import yaml

from src.system import Paths


def __resolve_configs_file():
    with open(Paths.config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def __create_config_file():
    with open(Paths.config_path, 'w', encoding='utf-8') as f, \
            open(Paths.config_template_path, 'r', encoding='utf-8') as template:
        yaml.safe_dump(
            data=json.loads(template.read()),
            stream=f,
            default_style=None,
            sort_keys=False,
            allow_unicode=True,
            indent=2,
        )


def get_config():
    if not os.path.exists(Paths.config_path):
        __create_config_file()
    return __resolve_configs_file()
