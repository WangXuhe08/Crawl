# -*- coding: UTF-8 -*-
"""
@Author: 王散 Creative
@Time: 2022/3/3 22:35
@IDE_Name/Software: PyCharm
@File: selenium抢货京东
"""
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from datetime import datetime
# from os import system


def analysis_time():
    print('输入预购发售时间,格式如"2022-02-08 16:00"')
    timer = input('==>')

    while 1:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        if timer <= now:
            return True
        else:
            print(now)


def log_and_front(web_):
    web_.get('https://www.jd.com/')
    web_.find_element(By.XPATH, '//*[@id="ttbar-login"]/a[1]').click()
    print('<<<==请您在20s内手机打开京东app扫码,我们将为您继续进行抢购工作==>>>')
    sleep(15)
    # scan_code_inspect1(web_)
    web_.find_element(By.XPATH, '//*[@id="settleup"]/div[1]').click()
    web_.switch_to.window((web.window_handles[1]))
    # web_.find_element(By.XPATH, '//*[@id="cart-body"]/div[2]/div[4]/div[1]/div/input').click()
    # web_.find_element(By.XPATH, '//*[@id="cart-body"]/div[2]/div[5]/div[1]/div/input').click()
    # web_.find_element(By.XPATH, '//*[@id="cart-body"]/div[2]/div[13]/div/div[2]/div/div/div/div[2]/div[2]/div/div[1]/a').click()
    return web_


def after_click(web_):
    while 1:
        try:
            web_.find_element(By.XPATH, '//*[@id="cart-body"]/div[2]/div[6]/div/div[2]/div/div/div/div[2]/div[1]/div[1]/input').click()
        except:
            continue
    sleep(0.1)
    while 1:
        try:
            web_.find_element(By.XPATH, '//*[@id="cart-body"]/div[2]/div[13]/div/div[2]/div/div/div/div[2]/div[2]/div/div[1]/a').click()
            web_.find_element(By.XPATH, '//*[@id="order-submit"]').click()
        except:
            continue

# //*[@id="cart-body"]/div[2]/div[4]/div[1]/div/input
# //*[@id="cart-body"]/div[2]/div[5]/div[1]/div/input


if __name__ == "__main__":
    web = Chrome()
    web = log_and_front(web)
    if analysis_time():
        after_click(web)
