# -*- coding: utf-8 -*-
import scrapy

from Curling.utils.tools import get_today, gen_md5


class WorldrankingsSpider(scrapy.Spider):
    name = 'worldrankings'
    allowed_domains = ['worldcurling.org']
    start_urls = ['http://www.worldcurling.org/worldrankings']

    def parse(self, response):
        # 比赛类型分组
        division_type =  response.xpath('//div[@id="tabs"]/ul/li//text()').extract()
        worldrankings = dict()

        tables =  response.xpath('//div[contains(@id,"tabs-")]')
        connect_table = zip(division_type,tables)
        for  each_table in connect_table:
            tr_selector = each_table[1].xpath('.//tr')
            worldrankings['division_name'] = each_table[0]
            worldrankings['season'] = tr_selector[1].xpath('./td[1]/text()').extract_first()
            for tr in tr_selector[2:]:
                td_text =  tr.xpath('./td/text()').extract()
                if len(td_text) == 4:
                    worldrankings['ranking'] = td_text[0]
                    worldrankings['association'] = td_text[1]
                    worldrankings['points'] = td_text[2]
                    worldrankings['up_or_down'] = td_text[3]
                    worldrankings['dt_update'] = get_today()
                    worldrankings['vc_url'] = response.url
                    worldrankings['vc_md5'] = gen_md5('#{}#{}#{}'.format(worldrankings['association'],worldrankings['ranking'],worldrankings['division_name']))
                    worldrankings_item = dict()
                    worldrankings_item['table_name'] = 'worldrankings'
                    worldrankings_item['metric_pk'] = worldrankings.get('vc_md5')
                    worldrankings_item['data_rows'] = [dict(worldrankings)]

                    yield worldrankings_item

                    # yield worldrankings
