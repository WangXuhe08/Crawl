# -*- coding: UTF-8 -*-
"""
@Author: 王散 Creative
@Time: 2022/3/29 22:18
@IDE_Name/Software: PyCharm
@File: temp
"""
from random import randint
from AvatarOutsideUrl_NameSpider import *
from os import mkdir

def txt_handle():
    InsideUrls = []
    InsideNames = []
    File_txt = open('D:\python_write_file\爬虫NumberTwo\Image\Avatar/InsideUrl_Name.txt', 'r', encoding='UTF-8')
    ReadTxt = File_txt.read()
    for item_ in ReadTxt.split('---WangXuHe_Split_Line\n')[:-1]:
        url_nameList = item_.split('---WangXuHe_Split---')
        InsideUrls.append(url_nameList[0])
        InsideNames.append(url_nameList[1])
    return InsideUrls, InsideNames

def inside_request(url):
    global RespOne, AnalysisThree
    for item_ in range(1, 10):
        try:
            RespOne = get(url=url, headers=header_fresh, timeout=30)
            RespOne.encoding = "UTF-8"
            RuleThree = compile(r'<li class="tx-img"><a href="(.*?)".*?src=', re.S)
            AnalysisThree = RuleThree.findall(RespOne.text)
            break
        except:
            print("!!请求超时!! -将重新请求")
            print(url, RespOne.status_code)
    if RespOne.status_code >= 400:
        print("\n请求状态码异常  -结论: 被反爬 , 获取最新header中...\n")
        header_new = get_header()
        print("已获得最新header..开始重新请求..\n")
        for item_ in range(1, 10):
            try:
                RespOne = get(url=url, headers=header_new, timeout=30)
            except:
                print("请求超时 -重新请求..")
        RespOne.encoding = "UTF-8"
        RuleThree = compile(r'<li class="tx-img"><a href="(.*?)".*?src=', re.S)
        AnalysisThree = RuleThree.findall(RespOne.text)
    if AnalysisThree:
        if len(AnalysisThree) == 0:
            print("\n页面源码 正则 分析异常 ,获取最新header中...\n")
            header_new = get_header()
            print("已获得最新header..开始重新请求并进行正则分析..\n")
            for item_ in range(1, 10):
                try:
                    RespOne = get(url=url, headers=header_new, timeout=30)
                except:
                    print("请求超时 -重新请求..")
            RespOne.encoding = "UTF-8"
            RuleThree = compile(r'<ul class="artCont cl">(.*?)<div class="tagsPl">', re.S)
            RuleFour = compile(r'<img src="(.*?)".*?</li>', re.S)
            AnalysisTwo = RuleThree.findall(RespOne.text)
            AnalysisThree = RuleFour.findall(AnalysisTwo[0])
            if len(AnalysisThree) != 0:
                return AnalysisThree
            else:
                print("三次纠错后, 仍然错误, 请检查网址或其他参数是否正确 -结论: 纠己错")
        else:
            return AnalysisThree

def image_download_request(url):
    for item_ in range(1, 10):
        try:
            Image_Content = get(url=f'https:{url}', timeout=30, headers=header_fresh)
        except:
            print("下载超时,即将重新请求下载")
        if Image_Content.status_code >= 400:
            print("请求状态码异常 -重新请求..")
        else:
            return Image_Content.content

def file_operation(image_content, dir_name):
    try:
        Image_File = open(f'{dir_name}/{randint(0,99999)}.jpg', 'wb')
        Image_File.write(image_content)
        Image_File.close()
    except:
        print("下载失败 -文件打开失败")
        return 0


if __name__ == "__main__":
    # main_outside()
    Urls_Names = txt_handle()
    header_fresh = get_header()
    with ThreadPoolExecutor(100000) as ThreadPool:
        for Frequency in range(0, 68719):
            Avatar_url = ThreadPool.submit(inside_request, Urls_Names[0][Frequency])
            try:
                path = rf"D:\python_write_file\爬虫NumberTwo\Image\Avatar/{Urls_Names[1][Frequency]}"
                mkdir(path)
            except:
                try:
                    path = rf"D:\python_write_file\爬虫NumberTwo\Image\Avatar/{Urls_Names[1][Frequency]}{randint(1, 999999)}"
                    mkdir(path)
                except:
                    path = rf"D:\python_write_file\爬虫NumberTwo\Image\Avatar/无法处理{randint(1, 999999)}"
                    mkdir(path)
            for item in Avatar_url.result():
                ImageContent = ThreadPool.submit(image_download_request, item)
                file_operation(ImageContent.result(), path)
            print(f'{Urls_Names[1][Frequency]}合集下载完毕')
    input("Press <Enter>")