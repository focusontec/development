# -*- coding: utf-8 -*-
import json
import time
from copy import deepcopy

import requests
import scrapy

from Curling.utils.tools import get_today, gen_md5


class PlayerPerformanceSpider(scrapy.Spider):
    count = 1
    name = 'player_performance'
    allowed_domains = ['worldcurling.org','odf2.worldcurling.co']
    start_urls = ['http://www.worldcurling.org/events/2017']

    def parse(self, response):
        event_list = [{"event_name": "World Junior-B Curling Championships 2017", "event_id": "",
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
                       "event_href": "http://www.worldcurling.org/oqe2017", "event_abbr": "CUR_OQE2017P"}]
        for item in event_list:

            if item.get('event_id'):
                event_abbr = item.get('event_abbr')
                event_id = item.get('event_id')
                player_performance['event_name'] = item.get('event_name')
                player_performance['event_id'] = item.get('event_id')
                player_performance['event_abbr'] = event_abbr
                i = 1
                while True:

                    event_session_link = "http://odf2.worldcurling.co/data/{}/{}-session-{}.html?_={}".format(event_abbr,event_id, i, int(round(time.time() * 1000)))
                    status_code = requests.head(event_session_link).status_code
                    if status_code == 200:
                        pass
                    else:
                        break
                    player_performance['game_session'] = str(i)
                    i+=1
                    yield scrapy.Request(url= event_session_link,callback= self.parse_session_data,meta={'player_performance':deepcopy(player_performance)})

            else:
                player_performance = dict()
                player_performance['event_name'] = item.get('event_name')
                player_performance['dt_update'] = get_today()
                player_performance['vc_md5'] = gen_md5('{}#'.format(player_performance['event_name']))

                player_performance_item = dict()
                player_performance_item['table_name'] = 'player_performance'
                player_performance_item['metric_pk'] = player_performance.get('vc_md5')
                player_performance_item['data_rows'] = [dict(player_performance)]
                yield player_performance_item

    def parse_session_data(self,response):
        player_performance = deepcopy(response.meta.get('player_performance'))
        res_to_json = json.loads(response.text)
        for each_game in res_to_json:
            game_id = each_game.get('game_id')
            if  game_id:
                pass
            else:
                continue
            player_performance['game_id'] = game_id
            player_detail_api = 'http://odf2.worldcurling.co/data/{}/{}-game-{}.' \
                                'html?cb={}'.format(player_performance['event_abbr'],
                                                    player_performance['event_id'],
                                                    player_performance['game_id'],
                                                    int(round(time.time() * 1000)))
            yield scrapy.Request(url=player_detail_api,callback= self.parse_json_data,meta={'player_performance':deepcopy(player_performance)})

    def parse_json_data(self,response):
        player_performance = deepcopy(response.meta.get('player_performance'))
        player_performance['vc_url'] = response.url
        game_json_data = json.loads(response.text)
        home_team = game_json_data.get('HOME')
        away_team = game_json_data.get('AWAY')
        team_li = []
        team_li.append(home_team)
        team_li.append(away_team)
        for team in team_li:
            player_performance['team_abbr'] = team.get('abbr')
            player_performance['team_name'] = team.get('teamname')
            player_performance['team_id'] = team.get('team_id')
            line_up = team.get('LINEUP')
            for player in line_up:
                player_performance['player_id'] = player.get('ID')
                player_performance['position'] = player.get('POSITION')
                player_performance['player_role'] = player.get('ROLE')
                player_performance['player_name'] = player.get('DISPLAYNAME')
                pstats = player.get('PSTATS')
                if pstats:
                    # print 'yes we hava pstats*****it is a player***********{}'.format(pstats)
                    player_performance['game_num'] = pstats.get('gameNum')
                    player_performance['game_percent'] = pstats.get('gamePercent')
                    player_performance['draw_num'] = pstats.get('drawNum')
                    player_performance['draw_percent'] = pstats.get('drawPercent')
                    player_performance['takeout_num'] = pstats.get('takeoutNum')
                    player_performance['takeout_percent'] = pstats.get('takeoutPercent')
                    player_performance['dt_update'] = get_today()
                    player_performance['vc_md5'] = gen_md5('{}#{}#{}'.format(player_performance['game_id'],player_performance['player_id'],player_performance['player_name']))
                    player_performance_item = dict()
                    player_performance_item['table_name'] = 'player_performance'
                    player_performance_item['metric_pk'] = player_performance.get('vc_md5')
                    player_performance_item['data_rows'] = [dict(player_performance)]
                    yield player_performance_item

                else:
                    # 没有pstats 数据，说明是教练
                    # print 'no pstats -----this is a coach------------{}'.format(pstats)
                    player_performance['dt_update'] = get_today()
                    player_performance['vc_md5'] = gen_md5('{}#{}#{}'.format(player_performance['game_id'],player_performance['player_id'],player_performance['player_name']))
                    player_performance_item = dict()
                    player_performance_item['table_name'] = 'player_performance'
                    player_performance_item['metric_pk'] = player_performance.get('vc_md5')
                    player_performance_item['data_rows'] = [dict(player_performance)]
                    yield player_performance_item






