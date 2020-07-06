# flutter_build_script
Flutter项目自动打包上线脚本

### Python环境
>Python 3.7

### 三方库
>PyYAML  
>requests

### 启动方式
新建启动配置，配置模块启动方式，模块名为src，或者直接用命令方式：  
``` shell 
python3 -m src
```

### 配置参数解释

```yaml
name: 自动化打包脚本
description: 用于Flutter项目的自动化导包上线及发布到蒲公英测试

# 是否在build之前先拉取最新代码
git_enable: true
# 启用android构建，默认开启
android_enable: true
# 启用iOS构建，默认开启
ios_enable: true


# git配置
git_config:
  # git远程地址
  remote: xxx
  # 分支
  branch: dev
  # 本地文件夹，存放在项目根目录下
  local_dir: xxx
  # git用户名
  username: xxx
  # git密码
  password: xxx
  # git邮箱
  email: xxx

# Android构建配置
android_build_config:
  # 构建类型[debug|profile|release|自定义类型]
  build_type: release
  # 导出类型[export|pgy|appStore]
  export_type: pgy
  # 树摇动图标树摇动图标字体，以便仅保留应用程序使用的标志符号。
  #（默认为打开）
  # tree_shake_icons: true
  # 在设备上运行的应用程序的主入口点文件。如果省略了--target选项，但在命令行上提供了文件名，则使用该选项。
  #（默认为“lib/main.dart")
  # target: xxx
  # Build由特定于平台的生成设置定义的自定义应用程序flavor。
  # 支持在Android Gradle脚本中使用产品风格，以及使用自定义Xcode方案。
  # flavor: xxx
  # 执行此命令之前是否运行“fluster pub get”。
  #（默认为打开）
  # pub: true
  # 内部版本号用作内部版本号的标识符。
  # 每个生成都必须有一个唯一的标识符，以区别于以前的生成。
  # 它用于确定一个生成是否比另一个生成更新，较高的数字表示更新的生成。
  # 在Android上，它被用作“versionCode”。
  # 在Xcode构建中，它被用作“CFBundleVersion”
  # build_number: xxx
  # 内部版本名=<x:y:z>一个“x:y:z”字符串，用作显示给用户的版本号。
  # 对于应用程序的每个新版本，您将提供一个版本号，以区别于以前的版本。
  # 在Android上，它被用作“versionName”。
  # 在Xcode构建中，它被用作“CFBundleShortVersionString”
  # build_name: xxx
  # </project name/v1.2.3/>在发布版本中，此标志通过将Dart程序符号存储在主机上的单独文件中而不是存储在
  # 申请。标志的值应该是一个目录，可以在其中存储程序符号文件以供以后使用。这些符号文件包含
  # 表示飞镖堆叠痕迹所需的信息。对于使用此标志构建的应用程序，“flutr symbol”命令使用正确的程序符号
  # 文件是获取人类可读堆栈跟踪所必需的
  # split_debug_info: xxx
  # 在发布版本中，此标志将删除标识符，并用随机值替换它们，以进行源代码混淆。这面旗子
  # 必须始终与“--split-debug-info”选项结合使用，值和原始标识符之间的映射存储在符号映射中在指定目录中创建。
  # 对于使用此标志构建的应用程序，带有正确程序符号文件的“flutter symbol”命令是需要获取人类可读的堆栈跟踪。
  #
  # 因为所有标识符都被重命名，所以对象.runtimeType, 类型toString, 枚举toString, Stacktrace.toString, 符号.toString（用于
  # 常量符号或运行时系统生成的符号）将返回模糊结果。任何依赖确切名称的代码或测试都将崩溃。
  # obfuscate: true
  # 可以作为字符串.fromEnvironment, 来自环境的布尔, 内部环境，和双.from环境施工人员。
  # 可以通过重复传递多个定义--省道定义多次。
  # dart_define: xxx
  # 性能度量文件flutter汇编性能和缓存信息将以JSON格式写入的文件的名称。
  # performance_measurement_file: xxx
  # 收缩是否在释放模式下启用代码收缩。当启用收缩时，您还可以受益于模糊处理，它缩短了
  # 应用程序的类和成员，以及优化，这将应用更积极的策略来进一步减小应用程序的大小。要了解更多信息，请参见：
  # https://developer.android.com/studio/build/shrink-code网站
  #（默认为打开）
  # shrink: true
  # 是否按abi拆分apk。要了解更多信息，请参见：https://developer.android.com/studio/build/configure apk splits配置-abi分离
  # 编译应用程序的目标平台。
  #  [android-arm (default), android-arm64 (default), android-x86, android-x64 (default)]
  # target_platform: xxx
  # 是否按ABI拆分APK。要了解更多信息，请参见：https://developer.android.com/studio/build/configure apk拆分配置-abi分离
  # split_per_abi: xxx
  # 跟踪小部件创建跟踪小部件创建位置。这将启用小部件检查器等功能。此参数仅在调试模式下起作用（即
  # 编译JIT，而不是AOT）。
  #（默认为打开）
  # track_widget_creation: true

# iOS构建配置
ios_build_config:
  # 构建类型[debug|profile|release]
  build_type: debug
  # 导出类型[export|pgy|appStore]
  export_type: pgy
  # 树摇动图标树摇动图标字体，以便仅保留应用程序使用的标志符号。
  #（默认为打开）
  # tree_shake_icons: true
  # 在设备上运行的应用程序的主入口点文件。如果省略了--target选项，但在命令行上提供了文件名，则使用该选项。
  #（默认为“lib/main.dart")
  # target: xxx
  # Build由特定于平台的生成设置定义的自定义应用程序flavor。
  # 支持在Android Gradle脚本中使用产品风格，以及使用自定义Xcode方案。
  # flavor: xxx
  # 执行此命令之前是否运行“fluster pub get”。
  #（默认为打开）
  # pub: true
  # 内部版本号用作内部版本号的标识符。
  # 每个生成都必须有一个唯一的标识符，以区别于以前的生成。
  # 它用于确定一个生成是否比另一个生成更新，较高的数字表示更新的生成。
  # 在Android上，它被用作“versionCode”。
  # 在Xcode构建中，它被用作“CFBundleVersion”
  # build_number: xxx
  # 内部版本名=<x:y:z>一个“x:y:z”字符串，用作显示给用户的版本号。
  # 对于应用程序的每个新版本，您将提供一个版本号，以区别于以前的版本。
  # 在Android上，它被用作“versionName”。
  # 在Xcode构建中，它被用作“CFBundleShortVersionString”
  # build_name: xxx
  # </project name/v1.2.3/>在发布版本中，此标志通过将Dart程序符号存储在主机上的单独文件中而不是存储在
  # 申请。标志的值应该是一个目录，可以在其中存储程序符号文件以供以后使用。这些符号文件包含
  # 表示飞镖堆叠痕迹所需的信息。对于使用此标志构建的应用程序，“flutr symbol”命令使用正确的程序符号
  # 文件是获取人类可读堆栈跟踪所必需的。
  # split_debug_info: xxx
  # 在发布版本中，此标志将删除标识符，并用随机值替换它们，以进行源代码混淆。这面旗子
  # 必须始终与“--split debug info”选项结合使用，值和原始标识符之间的映射存储在符号映射中在指定目录中创建。
  # 对于使用此标志构建的应用程序，带有正确程序符号文件的“flutter symbol”命令是需要获取人类可读的堆栈跟踪。
  #
  # 因为所有标识符都被重命名，所以对象.runtimeType, 类型toString, 枚举toString, Stacktrace.toString, 符号.toString（用于
  # 常量符号或运行时系统生成的符号）将返回模糊结果。任何依赖确切名称的代码或测试都将崩溃。
  # obfuscate: true
  # 可以作为字符串.fromEnvironment, 来自环境的布尔, 内部环境，和双.from环境施工人员。
  # 可以通过重复传递多个定义--省道定义多次。
  # dart_define: xxx
  # 性能度量文件flutter汇编性能和缓存信息将以JSON格式写入的文件的名称。
  # performance_measurement_file: xxx
  # 为iOS模拟器而不是设备生成模拟器。如果未指定，则将默认生成模式更改为调试。
  # simulator: true
  # 对应用程序包进行代码签名（仅适用于设备生成）。
  #（默认为打开）
  # codesign: true
  # exportOptionsPlist，一个键值对，放在项目assets目录下，build_type对应一个exportOptionsPlist。
  # 例如：
  # export_options:
  #   debug: ExportOptionsDebug.plist
  #   release: ExportOptionsRelease.plist
  export_options:
    debug: ExportOptionsDebug.plist
    release: ExportOptionsRelease.plist

# AppStore配置 详情请查看文档：https://help.apple.com/itc/apploader/#/apdATD1E53-D1E1A1303-D1E53A1126
app_store_config:
  # 您的用户名。
  apple_id: xxx
  # 指定文件的平台。{osx | ios | appletvos}
  type: ios
  # 密钥id
  api_key: xxx
  # Issuer id
  api_issuer: xxx
  # 您想让 Application Loader 以结构化的 XML 格式还是非结构化的文本格式返回输出信息。默认情况下，Application Loader 以文本格式返回输出信息。
  # [xml | normal]
  output_format: xml

# 蒲公英配置 详情请查看文档：https://www.pgyer.com/doc/view/api#paramInfo
pgy_config:
  # 路径
  url: http://www.pgyer.com/apiv2/app/upload
  # (必填) API Key
  _api_key: xxx
  # 用户Key，用来标识当前用户的身份，对于同一个蒲公英的注册用户来说，这个值在固定的。
  user_key: xxx
  # (必填)应用安装方式，值为(1,2,3)。1：公开，2：密码安装，3：邀请安装
  build_install_type: 1
  # (必填) 设置App安装密码
  build_password: ''
  # (选填) 版本更新描述，请传空字符串，或不传。
  # build_update_description: xxx
  # (选填) 应用名称
  # build_name: xxx
  # (选填)是否设置安装有效期，值为：1 设置有效时间， 2 长期有效，如果不填写不修改上一次的设置
  # build_install_date: xxx
  # (选填)安装有效期开始时间，字符串型，如：2018-01-01
  # build_install_start_date: xxx
  # (选填)安装有效期结束时间，字符串型，如：2018-12-31
  # build_install_end_date: xxx
  # (选填)所需更新的指定渠道的下载短链接，只可指定一个渠道，字符串型，如：abcd
  # build_channel_shortcut: xxx
  # android appKey
  android_app_key: xxx
  # ios appKey
  ios_app_key: xxx

# 钉钉配置 详情请查看文档：https://ding-doc.dingtalk.com/doc#/serverapi2/elzz1p
dingtalk_config:
  url: https://oapi.dingtalk.com/robot/send
  secret: xxx
  access_key: xxx
  # 首屏会话透出的展示内容
  title: 新的测试版本已发布
  # @所有人时：true，否则为：false（可选）
  is_at_all: false
  # 被@人的手机号（默认自动添加在text内容末尾，可取消自动化添加改为自定义设置，可选）
  at_mobiles:
    - xxx 
    - xxx 
  # 被@人的dingtalkId（可选）
  # at_dingtalk_ids:
  #   - xxx
  #   - xxx
  # 是否自动在text内容末尾添加@手机号，默认自动添加，可设置为False取消（可选）
  is_auto_at: true
```
