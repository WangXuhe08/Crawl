from requests import get
import re
from concurrent.futures import ThreadPoolExecutor
from os import path, environ
from sys import argv

environ['REQUESTS_CA_BUNDLE'] =  path.join(path.dirname(argv[0]), 'cacert.pem')

def temp(url_freq):
    try:
        resp2 = get(f'https://www.trxs.cc{url_freq}',headers=header, timeout=60)
        if resp2.status_code < 400:
            return resp2
        else:
            print("Status Error")
            return 0
    except TimeoutError:
        print("TimeOut Reconnect")
        try:
            resp2 = get(f'https://www.trxs.cc{url_freq}', headers=header, timeout=60)
            if resp2.status_code < 400:
                return resp2
            else:
                print("Status Error")
                return 0
        except TimeoutError:
            print("TimeOut Don't RE")
            return 0


if __name__ == '__main__':
    flag = 1
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.484"
                      "4.84 Safari/537.36",
    }
    while flag:
        url = input("详情页面URL==>")
        try:
            resp1 = get(url, headers=header, timeout=50)
        except TimeoutError:
            print("TimeOut Reconnect")
            try:
                resp1 = get(url, headers=header, timeout=50)
            except TimeoutError:
                print("TimeOut Don't RE")
                pass
        resp1.encoding = "GB18030"
        resp1 = resp1.text
        analysis0 = re.compile(r'<head>.*?keywords" content="(?P<part1>.*?)" />.*?</head>', re.S)
        titlename = analysis0.findall(resp1)[0]

        titlename = titlename.replace(r'：', '')
        titlename = titlename.replace(r':', '')
        titlename = titlename.replace(r'?', '')
        titlename = titlename.replace(r'/', '')
        titlename = titlename.replace(r'|', '')
        titlename = titlename.replace(r'<', '')
        titlename = titlename.replace(r'>', '')
        titlename = titlename.replace(r'*', '')
        titlename = titlename.replace(r'"', '')
        titlename = titlename.replace(r';', '')
        titlename = titlename.replace(r'，', ',')
        titlename = titlename.replace(r' ', '')
        titlename = titlename.replace(r'\r\n', '')
        print(titlename)

        analysis1 = re.compile(r'<ul class="clearfix">(?P<part1>.*?)<div class="copyright">', re.S)
        analysis2 = re.compile(r'<a href="(?P<part2>.*?)">', re.S)
        analysis3 = re.compile(r'<div class="read_chapterDetail">(?P<part3>.*?)<div class="pageNav">', re.S)
        analysis4 = re.compile(r'<p>(?P<content_avater>.*?)</p>', re.S)
        result1 = analysis1.findall(resp1)
        result2 = analysis2.findall(result1[0])

        with open(fr'D:\python_write_file\爬虫NumberTwo\novel/{titlename}.txt', 'a', encoding='gb18030') as file:
            avater_freq = 1
            with ThreadPoolExecutor(500) as Thread:
                try:
                    for url_part in result2:
                        partls = Thread.submit(temp, (url_part))
                        partls = partls.result()
                        if partls:
                            partls.encoding = "GB18030"
                            partls = partls.text
                            result3 = analysis3.findall(partls)
                            result4 = analysis4.findall(result3[0])
                            for i in result4:
                                file.write(i)
                                file.write("\n")
                        else:
                            print("Return is 0")
                            pass
                        print(avater_freq, "章 OK")
                        avater_freq += 1
                except UnicodeEncodeError:
                    print("Unicode error")
                    pass

        file.close()

        flag = int(input("1 继续"
                         "0 退出"
                         "是否继续?==>"))


