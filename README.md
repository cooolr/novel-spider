# 69shu-spider

69书屋是我阅读了很多年的小说网站，国内无法访问。

#### 前置任务

需要先在 [69书屋](https://www.69shu.com/) 搜索小说并进入到完整目录页，比如 [https://www.69shu.com/48089/](https://www.69shu.com/48089/) ，反正也是要搜索一下看小说存不存在的。

#### 使用说明

1. 安装依赖: `pip install requests`

2. 查看说明: `python main.py --help`
``` bash
usage: main.py [-h] [--proxy PROXY] node_url

positional arguments:
  node_url       小说目录页url.

optional arguments:
  -h, --help     show this help message and exit
  --proxy PROXY  翻墙代理.
```

3. 下载小说: 
``` bash
# 墙内下载
python main.py --proxy http://127.0.0.1:7890 https://www.69shu.com/48089/

# 墙外下载
python main.py https://www.69shu.com/48089/
```
#### 特性

1. 支持断点下载
2. 支持章节更新
3. 对网站友好，单线程慢慢下

#### 程序打包

1. 安装依赖: `pip install pyinstaller`

2. 执行打包:
``` bash
pyinstaller --onefile \
            --paths= `python -c "import os.path, requests; print(os.path.dirname(requests.__file__))"` \
main.py
```

4. 可执行文件下载小说:
``` bash
./dist/main https://www.69shu.com/48089/
```
