# -*- coding: UTF-8 -*-
"""@Author: 王散 Creative"""
from time import sleep
# from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from datetime import datetime
# from gooey import Gooey, GooeyParser
from os import system


def quit_():
    try:
        system("taskkill /f /im chromedriver.exe")
    except:
        # system('taskkill /im chrome.exe /F')
       pass
    else:
        pass


def _again_click(web_driver):
    web_driver.find_element(By.XPATH, '//*[@id="sn-bd"]/div/ul/li[2]/a').click()
    web_driver.find_element(By.XPATH, '//*[@id="J_SelectAll1"]/div/label').click()
    sleep(0.5)
    web_driver.find_element(By.XPATH, '//*[@id="J_Go"]').click()
    sleep(0.5)


def scan_code_inspect1(web):
    try:
        user_name = web.find_element(By.XPATH, '//*[@id="J_SiteNavLogin"]/div[1]/div/a').text
        print(f'>>扫码成功,欢迎-{user_name}-使用抢购脚本~~<<')
        return True
    except:
        print('<<<==操作错误,请您重新操作==>>>')
        return False


def scan_code_inspect2(web):
    try:
        user_name = web.find_element(By.XPATH, '//*[@id="J_SiteNavLogin"]/div[1]/div/a').text
        print(f'>>时间已到,正在为{user_name}全力抢购<<')
        return True
    except:
        print('<<<==操作错误,请您重新操作==>>')
        return False


def web_operation(web_driver):
        num = 0
        web_driver.find_element(By.XPATH, '//*[@id="J_MiniCart"]/div[1]/a').click()
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        web_driver.find_element(By.XPATH, '//*[@id="J_SelectAll1"]/div/label').click()
        sleep(0.2)
        web_driver.find_element(By.XPATH, '//*[@id="J_Go"]/span').click()
        sleep(0.5)
        while num < 20:
            try:
                web_driver.find_element(By.XPATH, '//*[@id="submitOrderPC_1"]/div/a[2]').click()
                break
            except:
                _again_click(web_driver)
                print("提交订单中...")
                num = num + 1
        print("抢购成功,请您付款~")
        return web_driver


def log(web_):
    web_.get('https://login.taobao.com/')
    web_.find_element(By.XPATH, '//*[@id="login"]/div[1]/i').click()
    print('<<<==请您在20s内打开淘宝扫码,我们将为您继续进行抢购工作==>>>')
    sleep(20)
    scan_code_inspect1(web_)
    # web_.find_element(By.XPATH, '//*[@id="J_MiniCart"]/div[1]/a').click()
    return web_


# def time_(timer: str):
#     # print('输入预购发售时间,格式如"2022-02-08 16:00"')
#     # timer = input('==>>')
#     return timer


# @Gooey
# def main():
#     parser = GooeyParser(description="抢购小能手_wangsan")
#     parser.add_argument('timer', help='输入预购发售时间,格式如"2022-02-08 16:00"')
#     args = parser.parse_args()
#     good_time = time_(args.timer)
#     return good_time
def str_deal(str_time):
    str_time = list(str_time)
    if int(str_time[11]) != 0:
         int(str_time[11] + str_time[12]) - 1

    #     str_time[15] = str(int(str_time[15]) - 1)
    #     # str_time[14] = '5'
    #     # str_time[15] = '9'
    #     str_time = ''.join(str_time)
    #     str_time = str_time + ':59.122342'
    #     # print(str_time)
    # else:
    str_time[15] = '9'
    str_time[14] = '5'
    return str_time


if __name__ == '__main__':
    # times = main()
    times_num = 0
    print('输入预购发售时间,格式如"2022-02-08 16:00"')
    timer = input('==>>')
    # options = webdriver.ChromeOptions()
    # # 处理SSL证书错误问题
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--ignore-ssl-errors')
    # # 忽略无用的日志
    # options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    # webs = webdriver.Chrome(options=options)
    times = str_deal(timer)
    # times = timer + ':00.000000'
    webs = Chrome()
    sleep(0.8)
    webs = log(webs)
    while True:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        print(now)
        if now >= times:
            while True:
               # try:
                if scan_code_inspect2(webs):
                    web = web_operation(webs)
                    sleep(30)
                    quit_()
                    break
                times_num = times_num + 1
                if times_num >= 20:
                    quit_()
                    break
               # except:
               #      print('错误..')
            break
