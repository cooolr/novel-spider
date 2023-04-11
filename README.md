# 69shu-spider

69书屋是我阅读了很多年的小说网站，国内无法访问，需要翻墙。

#### 前置任务

需要先在 [69书屋](https://www.69shu.com/) 搜索小说并进入到完整目录页，比如 [https://www.69shu.com/48089/](https://www.69shu.com/48089/) ，反正也是要搜索一下看小说存不存在的。

#### 使用说明

1. [Release页](https://github.com/cooolr/69shu-spider/releases/tag/v1.1) 下载对应平台的可执行文件
    - Windows 64位: [69shu-spider_windows_amd64](https://github.com/cooolr/69shu-spider/releases/download/v1.1/69shu-spider_windows_amd64.exe)
    - Linux 64位: [69shu-spider_linux_amd64](https://github.com/cooolr/69shu-spider/releases/download/v1.1/69shu-spider_linux_amd64)
    - Mac 64位: [69shu-spider_darwin_amd64](https://github.com/cooolr/69shu-spider/releases/download/v1.1/69shu-spider_darwin_amd64)
    - Android 64位: [69shu-spider_linux_arm64](https://github.com/cooolr/69shu-spider/releases/download/v1.1/69shu-spider_linux_arm64)

2. 下载小说（以Windows示例）:

下载完可执行文件69shu-spider_windows_amd64.exe后，在文件所在文件夹的路径栏输入 `cmd` 并回车，进入到cmd命令行界面

``` bash
# 墙内下载，需要指定翻墙代理
69shu-spider_windows_amd64.exe --proxy http://127.0.0.1:7890 https://www.69shu.com/48089/

# 墙外下载
69shu-spider_windows_amd64.exe https://www.69shu.com/48089/
```
#### 特性

1. 支持断点下载
2. 支持章节更新
3. 对网站友好，单线程慢慢下


