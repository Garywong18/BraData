# -*- coding: utf-8 -*-
import scrapy
import json
from BraData import settings

class BraSpider(scrapy.Spider):
    name = 'bra'
    allowed_domains = ['tmall.com']
    start_urls = ['https://rate.tmall.com/list_detail_rate.htm?itemId=41336666995&spuId=297847616&sellerId=391817269&order=3&currentPage=1&append=0&content=1&tagId=&posi=&picture=&groupId=%3D&needFold=0&_ksTS=1558768697460_669&callback=jsonp670']
    cookie_str = settings.cookie_str
    cookies = {i.split('=')[0]:i.split('=')[1] for i in cookie_str.split(';')}
    num = 1

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            cookies=self.cookies
        )

    def parse(self, response):
        res = response.text
        json_str = res.strip().lstrip('jsonp670(').strip(')')
        dic = json.loads(json_str)
        rate_list = dic['rateDetail']['rateList']
        print(len(rate_list))
        print(rate_list)
        for rate in rate_list:
            item = {}
            item['info'] = rate['auctionSku']
            item['content'] = rate['rateContent']
            item['date'] = rate['rateDate']
            item['golduser'] = rate['goldUser']
            yield item

        base_url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=41336666995&spuId=297847616&sellerId=391817269&order=3&currentPage={}&append=0&content=1&tagId=&posi=&picture=&groupId=%3D&needFold=0&_ksTS=1558768697460_669&callback=jsonp670'
        self.num += 1
        while self.num < 1000:
            next_page = base_url.format(self.num)
            yield scrapy.Request(
                next_page,
                cookies=self.cookies,
                callback=self.parse
            )