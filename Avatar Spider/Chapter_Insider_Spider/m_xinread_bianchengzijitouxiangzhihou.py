# -*- coding: UTF-8 -*-
"""
@Author: 王散 Creative
@Time: 2022/4/14 13:22
@IDE_Name/Software: PyCharm
@File: m_xinread_bianchengzijitouxiangzhihou
"""
from tongrenwang_cc import getheader, request_one, etree
def Handle_One(Text):
    treeOne = etree.HTML(Text)
    Chapter_name = treeOne.xpath('/html/body/div[2]/div[1]/h1/text()')
    Chapter_content = treeOne.xpath('/html/body/div[2]/div[2]/p/text()')
    Chapter_next_url = treeOne.xpath('//*[@id="nextbtn"]/@href')
    return Chapter_name, Chapter_content, Chapter_next_url
if __name__ == '__main__':
    url = 'https://m.xingread.cn/shenmaread/17200/1704273.html'
    header_first = getheader(url)
    OriginCode = request_one((url, header_first,))
    Chapter_information = Handle_One(OriginCode)


