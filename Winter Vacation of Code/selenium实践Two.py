# -*- coding: UTF-8 -*-
"""
@Author: 王散 Creative
@Time: 2022/1/24 21:47
@IDE_Name/Software: PyCharm
@File: selenium实践Two
"""
from selenium.webdriver import Chrome
from threading import Timer
# def get_latest_cookie():
#     cookie = {}
#     web_page = Chrome()
#     web_page.get('https://pic.netbian.com/new/')
#     cookie_list = web_page.get_cookies()
#     for item in cookie_list:
#         cookie.update(cookie, **item)
#     return cookie
# if __name__ == '__main__':
#     cookie = get_latest_cookie()
#     header = {
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.469"
#                       "2.99 Safari/537.36",
#         "cookie": f"{cookie}"
#     }
def Print():
    print('一次了')
    t = Timer(5, Print)
    t.start()
if __name__ == '__main__':
    Print()