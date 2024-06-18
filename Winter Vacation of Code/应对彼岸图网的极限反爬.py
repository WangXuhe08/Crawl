# -*- coding: UTF-8 -*-
"""
@Author: 王散 Creative
@Time: 2022/1/22 18:50
@IDE_Name/Software: PyCharm
@File: 应对彼岸图网的极限反爬
"""
import requests
from lxml import etree
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from threading import Timer
from multiprocessing import Lock
from selenium.webdriver import Chrome

cookie = None
def get_latest_cookie():
    cookie = {}
    web_page = Chrome()
    web_page.get('https://pic.netbian.com/new/')
    cookie_list = web_page.get_cookies()
    for item in cookie_list:
        cookie.update(cookie, **item)
    return cookie


def task(url, cookie):
    t.start()
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.469"
                      "2.99 Safari/537.36",
        "cookie": f"{cookie}"
    }
    Squence = 0
    resp1 = requests.get(url=url, headers=header)
    resp1.encoding = 'gbk'
    tree = etree.HTML(resp1.text)
    analysis1 = tree.xpath('//*[@id="main"]/div[3]/ul/li//a/@href')
    analysis2 = tree.xpath('//*[@id="main"]/div[3]/ul/li/a/b/text()')
    for ItemTwo in analysis1:
        url_two_page = 'https://pic.netbian.com' + ItemTwo
        resp2 = requests.get(url=url_two_page, headers=header)
        resp2.encoding = 'gbk'
        tree_two = etree.HTML(resp2.text)
        analysis3 = tree_two.xpath('//*[@id="img"]/img/@src')
        for ItemThree in analysis3:
            url_image_page = 'https://pic.netbian.com' + ItemThree
            resp3 = requests.get(url=url_image_page, headers=header)
            image_file = open(f'D:\python_write_file\爬虫NumberTwo\Image\彼岸网爬的好图2\\{analysis2[Squence]}.jpg', 'wb')
            image_file.write(resp3.content)
            image_file.close()
            print(f'{analysis2[Squence]}==>爬取完毕')
            Squence = Squence + 1


if __name__ == "__main__":
    t = Timer(600, get_latest_cookie)
    with ProcessPoolExecutor(50) as Process_Pool:
        for item in range(1, 1261):
            if item == 1:
                Process_Pool.submit(task, 'https://pic.netbian.com/new/')
            else:
                Process_Pool.submit(task, f'https://pic.netbian.com/new/index_{item}.html')
