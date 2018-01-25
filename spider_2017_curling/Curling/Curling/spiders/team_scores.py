# -*- coding: utf-8 -*-
import json
import time
from copy import deepcopy

import requests
import scrapy

from Curling.utils.tools import get_today, gen_md5


class TeamScoresSpider(scrapy.Spider):
    name = 'team_scores'
    allowed_domains = ['worldcurling.org','odf2.worldcurling.co']
    start_urls = ['http://worldcurling.org/']

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
            team_scores = dict()
            team_scores['event_name'] = item.get('event_name')
            team_scores['dt_update'] = get_today()

            # score_api = "http://odf2.worldcurling.co/data/CUR_WJCC2017P/118-session-30.html?_=1515052838407"
            i = 1
            event_abbr = item.get('event_abbr')
            event_id = item.get("event_id")
            if item.get('event_id'):
                while True:
                    score_api = "http://odf2.worldcurling.co/data/{}/{}-session-{}.html?_={}".format(event_abbr,event_id,i,int(round(time.time()*1000)))

                    # print score_api
                    status_code = requests.head(score_api).status_code
                    if status_code == 200:
                        pass
                    elif status_code == 404:
                        # 再次尝试
                        print 'break----- %s-----%s------%s'%(score_api,status_code,type(status_code))
                        break
                    else:
                        print u'------出现其他状态码，需要注意'
                        time.sleep(3)
                        self.logger.info(u'------出现其他状态码，需要注意%s'%score_api)
                    team_scores['event_id'] = item.get('event_id')
                    team_scores['game_session'] = str(i)
                    i += 1
                    yield scrapy.Request(url=score_api,callback= self.parse_detail,meta={'team_scores':deepcopy(team_scores)})
            else:
                team_scores['vc_md5'] = gen_md5("{}#{}".format(team_scores['event_name'],item.get('event_href')))

                team_scores_item = dict()
                team_scores_item['table_name'] = 'team_scores'
                team_scores_item['metric_pk'] = team_scores.get('vc_md5')
                team_scores_item['data_rows'] = [dict(team_scores)]
                yield team_scores_item
                # yield team_scores

    def parse_detail(self,response):
        # TODO 使用logging模块记录异常，后期可以手动补数据

        # response 为每个session对应的game
        team_scores = response.meta.get('team_scores')
        data_li = json.loads(response.text)
        # 每个session可以有多长比赛

        for game in data_li:
            try:
                team_scores['division_name'] = game.get('draw_name')
                team_scores['formatted_date'] = game.get('formattedDate')
                team_scores['formatted_time'] = game.get('formattedTime')
                team_scores['game_type'] = game.get('game_type')
                team_scores['sheet_name'] = game.get('sheet_name')
                team_scores['game_id'] = game.get('game_id')
                team_scores['home_team'] = game.get('team_a_abbr')
                team_scores['away_team'] = game.get('team_b_abbr')
                team_scores['home_team_end'] = game.get('team_a_end')
                team_scores['away_team_end'] = game.get('team_b_end')
                team_scores['home_team_total_score'] = game.get('team_a_score')
                team_scores['away_team_total_score'] = game.get('team_b_score')
                if game.get('ends') is not None and len(game.get('ends')) == 2:
                    team_scores['home_team_score_list'] = game.get('ends')[0][1:int(team_scores['home_team_end']) + 1] if game.get('ends') else None
                    team_scores['away_team_score_list'] = game.get('ends')[1][1:int(team_scores['away_team_end']) + 1] if game.get('ends') else None
                else:
                    self.logger.info('scores list erro or empty')
                    print u'score list 可能为空,链接%s'%response.url
                    self.logger.error(u'score list 可能为空,链接%s'%response.url)
                    time.sleep(3)
                hammer = game.get('hammer')
                if hammer == '1':
                    team_scores['hammer'] = team_scores['home_team']
                elif hammer == '2':
                    team_scores['hammer'] = team_scores['away_team']
                team_scores['vc_md5'] = gen_md5('{}#{}#{}'.format(team_scores['event_name'],team_scores['game_session'],team_scores['game_id']))
                team_scores['vc_url'] = response.url
            except Exception as e:
                self.logger.error(u'抓不到数据了，链接%s,错误类型：%s'%(response.url,e.message))
                print u'been logged,see log files'
                time.sleep(3)
            else:
                team_scores_item = dict()
                team_scores_item['table_name'] = 'team_scores'
                team_scores_item['metric_pk'] = team_scores.get('vc_md5')
                team_scores_item['data_rows'] = [dict(team_scores)]
                yield team_scores_item
            # yield team_scores