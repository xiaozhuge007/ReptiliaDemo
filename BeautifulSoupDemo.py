# -*- coding: utf-8 -*-
# __author__ = 'zhudewei'
from bs4 import BeautifulSoup, Comment
import requests

'''
BeautifulSoup模块使用 抓取豆瓣电影热评点评
'''


def getHtml(url):
    s = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',

    }
    response = s.get(url, headers=headers)
    content = response.content
    soup = BeautifulSoup(content, 'lxml')
    # print(soup.a.attrs)
    # print(soup.a.name)
    # print(soup.span.string)  # 获取标签里的string
    print(soup.prettify())


if __name__ == '__main__':
    getHtml("https://movie.douban.com/review/best/")
