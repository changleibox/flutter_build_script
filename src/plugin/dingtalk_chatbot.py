#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

import base64
import hashlib
import hmac
import json
import logging
import re
import time
import urllib.parse
import urllib.request

from src.config import DingtalkConfig

try:
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError


# Created by changlei on 2020/6/24.
class DingtalkChatbot(object):
    def __init__(self):
        url = DingtalkConfig.url
        secret = DingtalkConfig.secret
        access_key = DingtalkConfig.access_key

        url = '%s?access_token=%s' % (url, access_key)  # 无加密的url

        timestamp = round(time.time() * 1000)  # 时间戳
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))  # 最终签名

        self.webhook_url = url + '&timestamp={}&sign={}'.format(timestamp, sign)  # 最终url，url+时间戳+签名

    @staticmethod
    def msg_open_type(url):
        """
        消息链接的打开方式
        1、默认或不设置时，为浏览器打开：pc_slide=False
        2、在PC端侧边栏打开：pc_slide=True
        """
        encode_url = urllib.parse.quote_plus(url)
        return 'dingtalk://dingtalkclient/page/link?url={}&pc_slide=false'.format(encode_url)

    def send_meassage(self, data):
        """
        发送消息至机器人对应的群
        :param data: 发送的内容
        :return:
        """
        header = {
            'Content-Type': 'application/json',
            'Charset': 'UTF-8'
        }
        send_data = json.dumps(data)  # 将字典类型数据转化为json格式
        send_data = send_data.encode('utf-8')  # 编码为UTF-8格式
        request = urllib.request.Request(url=self.webhook_url, data=send_data, headers=header)  # 发送请求

        opener = urllib.request.urlopen(request)  # 将请求发回的数据构建成为文件格式
        return json.loads(opener.read())

    def send_text(self, msg, is_at_all=False, at_mobiles=None, at_dingtalk_ids=None, is_auto_at=True):
        """
        text类型
        :param msg: 消息内容
        :param is_at_all: @所有人时：true，否则为false（可选）
        :param at_mobiles: 被@人的手机号（注意：可以在msg内容里自定义@手机号的位置，也支持同时@多个手机号，可选）
        :param at_dingtalk_ids: 被@人的dingtalkId（可选）
        :param is_auto_at: 是否自动在msg内容末尾添加@手机号，默认自动添加，可设置为False取消（可选）
        :return: 返回消息发送结果
        """
        if at_dingtalk_ids is None:
            at_dingtalk_ids = []
        if at_mobiles is None:
            at_mobiles = []
        data = {'msgtype': 'text', 'at': {}}
        if is_not_null_and_blank_str(msg):
            data['text'] = {'content': msg}
        else:
            logging.error('text类型，消息内容不能为空！')
            raise ValueError('text类型，消息内容不能为空！')

        if is_at_all:
            # noinspection PyTypeChecker
            data['at']['isAtAll'] = is_at_all

        if at_mobiles:
            at_mobiles = list(map(str, at_mobiles))
            # noinspection PyTypeChecker
            data['at']['atMobiles'] = at_mobiles
            if is_auto_at:
                mobiles_text = '\n@' + '@'.join(at_mobiles)
                data['text']['content'] = msg + mobiles_text

        if at_dingtalk_ids:
            at_dingtalk_ids = list(map(str, at_dingtalk_ids))
            # noinspection PyTypeChecker
            data['at']['atDingtalkIds'] = at_dingtalk_ids

        logging.debug('text类型：%s' % data)
        return self.send_meassage(data)

    def send_image(self, pic_url):
        """
        image类型（表情）
        :param pic_url: 图片链接
        :return: 返回消息发送结果
        """
        if is_not_null_and_blank_str(pic_url):
            data = {
                'msgtype': 'image',
                'image': {
                    'picURL': pic_url
                }
            }
            logging.debug('image类型：%s' % data)
            return self.send_meassage(data)
        else:
            logging.error('image类型中图片链接不能为空！')
            raise ValueError('image类型中图片链接不能为空！')

    def send_link(self, title, text, message_url, pic_url=''):
        """
        link类型
        :param title: 消息标题
        :param text: 消息内容（如果太长自动省略显示）
        :param message_url: 点击消息触发的URL
        :param pic_url: 图片URL（可选）
        :return: 返回消息发送结果

        """
        if all(map(is_not_null_and_blank_str, [title, text, message_url])):
            data = {
                'msgtype': 'link',
                'link': {
                    'text': text,
                    'title': title,
                    'picUrl': pic_url,
                    'messageUrl': self.msg_open_type(message_url)
                }
            }
            logging.debug('link类型：%s' % data)
            return self.send_meassage(data)
        else:
            logging.error('link类型中消息标题或内容或链接不能为空！')
            raise ValueError('link类型中消息标题或内容或链接不能为空！')

    def send_markdown(self, title, text, is_at_all=False, at_mobiles=None, at_dingtalk_ids=None, is_auto_at=True):
        """
        markdown类型
        :param title: 首屏会话透出的展示内容
        :param text: markdown格式的消息内容
        :param is_at_all: @所有人时：true，否则为：false（可选）
        :param at_mobiles: 被@人的手机号（默认自动添加在text内容末尾，可取消自动化添加改为自定义设置，可选）
        :param at_dingtalk_ids: 被@人的dingtalkId（可选）
        :param is_auto_at: 是否自动在text内容末尾添加@手机号，默认自动添加，可设置为False取消（可选）
        :return: 返回消息发送结果
        """
        if at_dingtalk_ids is None:
            at_dingtalk_ids = []
        if at_mobiles is None:
            at_mobiles = []
        if all(map(is_not_null_and_blank_str, [title, text])):
            # 给Mardown文本消息中的跳转链接添加上跳转方式
            text = re.sub(r'(?<!!)\[.*?\]\((.*?)\)',
                          lambda m: m.group(0).replace(m.group(1), self.msg_open_type(m.group(1))), text)
            data = {
                'msgtype': 'markdown',
                'markdown': {
                    'title': title,
                    'text': text
                },
                'at': {}
            }
            if is_at_all:
                data['at']['isAtAll'] = is_at_all

            if at_mobiles:
                at_mobiles = list(map(str, at_mobiles))
                data['at']['atMobiles'] = at_mobiles
                if is_auto_at:
                    mobiles_text = '\n@' + '@'.join(at_mobiles)
                    data['markdown']['text'] = text + mobiles_text

            if at_dingtalk_ids:
                at_dingtalk_ids = list(map(str, at_dingtalk_ids))
                data['at']['atDingtalkIds'] = at_dingtalk_ids

            logging.debug('markdown类型：%s' % data)
            return self.send_meassage(data)
        else:
            logging.error('markdown类型中消息标题或内容不能为空！')
            raise ValueError('markdown类型中消息标题或内容不能为空！')

    def send_action_card(self, action_card):
        """
        ActionCard类型
        :param action_card: 整体跳转ActionCard类型实例或独立跳转ActionCard类型实例
        :return: 返回消息发送结果
        """
        if isinstance(action_card, ActionCard):
            data = action_card.get_data()

            if 'singleURL' in data['actionCard']:
                data['actionCard']['singleURL'] = self.msg_open_type(data['actionCard']['singleURL'])
            elif 'btns' in data['actionCard']:
                for btn in data['actionCard']['btns']:
                    # noinspection PyTypeChecker
                    btn['actionURL'] = self.msg_open_type(btn['actionURL'])

            logging.debug('ActionCard类型：%s' % data)
            return self.send_meassage(data)
        else:
            logging.error('ActionCard类型：传入的实例类型不正确，内容为：{}'.format(str(action_card)))
            raise TypeError('ActionCard类型：传入的实例类型不正确，内容为：{}'.format(str(action_card)))

    def send_feed_card(self, links):
        """
        FeedCard类型
        :param links: FeedLink实例列表 or CardItem实例列表
        :return: 返回消息发送结果
        """
        if not isinstance(links, list):
            logging.error('FeedLink类型：传入的数据格式不正确，内容为：{}'.format(str(links)))
            raise ValueError('FeedLink类型：传入的数据格式不正确，内容为：{}'.format(str(links)))

        link_list = []
        for link in links:
            # 兼容：1、传入FeedLink实例列表；2、CardItem实例列表；
            if isinstance(link, FeedLink) or isinstance(link, CardItem):
                link = link.get_data()
                link['messageURL'] = self.msg_open_type(link['messageURL'])
                link_list.append(link)
            else:
                logging.error('FeedLink类型，传入的数据格式不正确，内容为：{}'.format(str(link)))
                raise ValueError('FeedLink类型，传入的数据格式不正确，内容为：{}'.format(str(link)))

        data = {'msgtype': 'feedCard', 'feedCard': {'links': link_list}}
        logging.debug('FeedCard类型：%s' % data)
        return self.send_meassage(data)


def is_not_null_and_blank_str(content):
    """
    非空字符串
    :param content: 字符串
    :return: 非空 - True，空 - False

    >>> is_not_null_and_blank_str('')
    False
    >>> is_not_null_and_blank_str(' ')
    False
    >>> is_not_null_and_blank_str('  ')
    False
    >>> is_not_null_and_blank_str('123')
    True
    """
    if content and content.strip():
        return True
    else:
        return False


class ActionCard(object):
    """
    ActionCard类型消息格式（整体跳转、独立跳转）
    """

    def __init__(self, title, text, btns, btn_orientation=0, hide_avatar=0):
        """
        ActionCard初始化
        :param title: 首屏会话透出的展示内容
        :param text: markdown格式的消息
        :param btns: 按钮列表：（1）按钮数量为1时，整体跳转ActionCard类型；（2）按钮数量大于1时，独立跳转ActionCard类型；
        :param btn_orientation: 0：按钮竖直排列，1：按钮横向排列（可选）
        :param hide_avatar: 0：正常发消息者头像，1：隐藏发消息者头像（可选）
        """
        super(ActionCard, self).__init__()
        self.title = title
        self.text = text
        self.btn_orientation = btn_orientation
        self.hide_avatar = hide_avatar
        btn_list = []
        for btn in btns:
            if isinstance(btn, CardItem):
                btn_list.append(btn.get_data())
        if btn_list:
            btns = btn_list  # 兼容：1、传入CardItem示例列表；2、传入数据字典列表
        self.btns = btns

    def get_data(self):
        """
        获取ActionCard类型消息数据（字典）
        :return: 返回ActionCard数据
        """
        if all(map(is_not_null_and_blank_str, [self.title, self.text])) and len(self.btns):
            if len(self.btns) == 1:
                # 整体跳转ActionCard类型
                data = {
                    'msgtype': 'actionCard',
                    'actionCard': {
                        'title': self.title,
                        'text': self.text,
                        'hideAvatar': self.hide_avatar,
                        'btnOrientation': self.btn_orientation,
                        'singleTitle': self.btns[0]['title'],
                        'singleURL': self.btns[0]['actionURL']
                    }
                }
                return data
            else:
                # 独立跳转ActionCard类型
                data = {
                    'msgtype': 'actionCard',
                    'actionCard': {
                        'title': self.title,
                        'text': self.text,
                        'hideAvatar': self.hide_avatar,
                        'btnOrientation': self.btn_orientation,
                        'btns': self.btns
                    }
                }
                return data
        else:
            logging.error('ActionCard类型，消息标题或内容或按钮数量不能为空！')
            raise ValueError('ActionCard类型，消息标题或内容或按钮数量不能为空！')


