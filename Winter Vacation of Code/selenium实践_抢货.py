# -*- coding: UTF-8 -*-
"""
@Author: 王散 Creative
@Time: 2022/2/8 13:45
@IDE_Name/Software: PyCharm
@File: selenium实践_抢货
"""
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import datetime
import threading
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
# print(now)


class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

        def run(self):
            self.result = self.func(*self.args)  # 在执行函数的同时，把结果赋值给result,
            # 然后通过get_result函数获取返回的结果

        def get_result(self):
            try:
                return self.result
            except Exception as e:
                return None


def sleep_():
    time.sleep(60)
    return True


def in_put():
    In = input()
    return In


def scan_code_inspect(web):
    try:
        user_name = web.find_element(By.XPATH, '//*[@id="J_Col_Main"]/div/div[1]/div/div[1]/div[1]/div/div[1]/a/em').text
        print(f'>>扫码成功,欢迎-{user_name}-使用抢购脚本~~')
        return True
    except:
        print('<<<==操作错误,请您重新操作==>>')
        return False


def sleep_or_input(webr):
    result = []
    threads = []
    for i in range(10):
        active1 = threading.Thread(target=sleep_, args=(i,))
        active1.start()
        active2 = threading.Thread(target=in_put, args=(i,))
        active2.start()
    for t in threads:
        t.join()  # 一定执行join,等待子进程执行结束，主进程再往下执行
        result.append(t.get_result())
        print(result)
    if result[0]:
        print('超时')
    if result[1] == '\n':
        scan_code_inspect(webr)


def web_operation(web_driver):
    web_driver.get('https://login.taobao.com/')
    web_driver.find_element(By.XPATH, '//*[@id="login"]/div[1]/i').click()
    print('<<<==请您在一分钟内打开淘宝扫码,扫码完成后输入回车,我们将为您继续进行抢购工作==>>>')
    sleep_or_input(web_driver)


if __name__ == '__main__':
    webs = Chrome()
    times = '2022-2-8 16:00:00.000000'
    web_operation(webs)

