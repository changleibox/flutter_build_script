#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/30.
import os

from src.config import GitConfig
from src.util import utils


class Paths(object):
    root_path = os.path.join(utils.root_path(), 'tmp', GitConfig.local_dir)
    yaml_path = os.path.join(root_path, 'pubspec.yaml')
    build_path = os.path.join(root_path, 'build')
    apk_path = os.path.join('app', 'outputs', 'flutter-apk')
    target_name = 'Runner'
    xcworkspace_path = os.path.join(root_path, 'ios', '%s.xcworkspace' % target_name)
    xcarchive_path = os.path.join(build_path, 'ios', 'iphoneos', '%s.xcarchive' % target_name)
    ipa_export_path = os.path.join(build_path, 'ios', 'iphoneos', '%s' % target_name)
    ipa_path = os.path.join(ipa_export_path, '%s.ipa' % target_name)
    export_dir = os.path.join(utils.root_path(), 'tmp', 'outputs')
