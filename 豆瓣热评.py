# -*- coding: utf-8 -*-
# __author__ = 'zhudewei'
from bs4 import BeautifulSoup, Comment
import requests
import os

'''
BeautifulSoup模块使用 抓取豆瓣电影热评点评
'''


class MovieTop(object):
    def __init__(self):
        self.baseUrl = 'https://movie.douban.com'
        self.first_url = "/review/best/"

    def getHtml(self, url):
        s = requests.session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',

        }
        response = s.get(url, headers=headers)
        return response

    def get_links_names(self, url):
        """
        文件名字 和评论详情地址
        :param url:
        :return:
        """
        movies = []
        names = []
        links = []

        content = self.getHtml(url).content
        soup = BeautifulSoup(content, 'lxml', from_encoding='utf-8')
        movie_titles = soup.select('a[class="subject-title"]')  # 电影名字
        lks = soup.select('a[class="title-link"]')  # 记录评论的页面
        aus = soup.select('a[class="author"] span')

        for m_title in movie_titles:
            movies.append(m_title.string)
        for lk in lks:
            href = lk.attrs.get('href')
            links.append(href)
        i = 0
        for auth in aus:
            movie = movies[i]
            names.append(movie + "-" + auth.string)
            i += 1
        # print(links)
        # print(names)
        return links, names

    def get_nexts(self, url):
        """
        获取下一页
        :return: 下一页的url
        """
        urls = []
        urls.append(self.first_url)
        soup = BeautifulSoup(self.getHtml(url).content, 'lxml', from_encoding='utf-8')
        urls1 = soup.select('div[class="paginator"] a')
        for url in urls1:
            urls.append(url.attrs.get('href'))
        return urls

    def getContent(self, url):
        """
        获取该用户点评的内容
        """
        soup = BeautifulSoup(self.getHtml(url).content, 'lxml', from_encoding='utf-8')
        content = soup.select('div[class="review-content clearfix"]')[0].text
        return content

    def writToText(self, name, content, index_name):
        if not os.path.exists(r'D:\Python\douban\%s' % index_name): os.makedirs(r'D:\Python\douban\%s' % index_name)
        i = 0
        with open(r'D:\Python\douban\%s\%s.txt' % (index_name, name), 'wb') as f:
            for c in content:
                c = c.encode('utf-8')
                if c == '\n': c.replace(c, '')
                if i % 100 == 0: f.write("\n".encode('utf-8'))
                f.write(c)
                i += 1

    def start(self):
        k = 1
        urls = self.get_nexts(self.baseUrl + self.first_url)
        for url in urls:
            print("--------------第%s页开始写入--------------" % k)
            links, names = self.get_links_names(self.baseUrl + url)
            i = 0
            for link in links:
                content = self.getContent(link)
                self.writToText(names[i], content, "第%s页" % k)
                i += 1
            print("第%s页写入完成" % k)
            k += 1


if __name__ == '__main__':
    mt = MovieTop()
    mt.start()
