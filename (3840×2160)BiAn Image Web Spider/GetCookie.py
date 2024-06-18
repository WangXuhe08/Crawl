# -*- coding: UTF-8 -*-
"""
@Author: 王散 Creative
@Time: 2022/3/28 16:01
@IDE_Name/Software: PyCharm
@File: GetCookie
"""
from selenium.webdriver import Chrome

web = Chrome()
web.get('https://pic.netbian.com/e/search/result/?searchid=1224')
cookie = web.get_cookies()
print(cookie)

