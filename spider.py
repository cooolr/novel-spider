import requests
import re
import urllib.parse
import os
import sys
import codecs


def request_get(proxy_url, req_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None

    try:
        response = requests.get(req_url, headers=headers, proxies=proxies)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"请求失败，请检查: {e}")
        sys.exit(1)


def search_book(proxy_url, keyword, book_index):
    keyword = urllib.parse.quote(keyword.encode("gbk"))
    search_url = f"https://www.69shu.com/modules/article/search.php?searchkey={keyword}&searchtype=all"
    body_string = request_get(proxy_url, search_url)
    re_book = re.compile(r'(?s)<h3>.*?<a href="(.*?).htm">(.*?)</a></h3>.*?<label>(.*?)</label>.*?<label>(.*?)</label>.*?<label>(.*?)</label>')
    book_list = re_book.findall(body_string)

    if len(book_list) == 0:
        re_book1 = re.compile(r'(?s)<h1><a href="(.*?).htm">(.*?)</a></h1>.*?<p>作者：.*?title="(.*?)".*?</a></p>.*?<p>分类：.*?title="(.*?)".*?</a></p>')
        book_list = re_book1.findall(body_string)
        re_status = re.compile(r'<meta property="og:novel:status" content="(.*?)"/>')
        book_status = re_status.search(body_string)
        if len(book_list) > 0:
            print(f"1. {book_list[0][1]} [{book_list[0][2]} {book_list[0][3]} {book_status[1]}]\n")
        else:
            print("抱歉，暂未收录此书。")
            sys.exit(1)
    else:
        for index, book in enumerate(book_list):
            print(f"{index+1}. {book[1]} [{book[2]} {book[3]} {book[4]}]\n")

    if book_index == 0:
        book_index = int(input("请输入要下载的小说序号: "))

    book_link = book_list[book_index-1][0]
    book_link = book_link.replace("/txt", "")
    return book_link + "/"


def get_node_list(proxy_url, node_url):
    body_string = request_get(proxy_url, node_url)
    re_title = re.compile(r'<title>(.*?)最新章节')
    book_name = re_title.search(body_string).group(1)
    re_node = re.compile(r'<li data-num="\d*?"><a href="(https://www.69shu.com/txt/.*?)">(.*?)</a></li>')
    node_list = re_node.findall(body_string)
    return book_name, node_list


def get_node_content(proxy_url, content_url):
    body_string = request_get(proxy_url, content_url)
    re_content = re.compile(r'(?s)<script>loadAdv\(2,0\);</script>(.*?)<script>loadAdv\(3,0\);</script>')
    text = re_content.search(body_string).group(1)
    text = text.replace('<div class="bottom-ad">', "")
    text = text.replace("</div>", "")
    text = text.replace("&nbsp;", " ")
    text = text.replace("<br />", "\n")
    text = text.replace("\r", "")
    text = text.replace("&emsp;", "  ")
    text = text.replace("(本章完)", "")
    return text


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-proxy", "--proxy", help="翻墙代理")
    parser.add_argument("-index", "--index", type=int, default=0, help="下载序号")
    parser.add_argument("keyword", help="搜索关键词")
    args = parser.parse_args()

    proxy_url = args.proxy
    book_index = args.index
    keyword = args.keyword
    node_url = search_book(proxy_url, keyword, book_index)
    book_name, node_list = get_node_list(proxy_url, node_url)

    file_name = book_name + ".txt"
    log_name = "." + book_name + ".log"

    exists_title = set()
    if os.path.exists(log_name):
        with open(log_name, "r") as log_file:
            for line in log_file:
                exists_title.add(line.strip())

    with open(file_name, "a", encoding="utf-8") as file_f, open(log_name, "a", encoding="utf-8") as log_f:
        total = len(node_list)
        for index, node in enumerate(node_list):
            title = node[1]
            if title in exists_title:
                continue
            content_url = node[0]
            content = get_node_content(proxy_url, content_url)
            content = "\n".join(content.strip().split("\n")[1:])

            content = f"\n\n\n\n\n\n\n\n{title}\n\n    {content}"

            file_f.write(content)
            file_f.flush()

            log_f.write(title + "\n")
            log_f.flush()

            print(f"{index+1}/{total} {title}")

    print(f"下载完成，文件名: {file_name}")


if __name__ == "__main__":
    main()

