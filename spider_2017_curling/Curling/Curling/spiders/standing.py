# -*- coding: utf-8 -*-
import json
import time
from copy import deepcopy

import scrapy

from Curling.utils.tools import get_today, gen_md5


class StandingSpider(scrapy.Spider):
    name = 'standing'
    allowed_domains = ['worldcurling.org','ktgsports.com']
    start_urls = ["http://www.worldcurling.org"]

    def parse(self, response):
        event_list = [
            {"event_name": "World Junior-B Curling Championships 2017", "event_id": "",
             "event_href": "http://www.worldcurling.org/world-junior-b-curling-championships-2017",
             "event_abbr": ""},
            {"event_name": "28th Winter Universiade", "event_id": "116",
             "event_href": "http://www.worldcurling.org/universiade-2017-live-scores",
             "event_abbr": "WUNI2017P"},
            {"event_name": "VoIP Defender World Junior Curling Championships 2017", "event_id": "118",
             "event_href": "http://www.worldcurling.org/wjcc2017", "event_abbr": "CUR_WJCC2017P"},
            {"event_name": "2017 Sapporo Asian Winter Games", "event_id": "",
             "event_href": "http://www.worldcurling.org/awg2017", "event_abbr": ""},
            {"event_name": "World Wheelchair Curling Championship 2017", "event_id": "119",
             "event_href": "http://www.worldcurling.org/wwhcc2017", "event_abbr": "CUR_WWhCC2017P"},
            {"event_name": "CPT World Women's Curling Championship 2017", "event_id": "120",
             "event_href": "http://www.worldcurling.org/wwcc2017", "event_abbr": "CUR_WWCC2017P"},
            {"event_name": "Ford World Men's Curling Championship 2017", "event_id": "121",
             "event_href": "http://www.worldcurling.org/wmcc2017", "event_abbr": "CUR_WMCC2017P"},
            {"event_name": "World Mixed Doubles Curling Championship 2017", "event_id": "122",
             "event_href": "http://www.worldcurling.org/wmdcc2017", "event_abbr": "CUR_WMDCC2017P"},
            {"event_name": "World Senior Curling Championships 2017", "event_id": "123",
             "event_href": "http://www.worldcurling.org/wscc2017", "event_abbr": "CUR_WSCC2017P"},
            {"event_name": "European Curling Championships C-Division 2017", "event_id": "",
             "event_href": "http://www.worldcurling.org/ecc2017", "event_abbr": ""},
            {"event_name": "Audi quattro Winter Games NZ 2017", "event_id": "",
             "event_href": "http://www.worldcurling.org/nzwg2017", "event_abbr": ""},
            {"event_name": "6th World Curling Congress", "event_id": "",
             "event_href": "http://www.worldcurling.org/congress2017", "event_abbr": ""},
            {"event_name": "World Mixed Curling Championship 2017", "event_id": "125",
             "event_href": "http://www.worldcurling.org/wmxcc2017", "event_abbr": "CUR_WMxCC2017P"},
            {"event_name": "Pacific-Asia Curling Championships 2017", "event_id": "126",
             "event_href": "http://www.worldcurling.org/pacc2017", "event_abbr": "CUR_PACC2017P"},
            {"event_name": "Le Gruy\u00e8re AOP European Curling Championships 2017", "event_id": "127",
             "event_href": "http://www.worldcurling.org/ecc2017", "event_abbr": "CUR_ECCA2017P"},
            {"event_name": "Olympic Qualification Event 2017", "event_id": "129",
             "event_href": "http://www.worldcurling.org/oqe2017", "event_abbr": "CUR_OQE2017P"}
        ]
        for item in event_list:
            req_url = "http://live.ktgsports.com/data/{}/{}-standings.html?_={}"
            standing = dict()
            json_url = req_url.format(item.get("event_abbr"), item.get('event_id'), int(round(time.time() * 1000)))
            standing['event_name'] = item.get('event_name')
            standing['dt_update'] = get_today()
            if item.get('event_id'):
                standing['vc_url'] = json_url
                yield scrapy.Request(url=json_url,callback=self.parse_detail,meta={'standing':deepcopy(standing)})
            else:
                standing['vc_md5'] = gen_md5('{}#{}'.format(standing['event_name'],item.get('event_href')))
                standing_item = dict()
                standing_item['table_name'] = 'standing_copy_copy'
                standing_item['metric_pk'] = standing.get('vc_md5')
                standing_item['data_rows'] = [dict(standing)]
                yield standing_item
    def parse_detail(self, response):
        print 'come here parse_detail'
        standing = response.meta.get('standing')
        json_data = json.loads(response.text)
        event_info = json_data[0]
        standing_table = json_data[1:]
        standing['event_abbr'] = event_info.get('eventCode')
        standing['event_id'] = event_info.get('eventID')
        for table in standing_table:
            for team in table:
                standing['division_name'] =team.get('divisionName')
                standing['team_name'] = team.get('team_name')
                standing['ranking'] = team.get('rank')
                standing['played'] = team.get('played')
                standing['win'] = team.get('win')
                standing['loss'] = team.get('loss')
                standing['results'] = team.get('q')
                standing['vc_md5'] =gen_md5('{}#{}#{}#{}'.format(standing['event_name'],standing['division_name'],standing['team_name'],standing['ranking']))
                standing_item = dict()
                standing_item['table_name'] = 'standing_copy_copy'
                standing_item['metric_pk'] = standing.get('vc_md5')
                standing_item['data_rows'] = [dict(standing)]
                yield standing_item



