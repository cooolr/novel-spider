package main

import (
    "bytes"
    "flag"
    "fmt"
    "golang.org/x/text/encoding/simplifiedchinese"
    "golang.org/x/text/transform"
    "io/ioutil"
    "net/http"
    "net/url"
    "os"
    "regexp"
    "strings"
)

func requestGet(proxyUrl, reqUrl string) string{
    // 创建HTTP请求对象
    req, _ := http.NewRequest("GET", reqUrl, nil)
    // 设置请求头
    req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    // 创建HTTP客户端对象
    proxyURL, _ := url.Parse(proxyUrl)
    client := http.Client{
        Transport: &http.Transport{
            Proxy: http.ProxyURL(proxyURL),
        },
    }
    // 发送HTTP请求
    res, err := client.Do(req)
    if err != nil {
        fmt.Printf("%s请求失败，请检查: %v\n", reqUrl, err)
        os.Exit(1)
    }
    defer res.Body.Close()
    if res.StatusCode != http.StatusOK {
        fmt.Printf("%s请求失败，status_code: %d\n", reqUrl, res.StatusCode)
        os.Exit(1)
    }
    // GBK编码转换UTF-8编码
    gbkBytes, err := ioutil.ReadAll(res.Body)
    reader := transform.NewReader(bytes.NewReader(gbkBytes), simplifiedchinese.GBK.NewDecoder())
    bodyBytes, err := ioutil.ReadAll(reader)
    if err != nil {
        fmt.Printf("转换编码失败: %v\n", err)
        os.Exit(1)
    }
    bodyString := string(bodyBytes)
    return bodyString
}

func getNodeList(proxyUrl, nodeUrl string) (string, [][]string) {
    bodyString := requestGet(proxyUrl, nodeUrl)
    // 获取小说名称
    r := regexp.MustCompile(`<title>(.*?)最新章节`)
    bookName := r.FindStringSubmatch(bodyString)[1]
    // 获取小说目录
    nodeUrlRe := regexp.MustCompile(`<li data-num="\d*?"><a href="(https://www.69shu.com/txt/.*?)">(.*?)</a></li>`)
    nodeList := nodeUrlRe.FindAllStringSubmatch(bodyString, -1)
    return bookName, nodeList
}

func getNodeContent(proxyUrl, contentUrl string) string {
    bodyString := requestGet(proxyUrl, contentUrl)
    // 获取小说正文
    reText := regexp.MustCompile(`<script>loadAdv\(2,0\);</script>(?s:(.*?))<script>loadAdv\(3,0\);</script>`)
    text := reText.FindStringSubmatch(bodyString)[1]
    text = strings.ReplaceAll(text, `<div class="bottom-ad">`, "")
    text = strings.ReplaceAll(text, "</div>", "")
    text = strings.ReplaceAll(text, "&nbsp;", " ")
    text = strings.ReplaceAll(text, "<br />", "\n")
    text = strings.ReplaceAll(text, "&emsp;", "  ")
    text = strings.ReplaceAll(text, "(本章完)", "")
    return text
}

func main() {
    // 解析命令行参数
    var proxyUrl string
    var args []string
    flag.StringVar(&proxyUrl, "proxy", "", "翻墙代理")
    flag.Parse()
    args = flag.Args()
    if len(args) == 0 {
        fmt.Println("请输入小说完整目录页url")
        os.Exit(1)
    }
    nodeUrl := args[0]
    // 获取小说名称和目录列表
    bookName, nodeList := getNodeList(proxyUrl, nodeUrl)
    // 定义小说文件名和日志名
    fileName := bookName + ".txt"
    logName := "." + bookName + ".log"
    // 实现断点下载和更新功能
    existsTitle := make(map[string]bool)
    if _, err := os.Stat(logName); err == nil {
        // 如果日志文件存在，读取其中已存在的章节名称
        logBytes, _ := ioutil.ReadFile(logName)
        lines := strings.Split(string(logBytes), "\n")
        for _, line := range lines {
            if line != "" {
                existsTitle[line] = true
            }
        }
    }
    // 下载未下载的章节内容
    fileF, _ := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
    logF, _ := os.OpenFile(logName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
    defer fileF.Close()
    defer logF.Close()
    total := len(nodeList)
    for index, node := range nodeList {
        title := node[2]
        if existsTitle[title] {
            continue
        }
        contentUrl := node[1]
        content := getNodeContent(proxyUrl, contentUrl)
        // 写入章节内容到文件
        if _, err := fileF.WriteString(content); err != nil {
            fmt.Printf("写入文件失败: %v\n", err)
            fileF.Close()
            os.Exit(1)
        }
        fileF.Sync()
        // 记录已下载的章节标题到日志文件
        if _, err := logF.WriteString(title + "\n"); err != nil {
            fmt.Printf("写入日志失败: %v\n", err)
            logF.Close()
            os.Exit(1)
        }
        logF.Sync()
        fmt.Printf("%d/%d %s\n", index, total, title)
    }
    fmt.Printf("下载完成，文件名: %s\n", fileName)
}
