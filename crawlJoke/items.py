# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JokeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #分类
    classify = scrapy.Field()
    #列表页数
    page = scrapy.Field()
    #标题
    title = scrapy.Field()
    #内容
    content = scrapy.Field()
    #发布时间
    pubtime = scrapy.Field()
    #来源
    jokelink = scrapy.Field()