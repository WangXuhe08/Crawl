# -*- coding: UTF-8 -*-
"""
@Author: 王散 Creative
@Time: 2022/10/10 11:36
@File: main.py
"""
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from BrowserActive import BrowserActive, sleep
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor
from requests import get
from threading import RLock
from os import mkdir
from re import findall
from random import randint


class SpiderXHR_Offset_Main(BrowserActive):
    def __init__(self):
        super(SpiderXHR_Offset_Main, self).__init__()

    @staticmethod
    def option(prox):
        options = Options()

        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--proxy-server={}'.format(prox.proxy))

        options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        options.add_argument('--hide-scrollbars')  # 隐藏滚动条，应对一些特殊页面
        options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片，提升运行速度
        # options.add_argument('--headless')  # 浏览器不提供可视化界面。Linux下如果系统不支持可视化不加这条会启动失败
        return options

    def main(self):
        # 开启代理
        BMPserver = Server(r'D:\browsermob-proxy\bin\browsermob-proxy.bat', {'port': 8739})
        BMPserver.start()
        BMPproxy = BMPserver.create_proxy()

        # 配置selenium, 配置代理启动webdriver
        options = self.option(BMPproxy)
        web = webdriver.Chrome(options=options)

        # 获取返回内容
        url = "https://www.duitang.com/"
        BMPproxy.new_har("lagou", options={'captureContent': False})

        # 模拟浏览器
        web.get(url)
        sleep(2)

        # 查看更多
        web.find_element(By.XPATH, '//*[@id="content"]/div[3]/div[2]/div/div[1]/div[2]/div[3]').click()
        sleep(2)

        # 滑到底部
        flag_scroll = BrowserActive.scroll_to_bottom(driver=web, Frequency=300)
        if flag_scroll == -1:
            print('Flag--main')
            BrowserActive.scroll_to_bottom(driver=web, Frequency=100)
        else:
            pass
        # BrowserActive.scroll_to_bottom_fixed(web)

        # 数据处理
        result = BMPproxy.har
        with open("XHR_offset_url.txt", 'a', errors='ignore') as f:
            for item1 in result['log']['entries']:
                if item1['request']['queryString']:
                    if item1['request']['queryString'][0]['name'] == 'offset':
                        f.write(item1['request']['url'])
                        f.write('\n')

        BMPproxy.close()
        BMPserver.stop()
        web.quit()


class JsonRequestAndHandle:
    def __init__(self):
        self.resource_ids = []
        self.img_urls = {}

    def OffsetRequest(self, url):
        RespOne = get(url)
        for item in RespOne.json()['data']['feeds']:
            lock.acquire()
            self.resource_ids.append(item['resource_id'])
            lock.release()

    def OffsetRequestMain(self):
        with open('XHR_offset_url.txt', 'r') as f:
            offsetUrls = f.readlines()
            with ThreadPoolExecutor(100) as thread_pool:
                for item in offsetUrls:
                    thread_pool.submit(self.OffsetRequest, item)

    def DetailRequest(self, url):
        RespOne = get(url)

        for item in RespOne.json()['data']['blogs']:
            self.img_urls.setdefault(f"{RespOne.json()['data']['desc']}", []).append(item['photo']['path'])

    def DetailRequestMain(self):
        with ThreadPoolExecutor(200) as thread_pool:
            for item in self.resource_ids:
                url = f'https://www.duitang.com/napi/vienna/atlas/detail/?atlas_id={item}'
                thread_pool.submit(self.DetailRequest, url)
        return self.img_urls


class ImagesDownload:
    def __init__(self):
        pass

    @staticmethod
    def image_download(ImageUrl):
        print(ImageUrl)
        RespOne = get(ImageUrl)
        with open(f'D:\SpiderSynthesis\com.duitang.www/{randint(1, 99999999999999)}.jpg', 'wb') as f:
            f.write(RespOne.content)
        # desc = ImageInfo[0].replace('\n', '')
        # regex_str = ".*?([\u4E00-\u9FA5]+).*?"
        # desc = findall(regex_str, desc)
        # desc = ' '.join(desc)
        # print(ImageInfo)
        # try:
        #     mkdir(f"D:\SpiderSynthesis\com.duitang.www/{desc}")
        #     Folder = desc
        # except Exception or BaseException as error:
        #     print(error)
        #     Folder = str(randint(1, 9999999999))
        #     mkdir(f"D:\SpiderSynthesis\com.duitang.www/{Folder}")
        #
        # RespOne = get(ImageInfo[1])
        # with open(f'D:\SpiderSynthesis\com.duitang.www/{Folder}/{randint(1, 9999999999)}.jpg', 'wb') as f:
        #     f.write(RespOne.content)

    def image_downloadMain(self, ImageInfos):
        with ThreadPoolExecutor(400) as ThreadPool:
            for Info in ImageInfos.items():
                for url in Info[1]:
                    ThreadPool.submit(self.image_download, url)


if __name__ == '__main__':
    inFlag = input('Is it the first time to use(Y/N):')
    lock = RLock()
    if inFlag == 'Y':
        spider_main = SpiderXHR_Offset_Main()

        spider_main.main()

        json_request_and_handle = JsonRequestAndHandle()
        imagesInformation = json_request_and_handle.DetailRequestMain()

        images_download = ImagesDownload()
        images_download.image_downloadMain(imagesInformation)

    elif inFlag == "N":
        json_request_and_handle = JsonRequestAndHandle()

        json_request_and_handle.OffsetRequestMain()
        imagesInformation = json_request_and_handle.DetailRequestMain()

        # pprint(imagesInformation)
        images_download = ImagesDownload()
        images_download.image_downloadMain(imagesInformation)
