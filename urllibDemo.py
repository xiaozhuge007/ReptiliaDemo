# -*- coding: utf-8 -*-
# __author__ = 'zhudewei'
import re

import urllib3


def loadHtml(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    http = urllib3.PoolManager()
    response = http.request('GET', url, headers=headers)
    return response.data


def getImg(html):
    reg = r'img .*? src="(.+?\.jpg|png|jpeg)"'
    img_re = re.compile(reg)
    img_list = re.findall(img_re, html)
    i = 0
    print(img_list)
    for img_url in img_list:
        get_img = loadHtml(img_url)
        print(get_img)
        with open("%s%s.png" % ("D:\Python\img\\", i), 'wb') as f:
            f.write(get_img)
            print("正在下载底%s张图片" % i)
            i += 1


if __name__ == "__main__":
    data = loadHtml("http://www.imooc.com/course/list")
    getImg(str(data))
