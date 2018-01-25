# -*- coding: utf-8 -*-
import scrapy


class Test1Spider(scrapy.Spider):
    name = 'test1'
    allowed_domains = ['worldcurling.org','odf2.worldcurling.co']
    start_urls = ['http://www.worldcurling.org/events/2017/']

    def parse(self, response):
        yield scrapy.Request('http://odf2.worldcurling.co/data/WUNI2017P/play_by_play/1645/1-11.jpg',callback=self.parse_tt)

    def parse_tt(self,response):
        print 'get hrere'