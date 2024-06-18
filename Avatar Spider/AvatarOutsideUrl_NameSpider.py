# -*- coding: UTF-8 -*-
"""
@Author: 王散 Creative
@Time: 2022/3/29 14:35
@IDE_Name/Software: PyCharm
@File: Avatar Spider
"""
import re
from requests import get
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver import Chrome
from re import compile

#   通过selenium获得cookie, 并将其拼为header
def get_header():
    web = Chrome()
    web.get('https://www.woyaogexing.com/touxiang/index.html')
    cookieOne = web.get_cookie('__gads')
    cookieOne = dict(cookieOne)
    cookieTwo = web.get_cookie('Hm_lvt_a077b6b44aeefe3829d03416d9cb4ec3')
    cookieTwo = dict(cookieTwo)
    cookieThree = web.get_cookie('Hm_lpvt_a077b6b44aeefe3829d03416d9cb4ec3')
    cookieThree = dict(cookieThree)
    HeaderFist = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844."
                      "84 Safari/537.36",
        "Cookie": f"__gads={list(cookieOne.values())[6]};Hm_lvt_a077b6b44aeefe3829d03416d9cb4ec3=1648534805,1648535429;Hm_lpvt_a077b6b4"
                  f"4aeefe3829d03416d9cb4ec3={list(cookieThree.values())[5]}"
    }
    return HeaderFist


# 外层页面的请求与粗分析
def outside_page_request(index_and_header):
    if index_and_header[0] == 1:
        for item in range(1, 10):
            try:
                RespOne = get(url='https://www.woyaogexing.com/touxiang/index.html', timeout=30, headers=index_and_header[1])
                RespOne.encoding = 'UTF-8'
                RuleOne = compile(r'class="img"(.*?)data-id=', re.S)
                AnalysisOne = RuleOne.findall(RespOne.text)
                break
            except:
                print("!!请求超时!! -将重新请求")
        if RespOne.status_code >= 400:
            print("\n请求状态码异常  -结论: 被反爬 , 获取最新header中...\n")
            header_new = get_header()
            print("已获得最新header..开始重新请求..\n")
            RespOne = get(url='https://www.woyaogexing.com/touxiang/index.html', timeout=30,
                          headers=header_new)
            RespOne.encoding = 'UTF-8'
            RuleOne = compile(r'class="img"(.*?)data-id=', re.S)
            AnalysisOne = RuleOne.findall(RespOne.text)
            if AnalysisOne:
                if len(AnalysisOne) <= 2:
                    print("\n页面源码 正则 分析异常 ,获取最新header中...\n")
                    header_new = get_header()
                    print("已获得最新header..开始重新请求并进行正则分析..\n")
                    RespOne = get(url='https://www.woyaogexing.com/touxiang/index.html', timeout=30,
                                  headers=header_new)
                    RespOne.encoding = 'UTF-8'
                    RuleOne = compile(r'class="img"(.*?)data-id=', re.S)
                    AnalysisOne = RuleOne.findall(RespOne.text)
                    if len(AnalysisOne) >= 2:
                        return AnalysisOne
                    else:
                        print("三次纠错后, 仍然错误, 请检查网址或其他参数是否正确 -结论: 纠己错")
        else:
            return AnalysisOne
    else:
        for item in range(1, 10):
            try:
                RespOne = get(url=f'https://www.woyaogexing.com/touxiang/index_{index_and_header[0]}.html', timeout=30,
                              headers=index_and_header[1])
                RespOne.encoding = 'UTF-8'
                RuleOne = compile(r'class="img"(.*?)data-id=', re.S)
                AnalysisOne = RuleOne.findall(RespOne.text)
                break
            except:
                print("!!请求超时!! -将重新请求")
        if RespOne.status_code >= 400:
            print("\n请求状态码异常  -结论: 被反爬 , 获取最新header中...\n")
            header_new = get_header()
            print("已获得最新header..开始重新请求..\n")
            RespOne = get(url=f'https://www.woyaogexing.com/touxiang/index_{index_and_header[0]}.html', timeout=30,
                          headers=index_and_header[1])
            RespOne.encoding = 'UTF-8'
            RuleOne = compile(r'class="img"(.*?)data-id=', re.S)
            AnalysisOne = RuleOne.findall(RespOne.text)
            if AnalysisOne:
                if len(AnalysisOne) <= 2:
                    print("\n页面源码 正则 分析异常 ,获取最新header中...\n")
                    header_new = get_header()
                    print("已获得最新header..开始重新请求并进行正则分析..\n")
                    RespOne = get(url=f'https://www.woyaogexing.com/touxiang/index_{index_and_header[0]}.html',
                                  timeout=30, headers=index_and_header[1])
                    RespOne.encoding = 'UTF-8'
                    RuleOne = compile(r'class="img"(.*?)data-id=', re.S)
                    AnalysisOne = RuleOne.findall(RespOne.text)
                    if len(AnalysisOne) >= 2:
                        return AnalysisOne
                    else:
                        print("三次纠错后, 仍然错误, 请检查网址或其他参数是否正确 -结论: 纠己错")
        else:
            return AnalysisOne


def Code_Fine(Txt):
    RuleTwo = compile(r'class="imgTitle".*?title="(.*?)".*?</a>', re.S)
    RuleThree = compile(r'<a href="(.*?)" class="imgTitle".*?</span><a', re.S)
    AnalysisTwo = RuleTwo.findall(Txt)
    AnalysisThree = RuleThree.findall(Txt)
    if len(AnalysisTwo) >= 20 and len(AnalysisThree) >= 20:
        return AnalysisTwo, AnalysisThree
    else:
        print('每页布局已变化 , 将调整 正则 规则')
        RuleTwo = compile(r'target"_blank>(.*?)</a>', re.S)
        RuleThree = compile(r'<a href="(.*?)" class="imgTitle".*?</span><a', re.S)
        AnalysisTwo = RuleTwo.findall(Txt)
        AnalysisThree = RuleThree.findall(Txt)
        return AnalysisTwo, AnalysisThree


def reserve_url_name(url_List, name_List, Frequency, File):
    for index in url_List:
        File.write(f'https://www.woyaogexing.com{index}---WangXuHe_Split---{name_List[Frequency]}---WangXuHe_Split_Line\n')
        Frequency += 1
    return 0

def main_outside():
    header = get_header()
    File = open('D:\python_write_file\爬虫NumberTwo\Image\Avatar/InsideUrl_Name.txt', 'a', encoding='UTF-8')
    with ThreadPoolExecutor(3600) as ThreadPool:
        for PageIndex in range(1, 2840):
            Crude_Page_Origin_Code = ThreadPool.submit(outside_page_request, (PageIndex, header,))
            InsideUrl_Name = Code_Fine("".join(Crude_Page_Origin_Code.result()))
            reserve_url_name(InsideUrl_Name[1], InsideUrl_Name[0], 0, File)
        print('\n详情页Url与Name已全部保存到txt')

if __name__ == '__main__':
    main_outside()