# coding=utf-8
"""
url1 = 'https://s.search.naver.com/imagesearch/instant/search.naver?where=image&' \
      'section=image&rev=31&ssl=1&res_fr=0&res_to=0&face=0&color=0&ccl=0&ac=0&aq=0&' \
      'spq=1&query=nba gif&nx_search_query=nba gif&nx_and_query=&nx_sub_query=&' \
      'nx_search_hlquery=&nx_search_fasquery=&datetype=0&startdate=0&enddate=0&' \
      'json_type=6&nlu_query=&nqx_theme=&start=151' \
      '&display=100&_callback=window.__jindo2_callback.__sauImageTabList_0'
"""
import json
from lxml import etree
import requests
import re
from base import logger
from base.tools import generate_UserAgent, unquote_url, Cleaner


class NaverGif():
    """
    发送请求
    解析页面
    组装数据，返回

    """
    def __init__(self,keyword = 'nba gif ',eachPageItemNum = 20,start = 1,pnNum = 0):

        self.url = 'https://s.search.naver.com/imagesearch/instant/search.naver?where=image&' \
        'section=image&rev=31&ssl=1&' \
        'spq=1&query={}&nx_search_query={}&' \
        'json_type=6&start={}' \
        '&display={}&_callback=window.__jindo2_callback.__sauImageTabList_0'
        self.headers = generate_UserAgent()
        self.keyword = keyword
        if not self.keyword.strip().endswith('gif'):
            self.keyword = keyword+' gif'
        else:
            pass
        self.eachPageItemNum = eachPageItemNum
        self.start = start
        self.pnNum = pnNum


    def parse_res(self):
        query_url = self.url.format(self.keyword,self.keyword,self.start,self.eachPageItemNum)
        try:
            res = requests.get(url=query_url,headers = self.headers).content
        except Exception as e:
            logger.info(e)
            res = requests.get(url=query_url,headers = self.headers).text
        res = res.strip()
        patterns = re.compile(r'.*?window\.__jindo2_callback\.__sauImageTabList_0\((.*?)\)$',re.S)
        json_data = patterns.findall(res)[0]
        dict_data = json.loads(json_data)
        result = dict_data.get('result')
        totalSearchNum = result.get('total')
        if totalSearchNum:
            # items 的样式为 {'item':[{},{},{}]}
            items = result.get('items')
            if items:
                item_list = items.get('item')
                each_page_imges = []
                for item in item_list:
                    img_info = dict()
                    html_str = item.get('html')
                    etree_html = etree.HTML(html_str)
                    contentInSpan = etree_html.xpath('//span[@class="_meta"]/text()')[0] if len(etree_html.xpath('//span[@class="_meta"]/text()'))>0 else None
                    contentToDict = json.loads(contentInSpan)
                    imageTitle = contentToDict.get('title')
                    imageFrom = contentToDict.get('link')
                    imageUrl = contentToDict.get('originalUrl')
                    if not imageUrl.endswith('gif'):
                        continue
                    imagePublishDate = contentToDict.get('date')
                    # 组装数据
                    img_info['fromUrl'] =unquote_url(imageFrom)
                    img_info['src'] = unquote_url(imageUrl)
                    img_info['imgTitle'] = imageTitle
                    img_info['mainTag'] = ""
                    img_info['slavaTag'] = []
                    each_page_imges.append(img_info)
                cc = Cleaner(each_page_imges)
                cc.task_()
                each_page_imges = cc.clean_data
                return each_page_imges,totalSearchNum

        else:
            return None,None




if __name__ == '__main__':
    naver = NaverGif(keyword="得分")
    a = naver.parse_res()
    print a
    print len(a[0])



