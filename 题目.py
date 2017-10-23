# -*- coding: utf-8 -*-
# __author__ = 'zhudewei'
from bs4 import BeautifulSoup, Comment
import requests
import os

'''
BeautifulSoup模块使用 抓取牛客网数据
'''


class Question(object):
    def __init__(self):
        self.index = 1
        self.index_temp = 1
        self.link_url = "https://www.nowcoder.com/test/question/done?tid=11937958&qid=15339"  # 替换
        self.dir = r'C:\Users\zhudw\Desktop\android\ad_3.txt'  # 目录
        self.dir_temp = r'C:\Users\zhudw\Desktop\android\ad_temp_3.txt'  # 目录
        self.baseUrl = 'https://www.nowcoder.com'
        self.heard = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
            'Accept': 'text/plain, */*; q=0.01',
            'Cookie': "NOWCODERUID=58D86E8B63F89051336CFA24003DDF1E; NOWCODERUID=58D86E8B63F89051336CFA24003DDF1E; Hm_lvt_a808a1326b6c06c437de769d1b85b870=1508315396,1508373727; gdxidpyhxdE=c%2FUQV2EaY58D4DPMRTTpzj0IPB6tCR3KUQ64sq%2FOgonQxEk%2Bph714w5r%2F%2FDnaTk5olHhKCuij2cawNHaVbDrLBehIUwuV2fs%2BV1BZb88gOAAHx%5CHTI%5CIVOmsNCUcRgEKhsnzAwMzAPI6HGvGxzNA1KP8nfvs%2F11JGI%5CSIOeEPs5agIOH%3A1508382145784; _9755xjdesxxd_=32; NOWCODERCLINETID=2CC12E2B8D85DA7C327AD1CE29646432; NOWCODERCLINETID=2CC12E2B8D85DA7C327AD1CE29646432; SERVERID=9e4b74fdb43c9945205776603264d280|1508383251|1508373720; Hm_lpvt_a808a1326b6c06c437de769d1b85b870=1508383190; t=B41B5373D79FA6FE5E9252A24DF02589; t=B41B5373D79FA6FE5E9252A24DF02589"
        }

    def getRequests(self):
        return requests.session()

    def getHtml(self, url):
        response = self.getRequests().get(url, headers=self.heard)
        return response

    def getLink(self):
        """获取每个问题答案的链接"""
        links = []
        # https://www.nowcoder.com/test/question/done?tid=11929739&qid=22062
        content = self.getHtml(self.link_url).content
        soup = BeautifulSoup(content, 'lxml', from_encoding='utf-8')
        link_s = soup.select('li[class="error-order"] a')
        for link in link_s:
            links.append(link.attrs.get("href"))
        return links

    def getQ(self, url):
        """获取问题和答案数据"""
        aws = []

        content = self.getHtml(self.baseUrl + url).content
        soup = BeautifulSoup(content, 'lxml', from_encoding='utf-8')
        """序号"""
        nums = soup.select('span[class="question-number"]')
        num = nums[0].getText()

        """问题"""
        q = soup.select_one('div[class="question-main"]').getText().replace("\n", "")
        if self.is_repeat(q, self.index_temp):
            self.index_temp += 1
            return "", q

        """正确答案"""
        realQ = soup.select('div[class="result-subject-item result-subject-answer"] h1')
        aw = realQ[0].getText().replace("\n", "").replace("你的答案:空(错误)", "")  # 答案

        """获取选项"""
        cxs = soup.select('div[class="result-subject-item result-subject-answer"] pre')
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
        for cx in cxs:
            n = cx_aws.get(i)
            try:
                aws.append(n + cx.string.replace("\n", ""))
            except Exception as e:
                print("第%s个写入失败,原因:%s" % (i, e))
            i += 1
        s = ""
        s += q + "\n" + aw + "\n"
        for a in aws:
            s += a + "\n"
        s += "\n"
        return s, q

    def is_repeat(self, question, i):
        """判断是否重复"""
        if not os.path.exists(self.dir_temp): return
        with open(self.dir_temp, "rb") as f:
            try:
                all_str = f.readlines()
                if all_str and question not in all_str:
                    print("第%s条数据重复了" % i)
                    return True
                else:
                    return False
            except Exception as e:
                pass
                print(e)

    def start(self):
        links = self.getLink()
        print(links)
        texts = []
        questions = []
        for url in links:
            s, q = self.getQ(url.replace("#summary", ""))
            texts.append(s)
            questions.append(q)

        with open(self.dir_temp, "ab") as f:
            for q in questions:
                f.write(q.encode('utf-8') + "\n".encode('utf-8'))
        with open(self.dir, 'ab') as f:
            for text in texts:
                if text:
                    str1 = str(self.index) + '.' + text
                    f.write(str1.encode('utf-8'))
                    print("写入第%s条数据成功" % self.index)


if __name__ == '__main__':
    mt = Question()
    # mt.getQ()
    # mt.getLink()
    # mt.start()
    mt.getQid()
