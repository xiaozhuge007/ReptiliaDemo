# -*- coding: utf-8 -*-
# __author__ = 'zhudewei'
"""
豆瓣电影
"""

from pyspider.libs.base_handler import *
import os
import urllib.request
import time

DIR = r'D:\Python\douban_movie'


class Handler(BaseHandler):
    def __init__(self):
        # https://movie.douban.com/explore#!type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0
        self.baseUrl = 'https://movie.douban.com/explore#!type=movie'
        self.heard = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'bid=7oc9onqmqYg; __utma=30149280.1305241593.1506409616.1508462436.1509071638.4; __utmz=30149280.1506409616.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.153562659.1506409616.1508462436.1509071638.4; __utmz=223695111.1506409616.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _pk_id.100001.4cf6=2a78e98fffb3d5bb.1506409618.4.1509074857.1508462434.; _pk_ses.100001.4cf6=*; __utmb=30149280.1.10.1509071638; __utmc=30149280; __utmb=223695111.0.10.1509071638; __utmc=223695111; ap=1; ps=y; ll="118282"; ue="zhu2948031@163.com"; dbcl2="168765779:5F2hlAfDkXw"; ck=yCVj; push_noty_num=0; push_doumail_num=0; __yadk_uid=bsIxsuQazKOSVdlkXQF3Xjpjlerrr4AU; _vwo_uuid_v2=1A5EEDF0D97F74F6997B662C3658364A|9aa3515bd2fe2fea0d09c80408dc8bce',

        }
        self.tags = ['热门', '最新', '经典', '可播放', '豆瓣高分', '冷门佳片', '华语', '欧美', '韩国',
                     '日本', '动作', '喜剧', '爱情', '科幻', '悬疑', '恐怖', '文艺']
        self.sorts = ['recommend', 'time', 'rank']  # 分别对应热度/时间/评价
        self.page_limit = 20  # 每页多少条
        self.page_start = 0  # 第几页
        self.review = 0  # 评论的条数 每次+20git
        self.util = Util()

    @every(minutes=24 * 60)
    def on_start(self):
        for tg in self.tags:
            url = self.get_url(tg, self.sorts[0], self.page_limit, self.page_start)
            self.crawl(url, callback=self.index_page, headers=self.heard, fetch_type='js', validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        time.sleep(1)
        a = response.doc('.item')
        for each in a.items():
            self.crawl(each.attr.href, callback=self.get_home, fetch_type='js', headers=self.heard,
                       validate_cert=False)

    def get_home(self, response):
        time.sleep(1)

        """
        保存封面和简介,抓取评论页面
        :param response:
        :return:
        """
        # 'https://movie.douban.com/subject/1292052/?tag=%E7%BB%8F%E5%85%B8&from=gaia_video'
        url = urllib.request.unquote(response.url)
        print(str(url))
        img = [x for x in response.doc('.nbgnbg img').items()][0].attr.src
        title = response.doc('h1').text()
        info = response.doc('#info').text()
        path = str(url).split('?tag=')[1].split('&from=')[0]
        self.util.save_file(path + "/" + title, '简介.txt', info)
        self.util.save_img(path + "/" + title, '封面.png', img)

        for i in range(5):
            final_url = url.split('?tag=')[0] + "reviews" + "?start=%s" % self.review
            self.crawl(final_url, callback=self.detail_page, fetch_type='js', headers=self.heard,
                       validate_cert=False, save={'path': path + "/" + title})

    def detail_page(self, response):
        time.sleep(0.5)
        self.review += 20
        path = response.save['path']
        title = response.doc('h1').text()
        authors = [x.text() for x in response.doc('.author').items()]
        contents = [x.text() for x in response.doc('.short-content').items()]
        i = 0
        with open(DIR + "/" + path + "/" + '评论.txt', 'ab')as f:
            f.write(str("\t\t\t\t\t\t\t" + title + "\n").encode('utf-8'))
            for content in contents:
                author = authors[i]
                s = author + ":\t" + content + "\n"
                f.write(s.encode('utf-8'))
                i += 1
        return {
            'title': title,
            'author': authors,
            'content': contents,
        }

    def get_url(self, tag, sort, page_limit, page_start):
        """获取开始抓取数据的baseUrl"""
        return self.baseUrl + "&tag=%s&sort=%s&page_limit=%s&page_start=%s" % (tag, sort, page_limit, page_start)


class Util(object):
    def __init__(self):
        pass

    def make_dir(self, path):
        if not os.path.exists(DIR + '/' + path):
            os.makedirs(DIR + '/' + path)

    def save_file(self, path, file_name, content):
        self.make_dir(path)
        if not path.endswith("/"):
            path += "/"
        with open(DIR + "/" + path + file_name, 'wb') as f:
            f.write(content.encode('utf-8'))

    def save_ab_file(self, path, file_name, content):
        self.make_dir(path)
        if not path.endswith("/"):
            path += "/"
        with open(DIR + "/" + path + file_name, 'ab') as f:
            f.write(content.encode('utf-8'))

    def save_img(self, path, file_name, url):
        self.make_dir(path)
        urllib.request.urlretrieve(url, DIR + "/" + path + '/' + file_name)


if __name__ == '__main__':
    # tag = b"%E7%BB%8F%E5%85%B8".decode('gbk').encode("utf-8")
    tag = urllib.request.unquote('%E7%BB%8F%E5%85%B8')
    print(tag)
