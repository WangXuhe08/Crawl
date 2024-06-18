# -*- coding: UTF-8 -*-
"""
@Author: 王散 Creative
@Time: 2022/2/9 20:35
@IDE_Name/Software: PyCharm
@File: 关闭chromedriver
"""
from os import system

system("taskkill /f /im chromedriver.exe")
system('taskkill /im chrome.exe /F')