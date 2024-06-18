# -*- coding: UTF-8 -*-
"""
@Author: 王散 Creative
@Time: 2022/4/12 22:17
@IDE_Name/Software: PyCharm
@File: Main
"""
from requests import get
from selenium.webdriver import Chrome, ChromeOptions
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
# 获取请求头信息
def getheader(url):
    cookie_value = ''
    FrequencyIndex = 0
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.484"
        "4.84 Safari/537.36",
     }
    cookieValues = []
    cookieNames = []
    option = ChromeOptions()
    option.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    web = Chrome()
    web.get(url)
    cookies = web.get_cookies()

    for item in cookies:
        FrequencyName = 0
        FrequencyValue = 0
        for itemOne in list(item.keys()):
            if itemOne == "value":
                cookieValues.append(list(item.values())[FrequencyValue])
                break
            else:
                FrequencyValue += 1

        for itemTwo in list(item.keys()):
            if itemTwo == "name":
                cookieNames.append(list(item.values())[FrequencyName])
                break
            else:
                FrequencyName += 1

    for itemThree in cookieNames:
        # 末尾分号根据实际情况决定是去是留
        cookie_value = cookie_value + f"{itemThree}={cookieValues[FrequencyIndex]};"
        # 两种方案取消注释根据情况选择一种
        header["Cookie"] = cookie_value + 'boomolastsearchtime=1649996494'
        # header["Cookie"] = cookie_value
        FrequencyIndex += 1
    return header


def request_one(url_header):
    try:
        RespOne = get(url_header[0], url_header[1], timeout=50)
    except:
        header = getheader(url_header[0])
        RespOne = get(url_header[0], header, timeout=40)
    # 编码根据实际情况决定
    RespOne.encoding = 'GB18030'
    return RespOne.text

def Handle_Outsider(Text):
    treeOne = etree.HTML(Text)
    AnalysisOne = treeOne.xpath("/html/body/div[3]/div[3]/ul/li/a/@href")
    AnalysisTwo = treeOne.xpath('/html/body/div[3]/div[2]/div[2]/h1/text()')
    return AnalysisOne, AnalysisTwo
def Handle_Insider(Text):
    treeTwo = etree.HTML(Text)
    AnalysisTwo = treeTwo.xpath('//*[@id="readContent_set"]/div[2]/div[2]/text()')
    if AnalysisTwo[0].isspace() == 1 or AnalysisTwo[0] == '\r\n                 ':
        AnalysisTwo = treeTwo.xpath('//*[@id="readContent_set"]/div[2]/div[2]/p/text()')
        return AnalysisTwo
    elif 0:
        pass
    else:
        return AnalysisTwo
def FileOperation(contents, name):
    novel = open(rf'D:\python_write_file\爬虫NumberTwo\novel/{name}.txt', 'a', encoding='gb18030')
    for item in contents:
        if item.isspace() == 1:
            continue
        novel.write(item)
        novel.write('\n')
    novel.close()
    print("一章节完毕")
    return 0

if __name__ == '__main__':
    input_url = ''
    while input_url != 'Q':
        input_url = input(" 小说章节页面url >('输入Q退出'): ")
        if input_url == 'Q':
            exit(-1)
        else:
            header_first = getheader(input_url)
            Origin_Code = request_one((input_url, header_first, ))
            ChapterUrls = Handle_Outsider(Origin_Code)
            with ThreadPoolExecutor(500) as Thread:
                for chapter in ChapterUrls[0]:
                    # 所加网站主域名根据实际情况而定
                    chapter = "http://www.trxs.cc" + chapter
                    # chapter = " http://tongrenquan.org" + chapter
                    ChapterPage_OriginCode = Thread.submit(request_one, (chapter, header_first,))
                    content_all = Handle_Insider(ChapterPage_OriginCode.result())
                    FileOperation(content_all, ChapterUrls[1][0])
            print(f"{ChapterUrls[1][0]} >下载完毕")
