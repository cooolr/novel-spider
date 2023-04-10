import os
import re
import sys

import requests
from requests.exceptions import RequestException
import argparse

# 解析命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('--proxy', help='翻墙代理.')
parser.add_argument('node_url', help='小说目录页url.')
args = parser.parse_args()

node_url = args.node_url

# 设置代理
proxy = args.proxy
proxies = {"https": proxy} if proxy else {}

# 设置请求头
headers = {
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}

# 获取小说目录列表
def get_node_list(url):
    try:
        r = requests.get(url, headers=headers, proxies=proxies)
        r.encoding = 'gbk'
        book_name = re.findall('<title>(.*?)最新章节', r.text)[0]
        node_list = re.findall('<li data-num="\d*?"><a href="(https://www.69shu.com/txt/.*?)">(.*?)</a></li>', r.text)
        return book_name, node_list
    except Exception as e:
        print(f"获取目录页失败，或许你需要指定翻墙代理: {e}")
        sys.exit(1)

# 获取小说正文
def get_node_text(url):
    try:
        r = requests.get(url, headers=headers, proxies=proxies)
        r.encoding = 'gbk'
        text = re.findall('<script>loadAdv\(2\,0\);</script>(.*?)<script>loadAdv\(3\,0\);</script>', r.text, re.S)[0]
        text = text.replace('<div class="bottom-ad">','').replace('</div>','')
        text = text.replace('&nbsp;',' ').replace('<br />','\n').replace('&emsp;','  ').replace('(本章完)','')
        return text
    except Exception as e:
        print(f"获取章节失败，请检查错误后重试: {e}")
        sys.exit(1)

# 写入文件
def write_to_file(filename, text):
    with open(filename, 'a+', encoding='gbk') as f:
        f.write(text)
        f.flush()

# 更新日志
def update_log(log_file, title):
    with open(log_file, 'a+', encoding='gbk') as f:
        f.write(title + "\n")

def main():
    book_name, node_list = get_node_list(node_url)
    filename = f"{book_name}.txt"
    # 实现断点下载和更新功能
    log_file = f".{book_name}.log"
    exists_title = set()
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='gbk') as f:
            exists_title = set(f.read().splitlines())

    for index, (url, title) in enumerate(node_list):
        if title in exists_title:
            continue
        text = get_node_text(url)
        write_to_file(filename, text)
        update_log(log_file, title)
        print(f"{index+1}/{len(node_list)} {title}")

if __name__ == '__main__':
    main()

