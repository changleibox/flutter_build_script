#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/30.
import os

from src.util import ntlog

COLOR_DEFAULT = 'default'
COLOR_BLACK = 'black'
COLOR_RED = 'red'
COLOR_GREEN = 'green'
COLOR_YELLOW = 'yellow'
COLOR_BLUE = 'blue'
COLOR_PURPLE = 'purple'
COLOR_CYAN = 'cyan'
COLOR_WHITE = 'white'

STYLE = {
    'fore': {
        COLOR_BLACK: 30, COLOR_RED: 31, COLOR_GREEN: 32, COLOR_YELLOW: 33,
        COLOR_BLUE: 34, COLOR_PURPLE: 35, COLOR_CYAN: 36, COLOR_WHITE: 37,
    },
    'back': {
        COLOR_BLACK: 40, COLOR_RED: 41, COLOR_GREEN: 42, COLOR_YELLOW: 43,
        COLOR_BLUE: 44, COLOR_PURPLE: 45, COLOR_CYAN: 46, COLOR_WHITE: 47,
    },
    'mode': {
        'bold': 1, 'underline': 4, 'blink': 5, 'invert': 7,
    },
    'default': {
        'end': 0,
    }
}


def use_style(string, mode='', fore='', back=''):
    mode = '%s' % STYLE['mode'][mode] if mode in STYLE['mode'].keys() else ''
    fore = '%s' % STYLE['fore'][fore] if fore in STYLE['fore'].keys() else ''
    back = '%s' % STYLE['back'][back] if back in STYLE['back'].keys() else ''
    style = ';'.join([s for s in [mode, fore, back] if s])
    style = '\033[%sm' % style if style else ''
    end = '\033[%sm' % STYLE['default']['end'] if style else ''
    return '%s%s%s' % (style, string, end)


def color_print(msg, color=COLOR_DEFAULT):
    if os.name == 'nt':
        if color == COLOR_BLACK:
            ntlog.print_black(msg)
        elif color == COLOR_RED:
            ntlog.print_red(msg)
        elif color == COLOR_GREEN:
            ntlog.print_green(msg)
        elif color == COLOR_YELLOW:
            ntlog.print_yellow(msg)
        elif color == COLOR_BLUE:
            ntlog.print_blue(msg)
        elif color == COLOR_PURPLE:
            ntlog.print_pink(msg)
        elif color == COLOR_CYAN:
            ntlog.print_sky_blue(msg)
        elif color == COLOR_WHITE:
            ntlog.print_white(msg)
    else:
        print(use_style(msg, fore=color))


def normal(msg):
    color_print(msg)


def verbose(msg):
    color_print(msg, COLOR_BLUE)


def debug(msg):
    color_print(msg, COLOR_BLUE)


def info(msg):
    color_print(msg, COLOR_GREEN)


def warn(msg):
    color_print(msg, COLOR_YELLOW)


def error(msg):
    color_print(msg, COLOR_RED)


def debug_cmd(cmd):
    debug(cmd)
