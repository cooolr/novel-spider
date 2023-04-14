# novel-spider

这个书源是我阅读了很多年的小说网站，国内无法访问，需要翻墙。

#### 使用说明

1. [Release页](https://github.com/cooolr/novel-spider/releases/tag/v1.3) 下载对应平台的可执行文件
    - Windows 64位: [spider_windows_amd64](https://github.com/cooolr/novel-spider/releases/download/v1.3/spider_windows_amd64.exe)
    - Linux 64位: [spider_linux_amd64](https://github.com/cooolr/novel-spider/releases/download/v1.3/spider_linux_amd64)
    - Mac 64位: [spider_darwin_amd64](https://github.com/cooolr/novel-spider/releases/download/v1.3/spider_darwin_amd64)
    - Android 64位: [spider_linux_arm64](https://github.com/cooolr/novel-spider/releases/download/v1.3/spider_linux_arm64)

2. 下载小说（以Windows示例）:

    下载完可执行文件后，在文件所在文件夹的路径栏输入 `cmd` 并回车，进入到cmd命令行界面

    输入
    ``` bash
    # 墙内下载，需要指定翻墙代理
    spider_windows_amd64.exe --proxy http://127.0.0.1:7890 诛仙

    # 墙外下载
    spider_windows_amd64.exe 诛仙
    ```

    输出
    ``` bash
    1. 诛仙长生传 [摩林若寒 修真武侠 全本]

    2. 一剑诛仙，找爸爸的女儿震惊封神 [小炸鸡 官场职场 全本]

    3. 诛仙 [萧鼎 修真武侠 全本]

    4. 从诛仙开始复制诸天 [简单旋律 官场职场 全本]

    ...

    请输入要下载的小说序号: 
    ```

    如果不想每次输入序号，使用 `--index` 指定默认序号
    ``` bash
    spider_windows_amd64.exe --index 1 诛仙
    ```

3. 在Termux使用说明
    
    下载 `[spider_linux_arm64](https://github.com/cooolr/novel-spider/releases/download/v1.3/spider_linux_arm64)` 到 `/sdcard/Downloads` 目录
    
    ``` bash
    # 去到家目录
    cd ~
    # 复制spider_linux_arm64到当前目录
    cp /sdcard/Downloads/spider_linux_arm64 spider
    # 设置可执行权限
    chmod 755 spider
    # 移动到bin目录
    mv spider ~/../usr/bin/
    # 在任意路径下载小说
    spider 诛仙
    ```

#### 特性

1. 关键词搜索
2. 支持断点下载
3. 支持章节更新
4. 对网站友好，单线程慢慢下
