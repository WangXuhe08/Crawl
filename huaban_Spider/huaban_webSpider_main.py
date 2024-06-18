# -*- coding: UTF-8 -*-
"""
@Author: 王散 Creative
@Time: 2022/3/25 18:50
@IDE_Name/Software: PyCharm
@File: huaban_webSpider_main
"""
from requests import get
import re
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from time import sleep
from random import randint


# from os import system
def get_json(frequency, since):
    try:
        header = {
            "accept": "application/json, text/plain, */*",
            "cookie": "sid=s%3A1cz_qAWxXOsd0PjfW_rpTsf8N8iZRYc8.6vIyNqGDV2DO4Fs3UzlaQQ6tbYPSf3bA65V3w8i0XC8; UM_distinctid="
                      "17fc095032e312-0f44045ed8f6bb-9771a3f-144000-17fc095032fe8c; Hm_lvt_d4a0e7c3cd16eb58a65472f40e7ee543="
                      "1648203466; user_device_id=1a4a0c2ad5fb4dc0b27b9834a85ee28e; user_device_id_timestamp=1648203465602; "
                      "Hm_up_d4a0e7c3cd16eb58a65472f40e7ee543=%7B%22version%22%3A%7B%22value%22%3A%222.0.0%22%2C%22scope%22%"
                      "3A1%7D%7D; uid=33589522; Hm_lpvt_d4a0e7c3cd16eb58a65472f40e7ee543=1648207624",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
        }
        RespOne = get(f'https://api.huaban.com/discovery/?limit={frequency}&max={since}', headers=header, timeout=20)
        sleep(1.5)
        RuleOne = re.compile(r'.*?"pin_id":(?P<key>.*?),', re.S)
        AnalysisOne = RuleOne.finditer(RespOne.text)
        return AnalysisOne
    except:
        pass


def data_handle(AnalysisOne):
    try:
        global id_handle
        past_id = []
        for item in AnalysisOne:
            try:
                past_id.append(int(item.group('key')))
            except:
                for _item_ in range(len(item.group('key'))):
                    id_handle = item.group('key').replace('"', '')
                    id_handle = id_handle.replace('}', '')
                    id_handle = id_handle.replace('{', '')
                past_id.append(int(id_handle))
        return past_id
    except:
        pass


def get_json_two(arg_id_paths):
    try:
        RespJsonList = []
        header = {
            "accept": "application/json, text/plain, */*",
            "cookie": "sid=s%3A1cz_qAWxXOsd0PjfW_rpTsf8N8iZRYc8.6vIyNqGDV2DO4Fs3UzlaQQ6tbYPSf3bA65V3w8i0XC8; UM_distinctid="
                      "17fc095032e312-0f44045ed8f6bb-9771a3f-144000-17fc095032fe8c; Hm_lvt_d4a0e7c3cd16eb58a65472f40e7ee543="
                      "1648203466; user_device_id=1a4a0c2ad5fb4dc0b27b9834a85ee28e; user_device_id_timestamp=1648203465602; "
                      "Hm_up_d4a0e7c3cd16eb58a65472f40e7ee543=%7B%22version%22%3A%7B%22value%22%3A%222.0.0%22%2C%22scope%22%"
                      "3A1%7D%7D; uid=33589522; Hm_lpvt_d4a0e7c3cd16eb58a65472f40e7ee543=1648207624",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
        }
        for arg_id_path in arg_id_paths:
            Resp_two = get(f"https://api.huaban.com/pins/{arg_id_path}?pins=20", headers=header, timeout=20)
            sleep(1.5)
            RespJsonList.append(Resp_two.json())
        return RespJsonList
    except:
        pass


def data_handle_two(JsonList):
    try:
        UrlList = []
        NameList = []
        for item in JsonList:
            try:
                Url_key = list(list(list(item.values())[0].values())[4].values())[1]
                Name = list(list(item.values())[0].values())[8]
                NameList.append(Name)
                UrlList.append(Url_key)
            except:
                pass
        return UrlList, NameList
    except:
        pass


def download_image(Url_and_Name):
    global Image_file
    header = {
        "cookie": "sid=s%3A1cz_qAWxXOsd0PjfW_rpTsf8N8iZRYc8.6vIyNqGDV2DO4Fs3UzlaQQ6tbYPSf3bA65V3w8i0XC8; UM_distinctid="
                  "17fc095032e312-0f44045ed8f6bb-9771a3f-144000-17fc095032fe8c; Hm_lvt_d4a0e7c3cd16eb58a65472f40e7ee543="
                  "1648203466; user_device_id=1a4a0c2ad5fb4dc0b27b9834a85ee28e; user_device_id_timestamp=1648203465602; "
                  "Hm_up_d4a0e7c3cd16eb58a65472f40e7ee543=%7B%22version%22%3A%7B%22value%22%3A%222.0.0%22%2C%22scope%22%"
                  "3A1%7D%7D; uid=33589522; Hm_lpvt_d4a0e7c3cd16eb58a65472f40e7ee543=1648207624",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    }
    try:
        Frequency = 0
        for item in Url_and_Name[0]:
            RespImage = get(f'https://hbimg.huabanimg.com/{item}_fw658/format/webp', headers=header, timeout=20)
            sleep(1.5)
            try:
                number = randint(1, 999999999)
                Image_file = open(
                    f'D:\python_write_file\爬虫NumberTwo\Image\花瓣/{Url_and_Name[1][Frequency]}({number}).png', 'wb')
            except:
                number = randint(1, 999999999)
                Image_file = open(f'D:\python_write_file\爬虫NumberTwo\Image\花瓣/无法处理{number}.png', 'wb')
                Image_file.write(RespImage.content)
            Image_file.close()
            print(f"{Url_and_Name[1][Frequency]}~~=>下载完毕")
            Frequency += 1
    except:
        pass


def main(args):
    try:
        Analysis_Json = get_json(args[0], args[1])
        arg_id_paths = data_handle(Analysis_Json)
        RespJsonList = get_json_two(arg_id_paths)
        Url_and_NameTuple = data_handle_two(RespJsonList)
        download_image(Url_and_NameTuple)
    except:
        pass


def main_speed(args):
    try:
        with ThreadPoolExecutor(1000) as ThreadPool:
            for j in range(10000000):
                ThreadPool.submit(main, (args[0], args[1],))
                args[0] *= args[1]
                args[1] *= args[0]
    except:
        pass


if __name__ == '__main__':
    # path_image_List = listdir('D:\python_write_file\爬虫NumberTwo\Image\花瓣/')
    try:
        Since = 1
        Limit = 100
        with ProcessPoolExecutor(5) as ProcessPool:
            for i in range(1, 10000000000):
                ProcessPool.submit(main_speed, (Limit, Since,))
                # Limit += Since
                Since *= Limit
                Limit *= Since
    except:
        pass
    input("Press <Enter>")
    # system('shutdown -s -t 10')
