# -*- coding: UTF-8 -*-
"""
@Author: 王散 Creative
@Time: 2022/10/10 14:52
@File: BrowserActive.py
"""
from time import sleep


class BrowserActive:
    def __init__(self):
        pass

    @staticmethod
    def scroll_to_bottom(driver, Frequency):
        """控制浏览器自动拉倒底部"""

        js = "return action=document.body.scrollHeight"
        # 初始化现在滚动条所在高度为0
        height = 0
        # 当前窗口总高度
        new_height = driver.execute_script(js)
        for _ in range(Frequency):
            if height < new_height:
                # 将滚动条调整至页面底部
                driver.execute_script(f'window.scrollTo(0,{new_height})')
                height = new_height
                sleep(0.4)
                new_height = driver.execute_script(js)
            else:
                sleep(2)
                if height < new_height:
                    print("Flag--BrowserActive--continue")
                    continue
                else:
                    print("Flag--BrowserActive--return -1")
                    return -1

    @staticmethod
    def scroll_to_bottom_fixed(driver):
        while 1:
            driver.execute_script("var q=document.documentElement.scrollTop=10000000")
            sleep(1)


if __name__ == '__main__':
    pass