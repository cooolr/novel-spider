# 69shu-spider
69书屋小说爬虫

69书屋是我阅读了很多年的小说网站，国内无法访问。

#### 前置任务

需要先在 [69书屋](https://www.69shu.com/) 搜索小说并进入到完整目录页，比如 [https://www.69shu.com/48089/](https://www.69shu.com/48089/) 

#### 使用说明

1. 安装依赖: `pip install requests`

2. 查看说明: `python main.py --help`
```
usage: main.py [-h] [--proxy PROXY] node_url

positional arguments:
  node_url       小说目录页url.

optional arguments:
  -h, --help     show this help message and exit
  --proxy PROXY  翻墙代理.
```

3. 下载小说: 
```
# 墙内下载
python main.py --proxy http://127.0.0.1:7890 https://www.69shu.com/48089/

# 墙外下载
python main.py https://www.69shu.com/48089/
```
#### 特性

1. 支持断点下载
2. 支持章节更新
