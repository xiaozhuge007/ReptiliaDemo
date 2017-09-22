# -*- coding: utf-8 -*-
# __author__ = 'zhudewei'
import jieba
import numpy as np
from PIL import Image
from os import path
import matplotlib.pyplot as plt
import random

from whoosh.lang import stopwords
from wordcloud import WordCloud, STOPWORDS

name = 'seeLZ.txt'


def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(0, 100)


d = path.dirname(__file__)
mask = np.array(Image.open(path.join(d, "img\stormtrooper_mask.png")))
font = path.join(d, "font\DroidSansFallbackFull.ttf")

# stopwords.add("ext")
text = open(r'D:\Python\word\%s' % name).read()
wc = WordCloud(font_path=font, width=1920, height=1080, max_words=100, mask=mask, margin=10,
               random_state=1, max_font_size=80).generate(text)
default_colors = wc.to_array()
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3))
plt.axis("off")
plt.figure()
plt.title(u"贴吧评论数据统计")
plt.imshow(default_colors)
plt.axis("off")
plt.show()
