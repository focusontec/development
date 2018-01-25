# -*- coding: utf-8 -*-
import json
import time
from copy import deepcopy

import requests
import scrapy

from Curling.utils.tools import get_today, gen_md5


class PlayByPlaySpider(scrapy.Spider):
    name = 'play_by_play'
    allowed_domains = ['worldcurling.org',"odf2.worldcurling.co",]
    start_urls = ['http://www.worldcurling.org/events/2017/']

    def parse(self, response):
        # print u'-------------------开门红--------------------'
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
    #     for item in event_list:
    #
    #         if item.get('event_id'):
    #             event_abbr = item.get('event_abbr')
    #             event_id = item.get('event_id')
    #             player_performance['event_name'] = item.get('event_name')
    #             player_performance['event_id'] = item.get('event_id')
    #             player_performance['event_abbr'] = event_abbr
    #             i = 1
    #             while True:
    #
    #                 event_session_link = "http://odf2.worldcurling.co/data/{}/{}-session-{}.html?_={}".format(
    #                     event_abbr, event_id, i, int(round(time.time() * 1000)))
    #                 status_code = requests.head(event_session_link).status_code
    #                 if status_code == 200:
    #                     pass
    #                 else:
    #                     break
    #                 player_performance['game_session'] = str(i)
    #                 i += 1
    #                 yield scrapy.Request(url=event_session_link, callback=self.parse_session_data,
    #                                      meta={'player_performance': deepcopy(player_performance)})
    #
    #         else:
    #             player_performance = dict()
    #             player_performance['event_name'] = item.get('event_name')
    #             player_performance['dt_update'] = get_today()
    #             player_performance['vc_md5'] = gen_md5('{}#'.format(player_performance['event_name']))
    #
    #             play_by_play_item = dict()
    #             play_by_play_item['table_name'] = 'play_by_play'
    #             play_by_play_item['metric_pk'] = player_performance.get('vc_md5')
    #             play_by_play_item['data_rows'] = [dict(player_performance)]
    #             yield play_by_play_item
    #
    # def parse_session_data(self, response):
    #     player_performance = deepcopy(response.meta.get('player_performance'))
    #     res_to_json = json.loads(response.text)
    #     for each_game in res_to_json:
    #         game_id = each_game.get('game_id')
    #         if game_id:
    #             pass
    #         else:
    #             continue
    #         player_performance['game_id'] = game_id
    #         player_detail_api = 'http://odf2.worldcurling.co/data/{}/{}-game-{}.' \
    #                             'html?cb={}'.format(player_performance['event_abbr'],
    #                                                 player_performance['event_id'],
    #                                                 player_performance['game_id'],
    #                                                 int(round(time.time() * 1000)))
    #         yield scrapy.Request(url=player_detail_api, callback=self.parse_json_data,
    #                              meta={'player_performance': deepcopy(player_performance)})
    #
    # def parse_json_data(self, response):
    #     play_by_play = deepcopy(response.meta.get('player_performance'))
    #     play_by_play['vc_url'] = response.url
    #     game_json_data = json.loads(response.text)
    #     home_team = game_json_data.get('HOME')
    #     away_team = game_json_data.get('AWAY')
    #     team_li = []
    #     team_li.append(home_team)
    #     team_li.append(away_team)
        for item in event_list:
            print u'正在爬取event--------{}'.format(item.get('event_id'))
            if item.get('event_id'):
                play_by_play = dict()
                event_abbr = item.get('event_abbr')
                event_id = item.get('event_id')
                play_by_play['event_name'] = item.get('event_name')
                play_by_play['event_id'] = item.get('event_id')
                play_by_play['event_abbr'] = event_abbr
                i = 1
                while True:

                    event_session_link = "http://odf2.worldcurling.co/data/{}/{}-session-{}.html?_={}".format(
                        event_abbr, event_id, i, int(round(time.time() * 1000)))
                    status_code = requests.head(event_session_link).status_code
                    if status_code == 200:
                        pass
                    else:
                        break
                    play_by_play['game_session'] = str(i)
                    i += 1
                    yield scrapy.Request(url=event_session_link, callback=self.parse_session_data,
                                         meta={'play_by_play': deepcopy(play_by_play)})

            else:
                play_by_play = dict()
                play_by_play['event_name'] = item.get('event_name')
                play_by_play['dt_update'] = get_today()
                play_by_play['vc_md5'] = gen_md5('{}#'.format(play_by_play['event_name']))

                play_by_play_item = dict()
                play_by_play_item['table_name'] = 'play_by_play'
                play_by_play_item['metric_pk'] = play_by_play.get('vc_md5')
                play_by_play_item['data_rows'] = [dict(play_by_play)]
                yield play_by_play_item

    def parse_session_data(self, response):
        play_by_play = deepcopy(response.meta.get('play_by_play'))
        res_to_json = json.loads(response.text)
        for each_game in res_to_json:
            # 不规则数据异常处理
            try:
                game_id = each_game.get('game_id')
            except Exception as e:
                print u'错误信息：{},url:{}'.format(e, response.url)
                self.logger(u'错误信息：{},url:{}'.format(e, response.url))
                game_info = each_game.values()
                for game in game_info:
                    game_id = game.get('game_id')
                    if game_id:
                        pass
                    else:
                        continue
                    play_by_play['game_id'] = game_id
                    player_detail_api = 'http://odf2.worldcurling.co/data/{}/{}-game-{}.' \
                                        'html?cb={}'.format(play_by_play['event_abbr'],
                                                            play_by_play['event_id'],
                                                            play_by_play['game_id'],
                                                            int(round(time.time() * 1000)))
                    yield scrapy.Request(url=player_detail_api, callback=self.parse_json_data,
                                         meta={'play_by_play': deepcopy(play_by_play)})
            else:
                # 规范数据的处理
                if game_id:
                    pass
                else:
                    continue
                play_by_play['game_id'] = game_id
                player_detail_api = 'http://odf2.worldcurling.co/data/{}/{}-game-{}.' \
                                    'html?cb={}'.format(play_by_play['event_abbr'],
                                                        play_by_play['event_id'],
                                                        play_by_play['game_id'],
                                                        int(round(time.time() * 1000)))
                yield scrapy.Request(url=player_detail_api, callback=self.parse_json_data,
                                     meta={'play_by_play': deepcopy(play_by_play)})

    def parse_json_data(self, response):
        play_by_play = deepcopy(response.meta.get('play_by_play'))
        play_by_play['vc_url'] = response.url
        game_json_data = json.loads(response.text)
        home_team = game_json_data.get('HOME')
        away_team = game_json_data.get('AWAY')
        team_li = []
        team_li.append(home_team)
        team_li.append(away_team)
        for team in team_li:
            play_by_play['team_id'] = team.get('team_id')
            play_by_play['team_name'] = team.get('teamname')
            play_by_play['team_abbr'] = team.get('abbr')
            pplay_by_play = team.get('PPLAY_BY_PLAY')
            # 16年赛事没有PPLAY_BY_PLAY字段信息
            if pplay_by_play:
                if len(pplay_by_play) == 1:
                    # 长度为1 说明只有一个MSG信息，没有球的信息
                    play_by_play['vc_md5'] = gen_md5('#{}#{}#{}'.format(play_by_play['event_id'],play_by_play['game_id'],play_by_play['team_id']))
                    play_by_play['dt_update'] = get_today()
                    play_by_play_item = dict()
                    play_by_play_item['table_name'] = 'play_by_play'
                    play_by_play_item['metric_pk'] = play_by_play.get('vc_md5')
                    play_by_play_item['data_rows'] = [dict(play_by_play)]
                    yield play_by_play_item
                    # yield play_by_play
                else:
                    pass
                play_serial_no = 1
                for game_info in pplay_by_play[1:]:
                    # 遍历每场得信息
                    play_by_play['play_serial_no'] = play_serial_no
                    play_serial_no +=1
                    stone_info = game_info.get('STONES')
                    if stone_info:
                        pass
                    else:
                        play_by_play['vc_md5'] = gen_md5('{}#{}#{}'.format(play_by_play['event_id'],play_by_play['game_id'],play_by_play['team_id']))
                        play_by_play['dt_update'] = get_today()
                        play_by_play_item = dict()
                        play_by_play_item['table_name'] = 'play_by_play'
                        play_by_play_item['metric_pk'] = play_by_play.get('vc_md5')
                        play_by_play_item['data_rows'] = [dict(play_by_play)]
                        yield play_by_play_item
                        # yield play_by_play
                    for each_stone in stone_info.items():
                        stone = each_stone[1]
                        if stone.get('OWNER') == 'Y':
                            play_by_play['stones_num'] = stone.get('SN')
                            play_by_play['player_name'] = stone.get('PLAYERNAME')
                            play_by_play['player_id'] = stone.get('PLAYER')
                            play_by_play['player_task'] = stone.get('TASK')
                            play_by_play['turn'] = stone.get('HANDLE')
                            play_by_play['points'] = stone.get('POINTS')
                            play_by_play['E_S'] = stone.get('ES')
                            play_by_play['img_url'] = 'http://odf2.worldcurling.co/data/{}/play_by_play/{}/{}.jpg'.format(play_by_play['event_abbr'],
                                                                                                                              play_by_play['game_id'],
                                                                                                                               play_by_play['E_S'])
                            play_by_play['vc_md5'] = gen_md5('{}#{}#{}#{}'.format(play_by_play['event_id'],play_by_play['game_id'],play_by_play['play_serial_no'],play_by_play['stones_num']))
                            play_by_play['dt_update'] = get_today()
                            play_by_play_item = dict()
                            play_by_play_item['table_name'] = 'play_by_play'
                            play_by_play_item['metric_pk'] = play_by_play.get('vc_md5')
                            play_by_play_item['data_rows'] = [dict(play_by_play)]
                            yield play_by_play_item
                        else:
                            continue

            else:
                # pplay_by_play为None
                play_by_play['dt_update'] = get_today()
                play_by_play['vc_md5'] = gen_md5('{}#{}#{}'.format(play_by_play['event_id'],play_by_play['game_id'],play_by_play['team_id']))
                play_by_play_item = dict()
                play_by_play_item['table_name'] = 'play_by_play'
                play_by_play_item['metric_pk'] = play_by_play.get('vc_md5')
                play_by_play_item['data_rows'] = [dict(play_by_play)]
                yield play_by_play_item




