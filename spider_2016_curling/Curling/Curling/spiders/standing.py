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
            {'event_id': '', 'event_name': '5th World Curling Congress',
             'event_href': 'http://www.worldcurling.org/congress2016', 'event_abbr': ''},
            {'event_id': '', 'event_name': 'European Curling Championships C-Division 2016',
             'event_href': 'http://www.worldcurling.org/2016-ecc-c-division', 'event_abbr': ''},
            {'event_id': '51', 'event_name': "Ford World Women's Curling Championship 2016",
             'event_href': 'http://www.worldcurling.org/wwcc2016', 'event_abbr': 'WCF_WWCC2016PA'},
            {'event_id': '109', 'event_name': 'World Mixed Curling Championship 2016',
             'event_href': 'http://www.worldcurling.org/wmxcc2016', 'event_abbr': 'CUR_WMxCC2016P'},
            {'event_id': '106', 'event_name': 'World Mixed Doubles Curling Championship 2016',
             'event_href': 'http://www.worldcurling.org/wmdcc2016', 'event_abbr': 'CU_WMDCC2016P'},
            {'event_id': '103', 'event_name': 'VoIP Defender World Junior Curling Championships 2016',
             'event_href': 'http://www.worldcurling.org/wjcc2016', 'event_abbr': 'CU_WJCC2016P'},
            {'event_id': '104', 'event_name': "World Men's Curling Championship 2016",
             'event_href': 'http://www.worldcurling.org/wmcc2016', 'event_abbr': 'CU_WMCC2016P'},
            {'event_id': '105', 'event_name': 'World Senior Curling Championships 2016',
             'event_href': 'http://www.worldcurling.org/wscc2016', 'event_abbr': 'CU_WSCC2016P'},
            {'event_id': '101', 'event_name': 'Youth Olympic Games 2016',
             'event_href': 'http://www.worldcurling.org/yog2016', 'event_abbr': 'WYOG2016P'},
            {'event_id': '102', 'event_name': 'World Wheelchair Curling Championship 2016',
             'event_href': 'http://www.worldcurling.org/wwhcc2016', 'event_abbr': 'CU_WWhCC2016P'},
            {'event_id': '', 'event_name': 'World Junior-B Curling Championships 2016',
             'event_href': 'http://www.worldcurling.org/world-junior-b-curling-championships-2016', 'event_abbr': ''},
            {'event_id': '111', 'event_name': 'World Wheelchair-B Curling Championship 2016',
             'event_href': 'http://www.worldcurling.org/wwhcc2017/wwhbcc-live-scores', 'event_abbr': 'CUR_WWhCCB2016P'},
            {'event_id': '112', 'event_name': 'Le Gruy\xc3\xa8re AOP European Curling Championships 2016',
             'event_href': 'http://www.worldcurling.org/ecc2016', 'event_abbr': 'CUR_ECC2016P'},
            {'event_id': '113', 'event_name': 'Le Gruy\xc3\xa8re AOP European Curling Championships 2016',
             'event_href': 'http://www.worldcurling.org/ecc2016', 'event_abbr': 'CUR_ECCB2016P'
             },
            {'event_id': '110', 'event_name': 'Pacific-Asia Curling Championships 2016',
             'event_href': 'http://www.worldcurling.org/pacc2016', 'event_abbr': 'CUR_PACC2016P'}
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
                standing_item['table_name'] = 'standing'
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
                standing_item['table_name'] = 'standing'
                standing_item['metric_pk'] = standing.get('vc_md5')
                standing_item['data_rows'] = [dict(standing)]
                yield standing_item



