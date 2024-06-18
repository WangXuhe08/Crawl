# -*- coding: UTF-8 -*-
"""
@Author: 王散 Creative
@Time: 2022/3/27 16:03
@IDE_Name/Software: PyCharm
@File: (3840×2160)BiAn Image Web Spider
"""
import re
from requests import get
from urllib.request import HTTPCookieProcessor, build_opener
from re import *
from concurrent.futures import ThreadPoolExecutor
from http import cookiejar


def GetCookie():
    CookieOne = cookiejar.CookieJar()
    handle = HTTPCookieProcessor(CookieOne)
    opener = build_opener(handle)
    response = opener.open('www.baidu.com')


def requestOne(number):
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.484"
                      "4.84 Safari/537.36",
        "cookie": f"{cookie}",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,ap"
                  "plication/signed-exchange;v=b3;q=0.9"
    }
    try:
        RespOne = get(url=f'https://pic.netbian.com/e/search/result/index.php?page={number}&searchid=1224',
                      headers=header, timeout=20)
        RespOne.encoding = 'GBK'
        return RespOne.text
    except:
        print(f"{number}主页面访问超时")
        return 0


def Data_Fine_Handle(Text):
    RuleOne = compile(r'<ul class="clearfix">(.*?)</ul>', re.S)
    RuleTwo = compile(r'<li><a href="(.*?)".*?<b>', re.S)
    AnalysisOne = RuleOne.findall(Text)
    AnalysisTwo = RuleTwo.findall(AnalysisOne[0])
    Inside_Page_Tail_Url.append(AnalysisTwo)
    return Inside_Page_Tail_Url


def requestTwo(Tail_Url):
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,appli"
                  "cation/signed-exchange;v=b3;q=0.9",
        "cookie": f"{cookieOne}",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844."
                      "84 Safari/537.36"
    }
    try:
        RespTwo = get(url=f'https://pic.netbian.com/{Tail_Url}', headers=header, timeout=30)
        RespTwo.encoding = 'GBK'
        return RespTwo.text
    except:
        print(f"{Tail_Url}访问超时")
        return 0


def Data_Fine_Handle_Of_Inside(Text):
    RuleOne = compile(r'id="img"><img src="(.*?)" data-pic=', re.S)
    RuleTwo = compile(r'id="img">.*?alt="(.*?)".*?></a>', re.S)
    AnalysisOne = RuleOne.findall(Text)
    AnalysisTwo = RuleTwo.findall(Text)
    DownloadTailUrl.append(AnalysisOne[0])
    ImageNames.append(AnalysisTwo[0])
    return DownloadTailUrl, ImageNames


# def Download_Image(ImageDownloadTailUrl_And_ImageName):
#     header = {
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844."
#         "84 Safari/537.36"
#     }
#     ImageUrlTxT.close()
# try:
#     Image_Data = get(url=f'https://pic.netbian.com{ImageDownloadTailUrl_And_ImageName[0]}', headers=header, timeout=40)
#     try:
#         Image_File = open(f'D:\python_write_file\爬虫NumberTwo\Image\彼岸网爬的好图3/{ImageDownloadTailUrl_And_ImageName[1]}.jpg', 'wb')
#     except:
#         Image_File = open(f'D:\python_write_file\爬虫NumberTwo\Image\彼岸网爬的好图3/无法处理{randint(1,9999999)}.jpg', 'wb')
#     Image_File.write(Image_Data.content)
#     Image_File.close()
#     print(f'{ImageDownloadTailUrl_And_ImageName[1]}>>下载完成')
# except:
#     print(f"{ImageDownloadTailUrl_And_ImageName[1]}下载超时")
def main():
    with ThreadPoolExecutor(1000) as ThreadPool:
        for item in range(400, 643):
            Outside_Page_Origin_Code = ThreadPool.submit(requestOne, item)
            Tail_Url_List = Data_Fine_Handle(Outside_Page_Origin_Code.result())
    print("\n643个主页面数据细加工全部完成,每个详情页url尾部已导入列表,进入每个页面请求..")
    with ThreadPoolExecutor(12661) as ThreadPool:
        for item_inside in Tail_Url_List:
            for Page_Url in item_inside:
                Inside_Page_Origin_Code = ThreadPool.submit(requestTwo, Page_Url)
                DownloadTail_Url_And_Name_List = Data_Fine_Handle_Of_Inside(Inside_Page_Origin_Code.result())
    print("\n12661个详情页已请求完毕..")

    print('\n页面分析完毕,图片下载地址已全部保存到列表..')

    ImageUrlTxT = open('D:\python_write_file\爬虫NumberTwo\Image/Url.txt', 'a')
    for item_download in DownloadTail_Url_And_Name_List[0]:
        ImageUrlTxT.write(f'{item_download}\n')
    print("\n已全部下载完毕")


if __name__ == "__main__":
    cookie = input("输入彼岸图网最新刷新的cookie..>:")
    cookieOne = input("输入详情页最新的cookie..>:")
    Inside_Page_Tail_Url = []
    DownloadTailUrl = []
    ImageNames = []
    main()
    input(">>Press <Enter>..<<")
