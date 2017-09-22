# -*- coding: utf-8 -*-
# __author__ = 'zhudewei'
import urllib
from urllib import request, parse
import re
import os


class Tool(object):
    # 去除img标签,7位长空格
    removeImg = re.compile(r'<img.*?>')
    # 删除超链接标签
    removeAddr = re.compile(r'<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile(r'<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile(r'<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile(r'<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile(r'<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile(r'<.*?>')

    def replace(self, x):
        # if self.removeImg:
        #     x = re.sub(str(self.removeImg), "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()


class BDTB(object):
    def __init__(self, baseUrl, seeLZ):
        self.baseUrl = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)  # 是否只看楼主
        self.tool = Tool()

    def getPage(self, pageNum):
        url = self.baseUrl + self.seeLZ + '&pn=' + str(pageNum)
        rs = request.Request(url)
        try:
            response = request.urlopen(rs)
            return response.read().decode('utf-8')
        except request.URLError as e:
            if hasattr(e, 'reason'):
                print('连接百度贴吧失败...', e.reason)
                return None

    def getTitle(self):
        html = self.getPage(1)
        pattern = re.compile(r'<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pattern, html)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getNum(self):
        '''返回有多少页和多少条回复'''
        html = self.getPage(1)
        p_num = re.compile(r'<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', re.S)
        p_total = re.compile(r'<li class="l_reply_num.*?<span.*?>(.*?)</span>', re.S)
        result_num = re.search(p_num, html)
        result_total = re.search(p_total, html)
        if result_num:
            num = result_num.group(1).strip()
        else:
            num = None
        if result_total:
            total = result_total.group(1).strip()
        else:
            total = None
        return num, total

    def getContent(self):
        num = 1
        page = 1
        items = []
        max_page = int(self.getNum()[0])
        print('总共%s页数据----' % max_page)

        while page <= max_page:
            print('正在获取第%s页数据' % page)
            html = self.getPage(page)
            pattern = re.compile(r'<div id="post_content_.*?>(.*?)</div>', re.S)
            values = re.findall(pattern, html)
            items += values
            page += 1

        if not os.path.exists(r'D:\Python\word'):
            os.makedirs(r'D:\Python\word')
        name = 'all.txt' if self.seeLZ == 0 else 'seeLZ.txt'
        with open(r'D:\Python\word\%s' % name, 'w') as f:
            print('---------开始写入数据--------')
            for item in items:
                print('正在写入第%s条数据----------' % num)
                f.write('第%s楼------------------\n\n' % num)
                f.write(self.tool.replace(str(item)) + '\n\n')
                num += 1


if __name__ == '__main__':
    baseURL = 'http://tieba.baidu.com/p/5333347578'
    see_lz = input('是否只看楼主--0否 1是 请输入')  # 0否 1是
    bt = BDTB(baseURL, see_lz)

    bt.getContent()
# print(content)
