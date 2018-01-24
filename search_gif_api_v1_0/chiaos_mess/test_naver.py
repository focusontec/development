# coding=utf-8
"""
url1 = 'https://s.search.naver.com/imagesearch/instant/search.naver?where=image&' \
      'section=image&rev=31&ssl=1&res_fr=0&res_to=0&face=0&color=0&ccl=0&ac=0&aq=0&' \
      'spq=1&query=nba gif&nx_search_query=nba gif&nx_and_query=&nx_sub_query=&' \
      'nx_search_hlquery=&nx_search_fasquery=&datetype=0&startdate=0&enddate=0&' \
      'json_type=6&nlu_query=&nqx_theme=&start=151' \
      '&display=100&_callback=window.__jindo2_callback.__sauImageTabList_0'
"""

import requests
from base.tools import generate_UserAgent


class NaverGif():
    """
    发送请求
    解析页面
    组装数据，返回

    """

    def __init__(self, keyword="nba gif", eachPageItemNum = 30):
        self.url = 'https://s.search.naver.com/imagesearch/instant/search.naver?where=image&' \
            'section=image&rev=31&ssl=1&res_fr=0&res_to=0&face=0&color=0&ccl=0&ac=0&aq=0&' \
            'spq=1&query={}&nx_search_query={}&nx_and_query=&nx_sub_query=&' \
            'nx_search_hlquery=&nx_search_fasquery=&datetype=0&startdate=0&enddate=0&' \
            'json_type=6&nlu_query=&nqx_theme=&start=1' \
            '&display=100&_callback=window.__jindo2_callback.__sauImageTabList_0'
        # self.cookies = {
        #     "NNB":"CP3FMWFJDYXFU",
        #     "page_uid":"TAHlzwpVuFRssuHMkxossssssnV - 374697",
        #     "nx_ssl":"2",
        #     "npic":"NnSyl6cjhwsz8C2LZ4 / pHOp0IKgbGUK + 0xD7zMMkbf63Wpoygf7Bl6NVzj7jUoStCA =="
        # }
        self.headers = generate_UserAgent()
        self.keyword = keyword
        self.eachPageItemNum = eachPageItemNum

    def parse_res(self):
        query_url = self.url.format(self.keyword, self.keyword, self.eachPageItemNum)
        res = requests.get(url=self.url, headers=self.headers).content
        print res


if __name__ == '__main__':
    naver = NaverGif()
    naver.parse_res()


