# -*- coding: UTF-8 -*-
"""
@Author: 王散 Creative
@Time: 2022/3/28 16:27
@IDE_Name/Software: PyCharm
@File: DownLoad
"""
from concurrent.futures import ThreadPoolExecutor
from requests import get
from random import randint
def GET():
    ImageUrl = open('D:\python_write_file\爬虫NumberTwo\Image/Url.txt', 'r')
    ImageName = open('D:\python_write_file\爬虫NumberTwo\Image/Name.txt', 'r')
    ImageUrlList = ImageUrl.read().split('\n')
    ImageNameList = ImageName.read().split('\n')
    return ImageUrlList, ImageNameList
def download(Url_Name_):
    try:
        Resp = get(f'https://pic.netbian.com/{Url_Name_[0]}', timeout=20)

        try:
            File = open(f'D:\python_write_file\爬虫NumberTwo\Image\彼岸图(横屏)1/{Url_Name_[1]}.jpg', 'wb')
            File.write(Resp.content)
        except:
            File = open(f'D:\python_write_file\爬虫NumberTwo\Image\彼岸图(横屏)1/{randint(1,999999)}.jpg', 'wb')
            File.write(Resp.content)
        File.close()
        print(f'{Url_Name_[1]}==>下载完毕')
    except:
        print(f"{Url_Name_[1]}下载超时")
        return 0
# def task1():
#     for item1 in range(0, 1071):
#         download(Url_Name[0][item1], Url_Name[1][item1])
# def task2():
#     for item2 in range(1071, 1071*2):
#         download(Url_Name[0][item2], Url_Name[1][item2])
# def task3():
#     for item3 in range(1071*2, 1071*3):
#         download(Url_Name[0][item3], Url_Name[1][item3])
# def task4():
#     for item4 in range(1071*3, 1071*4):
#         download(Url_Name[0][item4], Url_Name[1][item4])
# def task5():
#     for item5 in range(1071*4, 1071*5):
#         download(Url_Name[0][item5], Url_Name[1][item5])
# def task6():
#     for item6 in range(1071*5, 1071*6):
#         download(Url_Name[0][item6], Url_Name[1][item6])
# def task7():
#     for item7 in range(1071*6, 1071*7):
#         download(Url_Name[0][item7], Url_Name[1][item7])
# def task8():
#     for item8 in range(1071*7, 1071*8):
#         download(Url_Name[0][item8], Url_Name[1][item8])
# def task9():
#     for item9 in range(1071*8, 1071*9):
#         download(Url_Name[0][item9], Url_Name[1][item9])
# def task10():
#     for item10 in range(1071*9, 1071*10):
#         download(Url_Name[0][item10], Url_Name[1][item10])
# def task11():
#     for item11 in range(1071*10, 1071*11):
#         download(Url_Name[0][item11], Url_Name[1][item11])
# def task12():
#     for item12 in range(1071*11, 1071*12):
#         download(Url_Name[0][item12], Url_Name[1][item12])
# def task13():
#     for item13 in range(1071*12, 1071*13):
#         download(Url_Name[0][item13], Url_Name[1][item13])
# def task14():
#     for item14 in range(1071*13, 1071*14):
#         download(Url_Name[0][item14], Url_Name[1][item14])
# def task15():
#     for item15 in range(1071*14, 1071*15):
#         download(Url_Name[0][item15], Url_Name[1][item15])
# def task16():
#     for item16 in range(1071*15, 1071*16):
#         download(Url_Name[0][item16], Url_Name[1][item16])
# def task17():
#     for item17 in range(1071*16, 1071*17):
#         download(Url_Name[0][item17], Url_Name[1][item17])
# def task18():
#     for item18 in range(1071*17, 1071*18):
#         download(Url_Name[0][item18], Url_Name[1][item18])
# def task19():
#     for item19 in range(1071*18, 1071*19):
#         download(Url_Name[0][item19], Url_Name[1][item19])
# def task20():
#     for item20 in range(1071*19, 1071*20):
#         download(Url_Name[0][item2], Url_Name[1][item20])
# def task21():
#     for item21 in range(1071*20, 1071*21):
#         download(Url_Name[0][item21], Url_Name[1][item21])
# def task22():
#     for item22 in range(1071*21, 1071*22):
#         download(Url_Name[0][item22], Url_Name[1][item22])
if __name__ == "__main__":
    Url_Name = GET()
    with ThreadPoolExecutor(5000) as ThreadPool:
        for item1 in range(0, 12852):
            ThreadPool.submit(download, (Url_Name[0][item1], Url_Name[1][item1],))
        # ProcessPool.submit(task1)
        # ProcessPool.submit(task2)
        # ProcessPool.submit(task3)
        # ProcessPool.submit(task4)
        # ProcessPool.submit(task5)
        # ProcessPool.submit(task6)
        # ProcessPool.submit(task7)
        # ProcessPool.submit(task8)
        # ProcessPool.submit(task9)
        # ProcessPool.submit(task10)
        # ProcessPool.submit(task11)
        # ProcessPool.submit(task12)
        # ProcessPool.submit(task13)
        # ProcessPool.submit(task14)
        # ProcessPool.submit(task15)
        # ProcessPool.submit(task16)
        # ProcessPool.submit(task17)
        # ProcessPool.submit(task18)
        # ProcessPool.submit(task19)
        # ProcessPool.submit(task20)
        # ProcessPool.submit(task21)
        # ProcessPool.submit(task22)

