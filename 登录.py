# -*- coding: utf-8 -*-
# __author__ = 'zhudewei'
from urllib import request, parse
import urllib


def login(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
    '''设置代理'''
    enable_proxy = True
    proxy_handler = request.ProxyHandler({"http": 'http://some-proxy.com:8080'})
    null_proxy_handler = request.ProxyHandler({})
    if enable_proxy:
        opener = request.build_opener(proxy_handler)
    else:
        opener = request.build_opener(null_proxy_handler)
    request.install_opener(opener)

    values = dict(username='zhu2948031@163.com', password='zdw2948031.')
    data = parse.urlencode(values).encode('utf-8')
    rs = request.Request(url, data=data, headers=headers)
    response = request.urlopen(rs)
    return response.read()


if __name__ == '__main__':
    data = login('https://www.baidu.com/')
    print(data)
