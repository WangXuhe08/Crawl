# -*- coding: UTF-8 -*-
"""
@Author: 王散 Creative
@Time: 2022/3/13 10:10
@IDE_Name/Software: PyCharm
@File: Spider_bi_an_imageWeb_NEW
2022.3.12 因写网站无图可用想在图网爬些能用的风景图片,想用寒假写的几个代码,却发现参差不齐,没写注释,不知那个是新版.
没有办法,另写一个!
以后尽量写注释吧 ! ! !
该版本还可进行优化,将每个requests的代码写为一个函数,传入url,encoding的值,User-Agent在函数内部设置即可,可以大大简化代码,提高运行速度
url拼接代码也是如此,传入尾部url参数,返回完整,真正做到模块化.每个函数都实现一个完整的功能
"""
from requests import get
from lxml import etree  # 注意导入 lxml 而非xml ,xml包里可没有etree.HTML方法哦
from time import sleep
from concurrent.futures import ThreadPoolExecutor
# from fake_useragent import UserAgent


#   在页面一进行的操作,返回一个含有图片名称的列表
def pageone_get_imagename(respOne):
    treeOne_name = etree.HTML(respOne.text)
    analysis_name_list = treeOne_name.xpath('//*[@id="main"]/div[3]/ul/li/a/b/text()')
    return analysis_name_list


#   在页面一进行的操作,返回一个每个图片url的尾部部分
def pageone(useragent_of_Object, urlOne):
    headerOne = {"User-Agent": useragent_of_Object, "cookie": "__yjs_duid=1_05d06a7e411e6d2016e7cd13a48a53f21642925312707; Hm_lvt_14b14198b6e26157b7eba06b390ab763=1642925315; Hm_lvt_526caf4e20c21f06a4e9209712d6a20e=1642925468,1643028479; Hm_lvt_c59f2e992a863c2744e1ba985abaea6c=1647136744; zkhanecookieclassrecord=%2C53%2C; yjs_js_security_passport=68822e3cba60d5c871c2e74222b51e828fa67151_1647153663_js; Hm_lpvt_c59f2e992a863c2744e1ba985abaea6c=1647153664"}
    # urlOne = "https://pic.netbian.com/4kfengjing/"
    respOne = get(url=urlOne, headers=headerOne)
    respOne.encoding = "GBK"
    name_list = pageone_get_imagename(respOne)
    treeOne = etree.HTML(respOne.text)
    analysisOne = treeOne.xpath('//*[@id="main"]/div[3]/ul/li/a/@href')
    return analysisOne, name_list


#   进行进入页面2的准备工作,既对页面一操作后返回的含有每个图片详情页的尾部url进行拼接,返回一个含有完整可请求的url的列表
def enter_pagetwo_prepare(pageone_of_useragent_object, url):
    tailurl_list = pageone(pageone_of_useragent_object, url)
    for item_enter_pagetwo in range(len(tailurl_list[0])):
        tailurl_list[0][item_enter_pagetwo] = 'https://pic.netbian.com' + tailurl_list[0][item_enter_pagetwo]
    return tailurl_list


#   在得到每个图片详情页的完整url后,将进行对每个图片页进行请求分析获取到图片下载地址的尾部url,并将它们组合到一个列表里,返回这个列表
def pagetwos_of_operation(enter_pagetwo_prepare_of_parameter, url):
    pagetwos_tail_url_list = []
    header = {"UserAgent": enter_pagetwo_prepare_of_parameter, "cookie": "__yjs_duid=1_05d06a7e411e6d2016e7cd13a48a53f21642925312707; Hm_lvt_14b14198b6e26157b7eba06b390ab763=1642925315; Hm_lvt_526caf4e20c21f06a4e9209712d6a20e=1642925468,1643028479; Hm_lvt_c59f2e992a863c2744e1ba985abaea6c=1647136744; zkhanecookieclassrecord=%2C53%2C; yjs_js_security_passport=68822e3cba60d5c871c2e74222b51e828fa67151_1647153663_js; Hm_lpvt_c59f2e992a863c2744e1ba985abaea6c=1647153664"}
    pagetwos_url_list = enter_pagetwo_prepare(enter_pagetwo_prepare_of_parameter, url)
    for item_pagetwo in pagetwos_url_list[0]:
        sleep(1)
        resptwo = get(url=item_pagetwo, headers=header)
        resptwo.encoding = 'GBK'
        treetwo = etree.HTML(resptwo.text)
        analysistwo = treetwo.xpath('//*[@id="img"]/img/@src')
        pagetwos_tail_url_list.append(analysistwo[0])
    return pagetwos_tail_url_list, pagetwos_url_list[1]


#   得到含有图片下载的尾部url的列表后将其每一个元素进行拼接,得到一个含有完整下载地址的url的列表,返回这个列表
def joint(pagetwos_of_operation_parameter, url):
    pagetwos_tail_url_list = pagetwos_of_operation(pagetwos_of_operation_parameter, url)
    for item_joint in range(len(pagetwos_tail_url_list[0])):
        pagetwos_tail_url_list[0][item_joint] = 'https://pic.netbian.com' + pagetwos_tail_url_list[0][item_joint]
    return pagetwos_tail_url_list


#   在得到含有图片完整下载地址的列表后,将其遍历requests并保存到文件
def download_image(ua, url):
    number = 0
    header = {"User-Agent": ua, "cookie": "__yjs_duid=1_05d06a7e411e6d2016e7cd13a48a53f21642925312707; Hm_lvt_14b14198b6e26157b7eba06b390ab763=1642925315; Hm_lvt_526caf4e20c21f06a4e9209712d6a20e=1642925468,1643028479; Hm_lvt_c59f2e992a863c2744e1ba985abaea6c=1647136744; zkhanecookieclassrecord=%2C53%2C; yjs_js_security_passport=68822e3cba60d5c871c2e74222b51e828fa67151_1647153663_js; Hm_lpvt_c59f2e992a863c2744e1ba985abaea6c=1647153664"}
    download_image_url_list = joint(ua, url)
    for item_down in download_image_url_list[0]:
        sleep(1)
        resp_image = get(url=item_down, headers=header)
        image_file = open(f"D:\python_write_file\爬虫NumberTwo\Image\彼岸网爬的好图2\Scenery_4K_image of BIAN/{download_image_url_list[1][number]}.jpg", 'wb')
        image_file.write(resp_image.content)
        image_file.close()
        print(f"{download_image_url_list[1][number]}下载完毕")
        number = number + 1


if __name__ == "__main__":
    UA_ = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    # with ThreadPoolExecutor(50) as ThreadPool:
    for item in range(1, 207):
        if item == 1:
            urls = "https://pic.netbian.com/4kfengjing/index.html"
            # ThreadPool.submit(download_image, )
            download_image(UA_, urls)
        elif item >= 2:
            urls = f"https://pic.netbian.com/4kfengjing/index_{item}.html"
            # ThreadPool.submit(download_image, )
            download_image(UA_, urls)

