#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) 2020 CHANGLEI. All rights reserved.

# Created by changlei on 2020/6/28.
import abc
import os

from src.config import configs_parser
from src.system import Paths
from src.util import print_procossing, log

_configs = configs_parser.get_config()

# 脚本名字
name = _configs.get('name')
# 脚本描述
description = _configs.get('description')
# 是否在build之前先拉取最新代码
git_enable = _configs.get('git_enable', True)
# 启用android构建，默认开启
android_enable = _configs.get('android_enable', True)
# 启用iOS构建，默认开启
ios_enable = _configs.get('ios_enable', True)


class Config(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def check_configs():
        ...

    @staticmethod
    def checkattr(args, args_name, args_type, nullable=True):
        if not nullable:
            assert args is not None, '请在\'assets/configs.yaml\'文件中设置参数 %s' % args_name
        if args is not None:
            assert type(args) == args_type, '%s 类型错误 %s，应该是 %s类型' % (args_name, type(args), args_type)
        log.info('%s：%s' % (args_name, args))

    @staticmethod
    def getattr(configs, attr_name, default=None):
        return configs[attr_name] if configs and attr_name in configs else default


class GitConfig(Config):
    # git配置
    git_config = Config.getattr(_configs, 'git_config')
    # git远程地址
    remote = Config.getattr(git_config, 'remote')
    # 分支
    branch = Config.getattr(git_config, 'branch')
    # 本地文件夹，存放在项目根目录下
    local_dir = Config.getattr(git_config, 'local_dir')
    # git用户名
    username = Config.getattr(git_config, 'username')
    # git密码
    password = Config.getattr(git_config, 'password')
    # git邮箱
    email = Config.getattr(git_config, 'email')

    @staticmethod
    def check_configs():
        Config.checkattr(GitConfig.git_config, 'git_config', dict, False)
        Config.checkattr(GitConfig.remote, 'remote', str, False)
        Config.checkattr(GitConfig.branch, 'branch', str, False)
        Config.checkattr(GitConfig.local_dir, 'local_dir', str, False)
        Config.checkattr(GitConfig.username, 'username', str, False)
        Config.checkattr(GitConfig.password, 'password', str, False)
        Config.checkattr(GitConfig.email, 'email', str, False)


class BuildConfig(Config, metaclass=abc.ABCMeta):
    @staticmethod
    def check_sub_class_configs(subclass):
        Config.checkattr(subclass.build_config, 'build_config', dict, False)
        Config.checkattr(subclass.build_type, 'build_type', str, False)
        Config.checkattr(subclass.export_type, 'export_type', str, False)
        Config.checkattr(subclass.tree_shake_icons, 'tree_shake_icons', bool)
        Config.checkattr(subclass.target, 'target', str)
        Config.checkattr(subclass.flavor, 'flavor', str)
        Config.checkattr(subclass.pub, 'pub', bool)
        Config.checkattr(subclass.build_number, 'build_number', str)
        Config.checkattr(subclass.build_name, 'build_name', str)
        Config.checkattr(subclass.split_debug_info, 'split_debug_info', str)
        Config.checkattr(subclass.obfuscate, 'obfuscate', bool)
        Config.checkattr(subclass.dart_define, 'dart_define', str)
        Config.checkattr(subclass.performance_measurement_file, 'performance_measurement_file', str)


class AndroidBuildConfig(BuildConfig):
    # Android构建配置
    build_config = Config.getattr(_configs, 'android_build_config')
    # 构建类型[debug|profile|release|自定义类型]
    build_type = Config.getattr(build_config, 'build_type')
    # 导出类型[export|pgy|appStore]
    export_type = Config.getattr(build_config, 'export_type')
    # 树摇动图标树摇动图标字体，以便仅保留应用程序使用的标志符号。
    # （默认为打开）
    tree_shake_icons = Config.getattr(build_config, 'tree_shake_icons')
    # 在设备上运行的应用程序的主入口点文件。如果省略了--target选项，但在命令行上提供了文件名，则使用该选项。
    # （默认为“lib/main.dart")
    target = Config.getattr(build_config, 'target')
    # Build由特定于平台的生成设置定义的自定义应用程序flavor。
    # 支持在Android Gradle脚本中使用产品风格，以及使用自定义Xcode方案。
    flavor = Config.getattr(build_config, 'flavor')
    # 执行此命令之前是否运行“fluster pub get”。
    # （默认为打开）
    pub = Config.getattr(build_config, 'pub')
    # 内部版本号用作内部版本号的标识符。
    # 每个生成都必须有一个唯一的标识符，以区别于以前的生成。
    # 它用于确定一个生成是否比另一个生成更新，较高的数字表示更新的生成。
    # 在Android上，它被用作“versionCode”。
    # 在Xcode构建中，它被用作“CFBundleVersion”
    build_number = Config.getattr(build_config, 'build_number')
    # 内部版本名=<x:y:z>一个“x:y:z”字符串，用作显示给用户的版本号。
    # 对于应用程序的每个新版本，您将提供一个版本号，以区别于以前的版本。
    # 在Android上，它被用作“versionName”。
    # 在Xcode构建中，它被用作“CFBundleShortVersionString”
    build_name = Config.getattr(build_config, 'build_name')
    # </project name/v1.2.3/>在发布版本中，此标志通过将Dart程序符号存储在主机上的单独文件中而不是存储在
    # 申请。标志的值应该是一个目录，可以在其中存储程序符号文件以供以后使用。这些符号文件包含
    # 表示飞镖堆叠痕迹所需的信息。对于使用此标志构建的应用程序，“flutr symbol”命令使用正确的程序符号
    # 文件是获取人类可读堆栈跟踪所必需的
    split_debug_info = Config.getattr(build_config, 'split_debug_info')
    # 在发布版本中，此标志将删除标识符，并用随机值替换它们，以进行源代码混淆。这面旗子
    # 必须始终与“--split-debug-info”选项结合使用，值和原始标识符之间的映射存储在符号映射中在指定目录中创建。
    # 对于使用此标志构建的应用程序，带有正确程序符号文件的“flutter symbol”命令是需要获取人类可读的堆栈跟踪。
    #
    # 因为所有标识符都被重命名，所以对象.runtimeType, 类型toString, 枚举toString, Stacktrace.toString, 符号.toString（用于
    # 常量符号或运行时系统生成的符号）将返回模糊结果。任何依赖确切名称的代码或测试都将崩溃。
    obfuscate = Config.getattr(build_config, 'obfuscate')
    # 可以作为字符串.fromEnvironment, 来自环境的布尔, 内部环境，和双.from环境施工人员。
    # 可以通过重复传递多个定义--省道定义多次。
    dart_define = Config.getattr(build_config, 'dart_define')
    # 性能度量文件flutter汇编性能和缓存信息将以JSON格式写入的文件的名称。
    performance_measurement_file = Config.getattr(build_config, 'performance_measurement_file')
    # 收缩是否在释放模式下启用代码收缩。当启用收缩时，您还可以受益于模糊处理，它缩短了
    # 应用程序的类和成员，以及优化，这将应用更积极的策略来进一步减小应用程序的大小。要了解更多信息，请参见：
    # https://developer.android.com/studio/build/shrink-code网站
    # （默认为打开）
    shrink = Config.getattr(build_config, 'shrink')
    # 是否按abi拆分apk。要了解更多信息，请参见：https://developer.android.com/studio/build/configure apk splits配置-abi分离
    # 编译应用程序的目标平台。
    #  [android-arm (default), android-arm64 (default), android-x86, android-x64 (default)]
    target_platform = Config.getattr(build_config, 'target_platform')
    # 是否按ABI拆分APK。要了解更多信息，请参见：https://developer.android.com/studio/build/configure apk拆分配置-abi分离
    split_per_abi = Config.getattr(build_config, 'split_per_abi')
    # 跟踪小部件创建跟踪小部件创建位置。这将启用小部件检查器等功能。此参数仅在调试模式下起作用（即
    # 编译JIT，而不是AOT）。
    # （默认为打开）
    track_widget_creation = Config.getattr(build_config, 'track_widget_creation')

    @staticmethod
    def check_configs():
        BuildConfig.check_sub_class_configs(AndroidBuildConfig)
        Config.checkattr(AndroidBuildConfig.shrink, 'shrink', bool)
        Config.checkattr(AndroidBuildConfig.target_platform, 'target_platform', str)
        Config.checkattr(AndroidBuildConfig.split_per_abi, 'split_per_abi', str)
        Config.checkattr(AndroidBuildConfig.track_widget_creation, 'track_widget_creation', bool)


class IOSBuildConfig(BuildConfig):
    # iOS构建配置
    build_config = Config.getattr(_configs, 'ios_build_config')
    # 构建类型[debug|profile|release]
    build_type = Config.getattr(build_config, 'build_type')
    # 导出类型[export|pgy|appStore]
    export_type = Config.getattr(build_config, 'export_type')
    # 树摇动图标树摇动图标字体，以便仅保留应用程序使用的标志符号。
    # （默认为打开）
    tree_shake_icons = Config.getattr(build_config, 'tree_shake_icons')
    # 在设备上运行的应用程序的主入口点文件。如果省略了--target选项，但在命令行上提供了文件名，则使用该选项。
    # （默认为“lib/main.dart")
    target = Config.getattr(build_config, 'target')
    # Build由特定于平台的生成设置定义的自定义应用程序flavor。
    # 支持在Android Gradle脚本中使用产品风格，以及使用自定义Xcode方案。
    flavor = Config.getattr(build_config, 'flavor')
    # 执行此命令之前是否运行“fluster pub get”。
    # （默认为打开）
    pub = Config.getattr(build_config, 'pub')
    # 内部版本号用作内部版本号的标识符。
    # 每个生成都必须有一个唯一的标识符，以区别于以前的生成。
    # 它用于确定一个生成是否比另一个生成更新，较高的数字表示更新的生成。
    # 在Android上，它被用作“versionCode”。
    # 在Xcode构建中，它被用作“CFBundleVersion”
    build_number = Config.getattr(build_config, 'build_number')
    # 内部版本名=<x:y:z>一个“x:y:z”字符串，用作显示给用户的版本号。
    # 对于应用程序的每个新版本，您将提供一个版本号，以区别于以前的版本。
    # 在Android上，它被用作“versionName”。
    # 在Xcode构建中，它被用作“CFBundleShortVersionString”
    build_name = Config.getattr(build_config, 'build_name')
    # </project name/v1.2.3/>在发布版本中，此标志通过将Dart程序符号存储在主机上的单独文件中而不是存储在
    # 申请。标志的值应该是一个目录，可以在其中存储程序符号文件以供以后使用。这些符号文件包含
    # 表示飞镖堆叠痕迹所需的信息。对于使用此标志构建的应用程序，“flutr symbol”命令使用正确的程序符号
    # 文件是获取人类可读堆栈跟踪所必需的。
    split_debug_info = Config.getattr(build_config, 'split_debug_info')
    # 在发布版本中，此标志将删除标识符，并用随机值替换它们，以进行源代码混淆。这面旗子
    # 必须始终与“--split debug info”选项结合使用，值和原始标识符之间的映射存储在符号映射中在指定目录中创建。
    # 对于使用此标志构建的应用程序，带有正确程序符号文件的“flutter symbol”命令是需要获取人类可读的堆栈跟踪。
    #
    # 因为所有标识符都被重命名，所以对象.runtimeType, 类型toString, 枚举toString, Stacktrace.toString, 符号.toString（用于
    # 常量符号或运行时系统生成的符号）将返回模糊结果。任何依赖确切名称的代码或测试都将崩溃。
    obfuscate = Config.getattr(build_config, 'obfuscate')
    # 可以作为字符串.fromEnvironment, 来自环境的布尔, 内部环境，和双.from环境施工人员。
    # 可以通过重复传递多个定义--省道定义多次。
    dart_define = Config.getattr(build_config, 'dart_define')
    # 性能度量文件flutter汇编性能和缓存信息将以JSON格式写入的文件的名称。
    performance_measurement_file = Config.getattr(build_config, 'performance_measurement_file')
    # 为iOS模拟器而不是设备生成模拟器。如果未指定，则将默认生成模式更改为调试。
    simulator = Config.getattr(build_config, 'simulator')
    # 对应用程序包进行代码签名（仅适用于设备生成）。
    # （默认为打开）
    codesign = Config.getattr(build_config, 'codesign')
    # exportOptionsPlist，一个键值对，放在项目assets目录下，build_type对应一个exportOptionsPlist。
    # 例如：
    # export_options:
    #   debug: ExportOptionsDebug.plist
    #   release: ExportOptionsRelease.plist
    export_options = Config.getattr(build_config, 'export_options')

    @staticmethod
    def check_configs():
        BuildConfig.check_sub_class_configs(IOSBuildConfig)
        Config.checkattr(IOSBuildConfig.simulator, 'simulator', bool)
        Config.checkattr(IOSBuildConfig.codesign, 'codesign', bool)
        Config.checkattr(IOSBuildConfig.export_options, 'export_options', dict, False)


class AppStoreConfig(Config):
    # AppStore配置 详情请查看文档：https://help.apple.com/itc/apploader/#/apdATD1E53-D1E1A1303-D1E53A1126
    app_store_config = Config.getattr(_configs, 'app_store_config')
    # 您的用户名。
    apple_id = Config.getattr(app_store_config, 'apple_id')
    # 指定文件的平台。{osx | ios | appletvos}
    type = Config.getattr(app_store_config, 'type')
    # 密钥id
    api_key = Config.getattr(app_store_config, 'api_key')
    # Issuer id
    api_issuer = Config.getattr(app_store_config, 'api_issuer')
    # 您想让 Application Loader 以结构化的 XML 格式还是非结构化的文本格式返回输出信息。默认情况下，Application Loader 以文本格式返回输出信息。
    # [xml | normal]
    output_format = Config.getattr(app_store_config, 'output_format')

    @staticmethod
    def check_configs():
        Config.checkattr(AppStoreConfig.app_store_config, 'app_store_config', dict, False)
        Config.checkattr(AppStoreConfig.apple_id, 'apple_id', str, False)
        Config.checkattr(AppStoreConfig.type, 'type', str, False)
        Config.checkattr(AppStoreConfig.api_key, 'api_key', str, False)
        Config.checkattr(AppStoreConfig.api_issuer, 'api_issuer', str, False)
        Config.checkattr(AppStoreConfig.output_format, 'output_format', str, False)


class PGYConfig(Config):
    # 蒲公英配置 详情请查看文档：https://www.pgyer.com/doc/view/api#paramInfo
    pgy_config = Config.getattr(_configs, 'pgy_config')
    # 路径
    url = Config.getattr(pgy_config, 'url')
    # (必填) API Key
    api_key = Config.getattr(pgy_config, '_api_key')
    # 用户Key，用来标识当前用户的身份，对于同一个蒲公英的注册用户来说，这个值在固定的。
    user_key = Config.getattr(pgy_config, 'user_key')
    # (必填)应用安装方式，值为(1,2,3)。1：公开，2：密码安装，3：邀请安装
    build_install_type = Config.getattr(pgy_config, 'build_install_type')
    # (必填) 设置App安装密码
    build_password = Config.getattr(pgy_config, 'build_password')
    # (选填) 版本更新描述，请传空字符串，或不传。
    build_update_description = Config.getattr(pgy_config, 'build_update_description')
    # (选填) 应用名称
    build_name = Config.getattr(pgy_config, 'build_name')
    # (选填)是否设置安装有效期，值为：1 设置有效时间， 2 长期有效，如果不填写不修改上一次的设置
    build_install_date = Config.getattr(pgy_config, 'build_install_date')
    # (选填)安装有效期开始时间，字符串型，如：2018-01-01
    build_install_start_date = Config.getattr(pgy_config, 'build_install_start_date')
    # (选填)安装有效期结束时间，字符串型，如：2018-12-31
    build_install_end_date = Config.getattr(pgy_config, 'build_install_end_date')
    # (选填)所需更新的指定渠道的下载短链接，只可指定一个渠道，字符串型，如：abcd
    build_channel_shortcut = Config.getattr(pgy_config, 'build_channel_shortcut')
    # android appKey
    android_app_key = Config.getattr(pgy_config, 'android_app_key')
    # ios appKey
    ios_app_key = Config.getattr(pgy_config, 'ios_app_key')

    @staticmethod
    def check_configs():
        Config.checkattr(PGYConfig.pgy_config, 'pgy_config', dict, False)
        Config.checkattr(PGYConfig.url, 'url', str, False)
        Config.checkattr(PGYConfig.api_key, 'api_key', str, False)
        Config.checkattr(PGYConfig.user_key, 'user_key', str, False)
        Config.checkattr(PGYConfig.build_install_type, 'build_install_type', int)
        Config.checkattr(PGYConfig.build_password, 'build_password', str)
        Config.checkattr(PGYConfig.build_update_description, 'build_update_description', str)
        Config.checkattr(PGYConfig.build_name, 'build_name', str)
        Config.checkattr(PGYConfig.build_install_date, 'build_install_date', str)
        Config.checkattr(PGYConfig.build_install_start_date, 'build_install_start_date', str)
        Config.checkattr(PGYConfig.build_install_end_date, 'build_install_end_date', str)
        Config.checkattr(PGYConfig.build_channel_shortcut, 'build_channel_shortcut', str)
        Config.checkattr(PGYConfig.android_app_key, 'android_app_key', str)
        Config.checkattr(PGYConfig.ios_app_key, 'ios_app_key', str)


class DingtalkConfig(Config):
    # 钉钉配置 详情请查看文档：https://ding-doc.dingtalk.com/doc#/serverapi2/elzz1p
    dingtalk_config = Config.getattr(_configs, 'dingtalk_config')
    url = Config.getattr(dingtalk_config, 'url')
    secret = Config.getattr(dingtalk_config, 'secret')
    access_key = Config.getattr(dingtalk_config, 'access_key')
    # 首屏会话透出的展示内容
    title = Config.getattr(dingtalk_config, 'title')
    # @所有人时：true，否则为：false（可选）
    is_at_all = Config.getattr(dingtalk_config, 'is_at_all', False)
    # 被@人的手机号（默认自动添加在text内容末尾，可取消自动化添加改为自定义设置，可选）
    at_mobiles = Config.getattr(dingtalk_config, 'at_mobiles')
    # 被@人的dingtalkId（可选）
    at_dingtalk_ids = Config.getattr(dingtalk_config, 'at_dingtalk_ids')
    # 是否自动在text内容末尾添加@手机号，默认自动添加，可设置为False取消（可选）
    is_auto_at = Config.getattr(dingtalk_config, 'is_auto_at', True)

    @staticmethod
    def check_configs():
        Config.checkattr(DingtalkConfig.dingtalk_config, 'dingtalk_config', dict, False)
        Config.checkattr(DingtalkConfig.url, 'url', str, False)
        Config.checkattr(DingtalkConfig.secret, 'secret', str, False)
        Config.checkattr(DingtalkConfig.access_key, 'access_key', str, False)
        Config.checkattr(DingtalkConfig.title, 'title', str, False)
        Config.checkattr(DingtalkConfig.is_at_all, 'is_at_all', bool)
        Config.checkattr(DingtalkConfig.at_mobiles, 'at_mobiles', list)
        Config.checkattr(DingtalkConfig.at_dingtalk_ids, 'at_dingtalk_ids', list)
        Config.checkattr(DingtalkConfig.is_auto_at, 'is_auto_at', bool)


class PathConfig(object):
    # 源码根目录
    root_path = os.path.join(Paths.sources_dir, GitConfig.local_dir)
    # Flutter配置文件
    yaml_path = os.path.join(root_path, 'pubspec.yaml')
    # build文件夹
    build_path = os.path.join(root_path, 'build')
    # apk输出路径
    apk_export_path = os.path.join(build_path, 'app', 'outputs', 'flutter-apk')
    # Flutter项目iOS的target名
    target_name = 'Runner'
    # xcworkspace路径
    xcworkspace_path = os.path.join(root_path, 'ios', '%s.xcworkspace' % target_name)
    # 生成的xcarchive路径
    xcarchive_path = os.path.join(build_path, 'ios', 'iphoneos', '%s.xcarchive' % target_name)
    # iap导出路径的文件名
    ipa_export_path = os.path.join(build_path, 'ios', 'iphoneos', target_name)
    # ipa路径
    ipa_path = os.path.join(ipa_export_path, '%s.ipa' % target_name)


def check_configs():
    print_procossing('通用配置')
    Config.checkattr(name, 'name', str, False)
    Config.checkattr(description, 'description', str, False)
    Config.checkattr(git_enable, 'git_enable', bool, False)
    Config.checkattr(android_enable, 'android_enable', bool, False)
    Config.checkattr(ios_enable, 'ios_enable', bool, False)
    for subclass in Config.__subclasses__():
        print_procossing(subclass.__name__)
        getattr(subclass, 'check_configs')()
