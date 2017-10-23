# -*- coding: utf-8 -*-
# __author__ = 'zhudewei'
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def getData(url):
    driver = webdriver.Chrome()  # 创建一个chrome内核浏览器
    driver.get(url)
    assert "Python" in driver.title
    # elem = driver.find_element_by_name("q")
    elem_dl = driver.find_element_by_id('downloads')
    elem_li = driver.find_element_by_css_selector('.element-1')
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.ENTER)
    ActionChains(driver).move_to_element(elem_dl).click(elem_li)  # 模拟鼠标移动并点击显示出来的按钮
    print(driver.page_source)
    driver.quit()


def t_bd(url):
    """
    模拟点击搜索百度
    :return:
    """
    driver = webdriver.Chrome()  # 创建一个chrome内核浏览器
    driver.get(url)
    el_input = driver.find_element_by_name('wd')
    el_submit = driver.find_element_by_id('su')
    el_input.send_keys("王尼玛")
    el_submit.submit()
    print(driver.page_source)
    driver.quit()
    pass


if __name__ == '__main__':
    # getData("http://www.python.org")
    t_bd("https://www.baidu.com/")
