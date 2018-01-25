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
                    home_team_score_list = game.get('ends')[0]
                    home_score_list_cp = deepcopy(home_team_score_list)
                    for i in home_score_list_cp:
                        if i == '':
                            home_team_score_list.remove(i)
                        else:
                            pass
                    team_scores['home_team_score_list'] = home_team_score_list
                    away_team_score_list = game.get('ends')[1]
                    away_team_score_list_cp = deepcopy(away_team_score_list)
                    for j in away_team_score_list_cp:
                        if j == '':
                            away_team_score_list.remove(j)
                    team_scores['away_team_score_list'] = away_team_score_list
                else:
                    self.logger.info('scores list erro or empty')
                    print u'score list 可能为空,链接%s'%response.url
                    self.logger.error(u'score list 可能为空,链接%s'%response.url)
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
                for game_info in game.values():
                    team_scores['division_name'] = game_info.get('draw_name')
                    team_scores['formatted_date'] = game_info.get('formattedDate')
                    team_scores['formatted_time'] = game_info.get('formattedTime')
                    team_scores['game_type'] = game_info.get('game_type')
                    team_scores['sheet_name'] = game_info.get('sheet_name')
                    team_scores['game_id'] = game_info.get('game_id')
                    team_scores['home_team'] = game_info.get('team_a_abbr')
                    team_scores['away_team'] = game_info.get('team_b_abbr')
                    team_scores['home_team_end'] = game_info.get('team_a_end')
                    team_scores['away_team_end'] = game_info.get('team_b_end')
                    ends = game_info.get('ends')
                    home_team_score_list = ends[0]
                    home_score_list_cp = deepcopy(home_team_score_list)
                    for i in home_score_list_cp:
                        if i == '':
                            home_team_score_list.remove(i)
                        else:
                            pass
                    team_scores['home_team_score_list'] = home_team_score_list
                    away_team_score_list = ends[1]
                    away_team_score_list_cp = deepcopy(away_team_score_list)
                    for i in away_team_score_list_cp:
                        if i == '':
                            away_team_score_list.remove(i)
                        else:
                            pass
                    team_scores['away_team_score_list'] = away_team_score_list
                    hammer = game.get('hammer')
                    if hammer == '1':
                        team_scores['hammer'] = team_scores['home_team']
                    elif hammer == '2':
                        team_scores['hammer'] = team_scores['away_team']
                    team_scores['vc_md5'] = gen_md5(
                        '{}#{}#{}'.format(team_scores['event_name'], team_scores['game_session'],
                                          team_scores['game_id']))
                    team_scores['vc_url'] = response.url
                    team_scores_item = dict()
                    team_scores_item['table_name'] = 'team_scores'
                    team_scores_item['metric_pk'] = team_scores.get('vc_md5')
                    team_scores_item['data_rows'] = [dict(team_scores)]
                    yield team_scores_item


            else:
                team_scores_item = dict()
                team_scores_item['table_name'] = 'team_scores'
                team_scores_item['metric_pk'] = team_scores.get('vc_md5')
                team_scores_item['data_rows'] = [dict(team_scores)]
                yield team_scores_item
            # yield team_scores