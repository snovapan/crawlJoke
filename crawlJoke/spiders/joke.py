# -*- coding: utf-8 -*-
import scrapy
import copy
import re
import time
from scrapy.spiders import CrawlSpider
from crawlJoke.items import JokeItem


class JokeSpider(CrawlSpider):
    name = 'joke'
    allowed_domains = ['jokeji.cn']
    start_urls = ['http://www.jokeji.cn/list.htm']
    global base_url
    base_url = 'http://www.jokeji.cn'


    def parse(self, response):
        '''
        #跑指定分类，可指定列表页数
        yield scrapy.Request(url=base_url + "/list43_1.htm", meta={'classify': "冷笑话"}, callback=self.list_parse)
        return
        '''
        for each in response.xpath('//div[@class="joke_right"]/ul/li'):
            classify = each.xpath("./a/text()").extract()[0].strip()
            classify = classify[0:classify.index('(')]
            link = each.xpath("./a/@href").extract()[0].strip()
            url = base_url + link
            print('class:{}, url:{}'.format(classify,url))

            if "/yuanchuangxiaohua/" == link:
                for page in range(1,8066):
                    yield scrapy.Request(url='{}list/default{}.htm'.format(url, page), meta={'classify': classify, 'page':page}, callback=self.ycjoke_parse)
            else:
                yield scrapy.Request(url=url, meta={'classify': classify}, callback=self.list_parse)
            '''
            #跑指定的几个分类，从第一页开始
            links = [
                '/list39_1.htm',
                '/list36_1.htm',
                '/list35_1.htm',
                '/list30_1.htm',
                '/list2_1.htm',
                '/list34_1.htm',
                '/list31_1.htm',
                '/list8_1.htm',
                '/list9_1.htm',
                '/list6_1.htm',
                '/list22_1.htm',
                '/list15_1.htm',
                '/list17_1.htm',
                '/list11_1.htm',
                '/list20_1.htm',
                '/list38_1.htm',
                '/list24_1.htm'
            ]
            if link in links:
                yield scrapy.Request(url=url, meta={'classify': classify}, callback=self.list_parse)
            '''

    def list_parse(self, response):
        classify = response.meta['classify']
        url = response.url
        print('url: ' + response.url)
        start = re.findall(r"_(\d*).htm", url)[0]
        print('page:' + start)
        endurl = response.xpath("//a[contains(text(),'尾页')]/@href").extract()[0]
        print('endurl: ' + endurl)
        for each in response.xpath('/html/body/div[3]/div[1]/div[2]/ul/li'):
            item = JokeItem()
            item['classify'] = classify
            item['page'] = start
            item['title'] = each.xpath('./b/a/text()').extract()[0].strip()
            item['content'] = 'content'
            item['pubtime'] = each.xpath('./i/text()').extract()[0].strip()
            item['jokelink'] = base_url + each.xpath('./b/a/@href').extract()[0].strip()
            #休眠一下，防止数据不全
            time.sleep(0.1)
            yield scrapy.Request(url=item['jokelink'], meta={'joke': item}, callback=self.joke_parse)
        if 'javascript:void(0)' == endurl:
            pass
        else:
            end = re.findall(r"_(\d*).htm", endurl)[0]
            now = int(start) + 1
            print('now: {}, end: {}'.format(now, end))
            if int(start) < int(end):
                nowurl = url.replace("_{}.htm".format(start), "_{}.htm".format(now))
                print("nowurl: " + nowurl)
                yield scrapy.Request(url=nowurl, meta={'classify': classify}, callback=self.list_parse)

    def joke_parse(self, response):
        joke = response.meta['joke']
        item = copy.deepcopy(joke)
        item['content'] = response.xpath('normalize-space(//*[@id="text110"])').extract()[0].strip()
        # 把数据交给管道文件
        yield item

    # 原创笑话
    def ycjoke_parse(self, response):
        classify = response.meta['classify']
        page = response.meta['page']
        url = response.url
        print('url: ' + response.url)
        for each in response.xpath("//div[@class='ycjoke']/div[@class='txt']"):
            print('jokelink: {}, content: {}'.format(base_url + each.xpath('./h2/a/@href').extract()[0].strip(), each.xpath('string(./ul/li)').extract()[0]))
            item = JokeItem()
            item['classify'] = classify
            item['page'] = page
            item['title'] = each.xpath('./h2/a/text()').extract()[0].strip()
            content = each.xpath('normalize-space(./ul/li)').extract()[0].strip()
            if content.endswith('[完]'):
                content = content[0:-3]
            item['content'] = content
            item['pubtime'] = each.xpath('./span/i/text()').extract()[0].strip()
            item['jokelink'] = base_url + each.xpath('./h2/a/@href').extract()[0].strip()
            yield item
