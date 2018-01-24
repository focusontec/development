# coding=utf-8
import requests
import re
import json
from lxml import etree

from base.tools import Cleaner


class Yahoo_gif(object):
    def __init__(self,keyword='nba',startNum = 1):
        # 说明： n = 60 测试过，已经写死，改动无用。每页固定返回60条，
        # b = 1 是起始的条目，代表first：1 ，条目是60 ，last因此为60
        self.gif_api = 'https://images.search.yahoo.com/search/images?imgty=gif&n=60&ei=UTF-8&fr=yfp-t&fr2=sb-top-images.search.yahoo.com&o=js&p={}&tab=organic&tmpl=&nost=1&b={}&iid=Y.1'
        self.keyword = keyword
        self.startNun = startNum

    def __parse_html(self):
        str_res = requests.get(self.gif_api.format(self.keyword,self.startNun)).content
        res_to_dict = json.loads(str_res)
        search_res_html = res_to_dict.get('html')
        meta_data = res_to_dict.get('meta')

        total_num = meta_data.get('total') if meta_data else 0

        modelList = []
        if search_res_html:
            e_res_html = etree.HTML(search_res_html)
            pic_list_node = e_res_html.xpath('//ul[@id="sres"]/li')
            for pic_li_node in pic_list_node:
                image_info = dict()
                data = pic_li_node.xpath('./@data')[0] if len(pic_li_node.xpath('./@data'))>0 else None
                if data:
                    data_dict = json.loads(data)

                    image_info[u'src'] = data_dict.get('iurl')
                    image_info[u'fromUrl'] = data_dict.get('rurl')
                    image_info[u'imgTitle'] = pic_li_node.xpath('./a/@aria-label')[0] if pic_li_node.xpath('./a/@aria-label') else ''
                    image_info[u'slaveTag'] = []
                    image_info[u'mainTag'] = ""
                modelList.append(image_info)
        cc = Cleaner(modelList)
        cc.task_()
        modelList = cc.clean_data
        return modelList,total_num

    def get_yahoo_gif(self):
        image_info,total_num =  self.__parse_html()
        return image_info,total_num


if __name__ == '__main__':
    ya = Yahoo_gif('大风')
    print ya.get_yahoo_gif()
