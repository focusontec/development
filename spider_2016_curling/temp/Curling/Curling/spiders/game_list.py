# -*- coding: utf-8 -*-

import re
from copy import deepcopy

import scrapy

from Curling.utils.tools import gen_md5, get_today
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class GameListSpider(scrapy.Spider):
    count_num = 1
    name = 'game_list'
    # allowed_domains = ['*']
    # todo changed
    start_urls = ['http://www.worldcurling.org/events/2017/']
    def parse(self, response):
        # todo changed
        game_of_17 = response.xpath('(//tr[@class="odd"]|//tr[@class="even"])/td[6]')
        item = dict()
        item["season_year"] = "2016"
        temp = game_of_17.xpath('.//text()').extract()[0:-1]
        print temp,len(temp)
        # 获取月份列表
        month_list_selector = response.xpath('(//tr[@class="odd"]|//tr[@class="even"])/td[1]')
        month_list = month_list_selector.xpath('.//text()').extract()[:-1]
        temp_href = []
        for href in game_of_17[:-1]:
            month_events_href ="http://www.worldcurling.org"+ href.xpath('.//a/@href').extract_first() if len(href.xpath('.//a/@href'))>0 else None
            temp_href.append(month_events_href)
        print temp_href,len(temp_href)
        zip_month_time =  zip(month_list,temp,temp_href)

        print zip_month_time


        for i in zip_month_time:
            item['month_of_year'] = i[0]
            item["times_in_month"] = i[1] if i[1].isdigit() else 0
            month_href = i[2]
            if item["times_in_month"] != 0:
                yield scrapy.Request(url = month_href,callback=self.parse_detail,meta={"game_list":deepcopy(item)})


    def parse_detail(self,response):
        game_list = response.meta.get("game_list")
        game_list_selector = response.xpath('//div[@class="listingResults"]/div[contains(@class,"result item")]')
        print len(game_list_selector), '--------------------------------------------', game_list['times_in_month']
        tmp=[]
        for game in game_list_selector:
            game_list['event_name'] = game.xpath('.//h4/a/text()').extract_first()
            game_list['event_href'] = "http://www.worldcurling.org"+game.xpath('.//h4/a/@href').extract_first()
            game_time_duration = game.xpath('.//p[1]/text()').extract_first()
            game_list['starttime'] = game_time_duration.split(' - ')[0]
            game_list['endtime'] = game_time_duration.split(' - ')[1]
            game_list['vc_url'] = game_list['event_href']
            game_list['game_logo_url'] = "http://www.worldcurling.org"+game.xpath('.//img/@src').extract_first()
            location = game.xpath('.//p[@class="dateline results small"][2]/text()').extract() if len(game.xpath('.//p[@class="dateline results small"][2]/text()'))>0 else ""
            game_list['venue'] = '-'.join(location) if location else ""
            yield scrapy.Request(url = game_list['event_href'],callback=self.get_event_id,meta={"game_list":deepcopy(game_list)},dont_filter=True)



    def get_event_id(self,response):
        GameListSpider.count_num += 1
        game_list = response.meta.get('game_list')
        event_id = re.search(r"lsEventID=(\d+)",response.text)
        if event_id :
            game_list['event_id'] = event_id.group(1)
        else:
            game_list['event_id'] = ""
        game_list['vc_md5'] = gen_md5("{}#{}".format(game_list['event_name'],game_list['event_href']))
        game_list['dt_update'] = get_today()
        game_list_item = dict()
        game_list_item['table_name'] = 'event_list'
        game_list_item['metric_pk'] = game_list.get('vc_md5')
        game_list_item['data_rows'] = [dict(game_list)]
        yield game_list_item





