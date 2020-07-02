#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/29.
import abc


class Publisher(metaclass=abc.ABCMeta):
    def __init__(self): ...

    @abc.abstractmethod
    def upload(self, app_path): ...
