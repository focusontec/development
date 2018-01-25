# -*- coding: utf-8 -*-
import re
import time
from copy import deepcopy
import scrapy
from Curling.utils.tools import gen_md5, get_today


class TeamAndPlayerSpider(scrapy.Spider):
    name = 'team_and_player'
    allowed_domains = ['worldcurling.org']
    start_urls = ['http://www.worldcurling.org/events/2017/']

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
        for event in event_list:
            if event.get('event_id') == "":
                # 说明该赛事下没有信息
                team_and_player = dict()
                team_and_player['event_name'] = event.get('event_name')
                team_and_player['vc_md5'] = gen_md5('{}#{}'.format(event.get('event_name'),event.get('event_href')))
                team_and_player['dt_update'] = get_today()
                # yield team_and_player
                team_and_player_item = dict()
                team_and_player_item['table_name'] = 'team_and_player'
                team_and_player_item['metric_pk'] = team_and_player.get('vc_md5')
                team_and_player_item['data_rows'] = [dict(team_and_player)]
                yield team_and_player_item
            else:
                team_and_player = dict()
                team_and_player['event_name'] = event.get('event_name')
                team_and_player['event_id'] = event.get('event_id')
                yield scrapy.Request(event.get('event_href') + "/teams", callback=self.parse_event,
                                     meta={"team_and_player": deepcopy(team_and_player)})
    def parse_event(self,response):

        team_and_player = response.meta.get('team_and_player')
        team_n_type_selector = response.xpath('//div[@class="textblock5 textblockBODY tbnormal"]|//div[@class="textblock1 textblockBODY tbnormal"]')
        if len(team_n_type_selector) == 0:
            # 表示没有team可查
            team_and_player['dt_update'] = get_today()
            team_and_player['vc_md5'] = gen_md5('{}#{}'.format(team_and_player['event_name'],team_and_player['event_id']))
            # team_and_player['vc_url'] = response.url
            # yield team_and_player
            team_and_player_item = dict()
            team_and_player_item['table_name'] = 'team_and_player'
            team_and_player_item['metric_pk'] = team_and_player.get('vc_md5')
            team_and_player_item['data_rows'] = [dict(team_and_player)]
            yield team_and_player_item

        else:
            team_and_player['vc_url'] = response.url
            # 获取分组类型的index
            team_type_index_list = []
            i = 0
            for item in team_n_type_selector:
                if item.xpath('./@class').extract_first() == "textblock5 textblockBODY tbnormal":
                    team_type_index_list.append(i)
                i+=1

            # 对获取到的下标进行分组
            if team_type_index_list:
                team_type_group = [team_type_index_list[x:x+2] for x in range(len(team_type_index_list))]
                for index_group in team_type_group:
                    if len(index_group) == 2:
                        # 球员节点
                        team_selectors = team_n_type_selector[index_group[0]+1:index_group[1]]
                        # 分组的名字节点
                        team_type_name = team_n_type_selector[index_group[0]]
                    else:
                        # 说明是最后一个分组
                        team_type_name = team_n_type_selector[index_group[0]]
                        team_selectors = team_n_type_selector[index_group[0] + 1:]
                    for team in team_selectors:
                        team_and_player['division_name'] = team_type_name.xpath('.//h2//text()').extract_first()
                        # todo 处理队伍名，去掉带括号的部分
                        team_name = team.xpath('.//h2/text()').extract_first()
                        full_team_name = team_name.split('(')[0]
                        team_and_player['team_name'] = full_team_name
                        team_and_player['pic_url'] = "http://www.worldcurling.org"+team.xpath('.//div[@class="image"]/img/@src').extract_first() if len(team.xpath('.//div[@class="image"]/img'))>0 else None
                        judge_b = team.xpath('.//b')
                        if len(judge_b) == 0:
                            players_list = team.xpath('.//div[@class="text"]//text()').extract()
                            for player in players_list:
                                split_by_colon  = player.split(':')
                                if len(split_by_colon) == 2:
                                    team_and_player['player_pos'] = split_by_colon[0]
                                    player_name_n_role = split_by_colon[1]
                                else:
                                    team_and_player['player_pos'] = player.split('-')[0]
                                    player_name_n_role = '-'.join(player.split('-')[1:])
                                res = re.search(r'(.+?)(\(.*\))',player_name_n_role)
                                if res :
                                    # 标注了role的队员
                                    team_and_player['player_role'] = res.group(2).replace('(',"").replace(')','').replace(' ',',')
                                    team_and_player['player_name'] = res.group(1).strip(' ')
                                else:
                                    # 没有注明role的队员
                                    team_and_player['player_role'] = None
                                    team_and_player['player_name'] = player_name_n_role.strip(' ')
                                team_and_player['dt_update'] = get_today()
                                team_and_player['vc_md5'] = gen_md5("{}#{}#{}".format(team_and_player['vc_url'],team_and_player['team_name'],team_and_player['player_name']))
                                # yield team_and_player
                                team_and_player_item = dict()
                                team_and_player_item['table_name'] = 'team_and_player'
                                team_and_player_item['metric_pk'] = team_and_player.get('vc_md5')
                                team_and_player_item['data_rows'] = [dict(team_and_player)]
                                yield team_and_player_item
                        else:
                            # 新版面，team节点下面有b标签
                            players_list = team.xpath('.//div[@class="text"]//text()').extract()
                            if len(players_list)%2 != 0:
                                print 'error______________+++++++++___________________'
                                return
                            pos_n_name = [players_list[x:x + 2] for x in range(0,len(players_list),2)]
                            for each_player in pos_n_name:
                                team_and_player['player_pos'] = each_player[0].replace(':','')
                                player_name_n_role = each_player[1]
                                res = re.search(r'(.+?)(\(.*\))',player_name_n_role)
                                if res:
                                    team_and_player['player_role'] = res.group(2).replace('(',"").replace(')','').replace(' ',',')
                                    team_and_player['player_name'] = res.group(1).strip(' ')
                                else:
                                    team_and_player['player_role'] = None
                                    team_and_player['player_name'] = player_name_n_role.strip(' ')
                                team_and_player['dt_update'] = get_today()
                                team_and_player['vc_md5'] = gen_md5(
                                    "{}#{}#{}".format(team_and_player['vc_url'], team_and_player['team_name'],
                                                      team_and_player['player_name']))
                                # yield team_and_player
                                team_and_player_item = dict()
                                team_and_player_item['table_name'] = 'team_and_player'
                                team_and_player_item['metric_pk'] = team_and_player.get('vc_md5')
                                team_and_player_item['data_rows'] = [dict(team_and_player)]
                                yield team_and_player_item
            else:
                # 说明有队员但是没有分组
                team_and_player['division_name'] = None
                team_and_player['dt_update'] = get_today()
                for team in team_n_type_selector:
                    team_name = team.xpath('.//h2/text()').extract_first()
                    full_team_name = team_name.split('(')[0]
                    team_and_player['team_name'] = full_team_name
                    team_and_player['pic_url'] ="http://www.worldcurling.org" + team.xpath('.//div[@class="image"]/img/@src').extract_first()
                    players_list = team.xpath('.//div[@class="text"]//text()').extract()
                    for player in players_list:
                        # [u'Female: Ekaterina Kirillova',
                        #  u'Male: Ilya Shalamitski',
                        #  u'Coach: Anton Batugin']
                        split_by_colon = player.split(':')
                        if len(split_by_colon) == 2:
                            team_and_player['player_pos'] = split_by_colon[0]
                            player_name_n_role = split_by_colon[1]
                        else:
                            team_and_player['player_pos'] = player.split('-')[0]
                            player_name_n_role = '-'.join(player.split('-')[1:])
                        res = re.search(r'(.+?)(\(.*\))', player_name_n_role)
                        if res:
                            team_and_player['player_role'] = res.group(2).replace('(',"").replace(')','').replace(' ',',')
                            team_and_player['player_name'] = res.group(1).strip(' ')
                        else:
                            team_and_player['player_role'] = None
                            team_and_player['player_name'] = player_name_n_role.strip(' ')
                        team_and_player['vc_md5'] = gen_md5(
                                    "{}#{}#{}".format(team_and_player['vc_url'], team_and_player['team_name'],
                                                      team_and_player['player_name']))
                        # yield team_and_player
                        team_and_player_item = dict()
                        team_and_player_item['table_name'] = 'team_and_player'
                        team_and_player_item['metric_pk'] = team_and_player.get('vc_md5')
                        team_and_player_item['data_rows'] = [dict(team_and_player)]
                        yield team_and_player_item


















