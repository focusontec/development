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

            print u'正在爬取event--------{}'.format(item.get('event_id'))
            if item.get('event_id'):
                player_performance = dict()
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
            # 不规则数据异常处理
            try:
                game_id = each_game.get('game_id')
            except Exception as e:
                print u'错误信息：{},url:{}'.format(e,response.url)
                self.logger(u'错误信息：{},url:{}'.format(e,response.url))
                game_info  = each_game.values()
                for game in game_info:
                    game_id = game.get('game_id')
                    if game_id:
                        pass
                    else:
                        continue
                    player_performance['game_id'] = game_id
                    player_detail_api = 'http://odf2.worldcurling.co/data/{}/{}-game-{}.' \
                                        'html?cb={}'.format(player_performance['event_abbr'],
                                                            player_performance['event_id'],
                                                            player_performance['game_id'],
                                                            int(round(time.time() * 1000)))
                    yield scrapy.Request(url=player_detail_api, callback=self.parse_json_data,
                                         meta={'player_performance': deepcopy(player_performance)})
            else:
                # 规范数据的处理
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
            if line_up:
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

            else:
                # 不存在line_up字段，说明没有球员表现的数据，直接返回
                player_performance['vc_md5'] = gen_md5(
                    '{}#{}#{}'.format(player_performance['event_id'], player_performance['game_id'],
                                      player_performance['team_id']))
                player_performance_item = dict()
                player_performance_item['table_name'] = 'player_performance'
                player_performance_item['metric_pk'] = player_performance.get('vc_md5')
                player_performance_item['data_rows'] = [dict(player_performance)]
                yield player_performance_item








