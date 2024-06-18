# -*- coding: UTF-8 -*-
"""
@Author: 王散 Creative
@Time: 2022/1/24 19:20
@IDE_Name/Software: PyCharm
@File: Selenium实践
"""
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import requests
from lxml import etree
from concurrent.futures import ProcessPoolExecutor
# web = Chrome()
# web.get('https://pic.netbian.com/new/')
# web.find_element(By.XPATH, '//*[@id="main"]/div[4]/a[1]').click()
# # 教程上说这样可以关掉旧页面,但是发现最新版本的selenium打开新窗口方式是替换而非新开一个窗口,所以不用下面的方法了
# # web.switch_to.window((web.window_handles[0]))
# # web.close()
# web.find_element(By.XPATH, '//*[@id="main"]/div[3]/ul/li[1]/a/img').click()
# web.switch_to.window((web.window_handles[1]))
# image_download_tail_path = web.find_element(By.XPATH, '//*[@id="img"]/img').get_attribute('src')
# image_name = web.find_element(By.XPATH, '//*[@id="main"]/div[2]/div[1]/div[1]/h1').text
# resp_image = requests.get(url=image_download_tail_path)
# with open(f'D:\python_write_file\爬虫NumberTwo\Image\彼岸网爬的好图2\\{image_name}.jpg', 'wb') as image_file:
#     image_file.write(resp_image.content)
# print(image_name, '完毕')
def task_two(url):
    resp1 = requests.get(url=url, headers=header)
    resp1.encoding = 'gbk'
    tree = etree.HTML(resp1.text)
    analysis1 = tree.xpath(f'//*[@id="main"]/div[3]/ul/li/a/b/text()')
    return analysis1
def task_one(url_one_part):
    image_name = task_two(url_one_part)
    web = Chrome()
    web.get(url_one_part)
    for image_num in range(1, 21):
        web.find_element(By.XPATH, f'//*[@id="main"]/div[3]/ul/li[{image_num}]/a/img').click()
        web.switch_to.window((web.window_handles[1]))
        image_download_tail_path = web.find_element(By.XPATH, '//*[@id="img"]/img').get_attribute('src')
        resp_image = requests.get(url=image_download_tail_path)
        with open(f'D:\python_write_file\爬虫NumberTwo\Image\彼岸网爬的好图2\\{image_name[image_num-1]}.jpg', 'wb') as image_file:
            image_file.write(resp_image.content)
        print(image_name[image_num-1], '=>>完毕')
        web.close()
        web.switch_to.window((web.window_handles[0]))
if __name__ =='__main__':
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.469"
                      "2.99 Safari/537.36",
        "cookie": "__yjs_duid=1_05d06a7e411e6d2016e7cd13a48a53f21642925312707; Hm_lvt_14b14198b6e26157b7eba06b390ab763" 
                  "=1642925315; Hm_lvt_526caf4e20c21f06a4e9209712d6a20e=1642925468,1643028479; Hm_lpvt_526caf4e20c21f06" 
                  "a4e9209712d6a20e=1643029975"
    }
    # with ProcessPoolExecutor(2) as Pool:
    for page in range(1, 20):
        if page == 1:
            # Pool.submit(task_one, 'https://pic.netbian.com/new/index.html')
            task_one('https://pic.netbian.com/new/index.html')
            # else:


