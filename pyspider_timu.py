# -*- coding: utf-8 -*-
# __author__ = 'zhudewei'
import os
from pyspider.libs.base_handler import *

DIR = r'C:\Users\zhudw\Desktop\android\123'  # 目录


class Handler(BaseHandler):
    def __init__(self):
        self.util = WritUtil()
        self.index = 1
        self.max = 5  # 一次写入30个题目 5次就是150题

        self.baseUrl = 'https://www.nowcoder.com'
        self.heard = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
            'Accept': 'text/plain, */*; q=0.01',
            'Cookie': "NOWCODERUID=58D86E8B63F89051336CFA24003DDF1E; NOWCODERUID=58D86E8B63F89051336CFA24003DDF1E; Hm_lvt_a808a1326b6c06c437de769d1b85b870=1508315396,1508373727; gdxidpyhxdE=c%2FUQV2EaY58D4DPMRTTpzj0IPB6tCR3KUQ64sq%2FOgonQxEk%2Bph714w5r%2F%2FDnaTk5olHhKCuij2cawNHaVbDrLBehIUwuV2fs%2BV1BZb88gOAAHx%5CHTI%5CIVOmsNCUcRgEKhsnzAwMzAPI6HGvGxzNA1KP8nfvs%2F11JGI%5CSIOeEPs5agIOH%3A1508382145784; _9755xjdesxxd_=32; NOWCODERCLINETID=2CC12E2B8D85DA7C327AD1CE29646432; NOWCODERCLINETID=2CC12E2B8D85DA7C327AD1CE29646432; SERVERID=9e4b74fdb43c9945205776603264d280|1508383251|1508373720; Hm_lpvt_a808a1326b6c06c437de769d1b85b870=1508383190; t=B41B5373D79FA6FE5E9252A24DF02589; t=B41B5373D79FA6FE5E9252A24DF02589"
        }

    @every(minutes=24 * 60)
    def on_start(self):
        """
        /makePaper?source=1&tagIds=617&difficulty=5&questionCount=30
               difficulty=5 代表5星
        """
        n = 0
        while n < self.max:
            n += 1
            difficulty = 3  # 3星 题目难度 1~5星
            final_url = self.baseUrl + "/makePaper?source=1&tagIds=569&difficulty=%s&questionCount=30" % str(difficulty)
            self.crawl(final_url, callback=self.get_links, fetch_type='js', headers=self.heard, method='post',
                       validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def get_links(self, response):
        """获取进入测评结果的连接"""
        url = response.url  # 这里截取 tid
        tid = str(url).split("tid=")[1]
        final_url = "https://www.nowcoder.com/test/question/analytic?tid=%s" % tid
        self.crawl(final_url, callback=self.get_result, fetch_type='js', headers=self.heard, validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def get_result(self, response):
        """查看结果的连接"""
        url = [x for x in response.doc('.report-btnbox a').items()]
        final_url = url[0].attr.href  # https://www.nowcoder.com/test/question/done?tid=12012085&qid=51717
        self.crawl(final_url, callback=self.index_page, fetch_type='js', headers=self.heard, validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.error-order a').items():
            self.crawl(each.attr.href.split("#summary")[0], callback=self.detail_page, headers=self.heard,
                       validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        title = response.doc('.question-main').text()
        title = str(self.index) + '.' + title.replace("\n", "")
        right_aw = response.doc('.result-subject-answer h1').text()
        right_aw = right_aw.replace("\n", "").replace("你的答案:空 (错误)", "")  # 答案
        cxs = [x.text() for x in response.doc('.result-answer-item pre').items()]
        cx_aws = {
            0: 'A.',
            1: 'B.',
            2: 'C.',
            3: 'D.',
            4: 'E.',
            5: 'F.',
            6: 'G.',
        }
        i = 0
        aws = []
        for cx in cxs:
            n = cx_aws.get(i)
            try:
                aws.append(n + cx.replace("\n", ""))
            except Exception as e:
                print(e)
                pass
            i += 1

        s = ""
        s += title + "\n" + right_aw + "\n"
        for a in aws:
            s += a + "\n"
        s += "\n"
        path = DIR + "/ad.txt"
        """写入数据"""
        self.util.save(s, path)
        self.index += 1
        return dict(a_title=title, a_right_aw=right_aw, aws=aws)


class WritUtil(object):
    def save(self, content, path):
        with open(path, 'ab') as f:
            f.write(content.encode('utf-8'))
