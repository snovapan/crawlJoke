# -*- coding: utf-8 -*-
import scrapy
import copy
import re
from scrapy.spiders import CrawlSpider
from crawlJoke.items import JokeItem


class JokeSpider(CrawlSpider):
    name = 'joke'
    allowed_domains = ['jokeji.cn']
    start_urls = ['http://www.jokeji.cn/list.htm']
    global base_url
    base_url = 'http://www.jokeji.cn'

    def parse(self, response):
        for each in response.xpath('//div[@class="joke_right"]/ul/li'):
            classify = each.xpath("./a/text()").extract()[0].strip()
            link = each.xpath("./a/@href").extract()[0].strip()
            url = base_url + link
            if "/yuanchuangxiaohua/" != link and '/list33_1.htm' == link:
                yield scrapy.Request(url=url, meta={'classify': classify}, callback=self.list_parse)

    def list_parse(self, response):
        classify = response.meta['classify']
        classify = classify[0:classify.index('(')]
        url = response.url
        print('url: ' + response.url)
        start = re.findall(r"_(\d*).htm", url)[0]
        print('page:' + start)
        endurl = response.xpath("//a[contains(text(),'尾页')]/@href").extract()[0]
        print('endurl: ' + endurl)
        for each in response.xpath('/html/body/div[3]/div[1]/div[2]/ul/li'):
            item = JokeItem()
            item['classify'] = classify
            item['title'] = each.xpath('./b/a/text()').extract()[0].strip()
            item['content'] = 'content'
            item['pubtime'] = each.xpath('./i/text()').extract()[0].strip()
            item['jokelink'] = base_url + each.xpath('./b/a/@href').extract()[0].strip()
            yield scrapy.Request(url=item['jokelink'], meta={'joke': item}, callback=self.joke_parse)
        if 'javascript:void(0)' == endurl:
            pass
        else:
            end = re.findall(r"_(\d*).htm", endurl)[0]
            print('end: ' + end)
            nowurl = url.replace("_{}.htm".format(start), "_{}.htm".format(end))
            print("nowurl: " + nowurl)
            yield scrapy.Request(url=nowurl, meta={'classify': classify}, callback=self.list_parse)

    def joke_parse(self, response):
        joke = response.meta['joke']
        item = copy.deepcopy(joke)
        item['content'] = response.xpath('//*[@id="text110"]').extract()[0].strip()
        # 把数据交给管道文件
        yield item