#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-03-06 18:08:02
# Project: lianjia

from pyspider.libs.base_handler import *
import math


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        for i in range(1, 1334):
            self.crawl('http://sh.lianjia.com/xiaoqu/d' + str(i), callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):

        for each in response.doc('div[class="info-panel"]>h2>a[name="selectDetail"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)
            # 翻页
            # for each in response.doc('a[gahref="results_next_page"]').items():
            # self.crawl(each.attr.href, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        # info = (response.doc('.aroundInfo>tbody>tr>td ').text()).encode('utf-8')
        return {
            # "url": response.url,
            # "title": response.doc('title').text(),
            "AveragePrice": response.doc('div[class="item col1"]>p:nth-child(2)').text(),
            "XiaoqQu": response.doc('div[class="title fl"]>span[class="t"]>h1').text(),
            # "PropertyType":response.doc('div[class="col-2 clearfix"]>ol>li:nth-child(1)>span[class="other"]').text(),
            # "decade":response.doc('div[class="col-2 clearfix"]>ol>li:nth-child(2)>span>span[class="other"]').text(),
            # "PropertyFee":response.doc('div[class="col-2 clearfix"]>ol>li:nth-child(3)>span[class="other"]').text(),
            # "PropertyCompany":response.doc('div[class="col-2 clearfix"]>ol>li:nth-child(4)>span[class="other"]').text(),
            # "Developers":response.doc('div[class="col-2 clearfix"]>ol>li:nth-child(5)>span[class="other"]').text(),
            "district": response.doc('div[class="col-2 clearfix"]>ol>li:nth-child(6)>span[class="other"]').text(),
            "ring": response.doc('div[class="col-2 clearfix"]>ol>li:nth-child(7)>span[class="other"]').text(),
            # "Address":response.doc('div[class="title fl"]>span[class="t"]>span[class="adr"]').text(),
            # "region":response.doc('div[class="title fl"]>span[class="t"]>span:nth-child(2)').text(),

        }

    # def on_result(self, result):
    #     if not result:
    #         return
    #     price = result['AveragePrice']
    #     XiaoqQu = result['XiaoqQu']
    #     content = price + '\t+------' + XiaoqQu
    #     with open(r"C:\Users\zhudw\Desktop\android\122\1.txt", 'ab') as f:
    #         f.write(content.encode('utf-8'))