class FeedLink(object):
    """
    FeedCard类型单条消息格式
    """

    def __init__(self, title, message_url, pic_url):
        """
        初始化单条消息文本
        :param title: 单条消息文本
        :param message_url: 点击单条信息后触发的URL
        :param pic_url: 点击单条消息后面图片触发的URL
        """
        super(FeedLink, self).__init__()
        self.title = title
        self.message_url = message_url
        self.pic_url = pic_url

    def get_data(self):
        """
        获取FeedLink消息数据（字典）
        :return: 本FeedLink消息的数据
        """
        if all(map(is_not_null_and_blank_str, [self.title, self.message_url, self.pic_url])):
            data = {
                'title': self.title,
                'messageURL': self.message_url,
                'picURL': self.pic_url
            }
            return data
        else:
            logging.error('FeedCard类型单条消息文本、消息链接、图片链接不能为空！')
            raise ValueError('FeedCard类型单条消息文本、消息链接、图片链接不能为空！')


class CardItem(object):
    """
    ActionCard和FeedCard消息类型中的子控件
    """

    def __init__(self, title, url, pic_url=None):
        """
        CardItem初始化
        @param title: 子控件名称
        @param url: 点击子控件时触发的URL
        @param pic_url: FeedCard的图片地址，ActionCard时不需要，故默认为None
        """
        super(CardItem, self).__init__()
        self.title = title
        self.url = url
        self.pic_url = pic_url

    def get_data(self):
        """
        获取CardItem子控件数据（字典）
        @return: 子控件的数据
        """
        if all(map(is_not_null_and_blank_str, [self.title, self.url, self.pic_url])):
            # FeedCard类型
            data = {
                'title': self.title,
                'messageURL': self.url,
                'picURL': self.pic_url
            }
            return data
        elif all(map(is_not_null_and_blank_str, [self.title, self.url])):
            # ActionCard类型
            data = {
                'title': self.title,
                'actionURL': self.url
            }
            return data
        else:
            logging.error('CardItem是ActionCard的子控件时，title、url不能为空；是FeedCard的子控件时，title、url、pic_url不能为空！')
            raise ValueError('CardItem是ActionCard的子控件时，title、url不能为空；是FeedCard的子控件时，title、url、pic_url不能为空！')
