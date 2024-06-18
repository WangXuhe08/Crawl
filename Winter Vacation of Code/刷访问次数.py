# -*- coding: UTF-8 -*-
"""
@Author: 王散 Creative
@Time: 2022/2/9 13:05
@IDE_Name/Software: PyCharm
@File: 刷访问次数
"""
import requests
from fake_useragent import UserAgent
from time import sleep

def main():
    ua = UserAgent()
    header = {"User-Agent": ua.random}
    # header = {
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.47"
    #                   "58.82 Safari/537.36"
    # }
    for item in range(1, 99999999):
        resp = requests.get(url=url, headers=header)
        print(resp)
        sleep(1)

if __name__ == "__main__":
    url = 'https://blog.csdn.net/superwang04/article/details/125022110'
    main()
