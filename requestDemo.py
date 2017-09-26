# -*- coding: utf-8 -*-
# __author__ = 'zhudewei'
import requests

'''
requests 基本使用
'''


def get_data(url):
    rs = requests.get(url)
    code = rs.status_code
    content = rs.content
    cookies = rs.cookies
    encoding = rs.encoding
    print('code=%s,\ncookies=%s,\nencoding=%s,\ncontent=%s' % (code, cookies, encoding, content))


if __name__ == '__main__':
    get_data("http://cuiqingcai.com/2556.html")
