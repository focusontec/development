import requests
import time

from base.tools import get_proxies,generate_UserAgent
from lxml import etree
class YandexGif(object):
    def __init__(self,keyword,pageIndex):
        self.url = "https://yandex.com/images/search?callback=jQuery21405543355148398587_{}&" \
                   "format=json&request=%7B%22blocks%22%3A%5B%7B%22block%22%3A%22i-global__params%3Aajax%22%2C%22params%22%3A%7B%7D%2C%22version%22%3A2%7D%2C%7B%22block%22%3A%22cookies_ajax%22%2C%22params%22%3A%7B%7D%2C%22version%22%3A2%7D%2C%7B%22block%22%3A%22search2%3Aajax%22%2C%22params%22%3A%7B%7D%2C%22version%22%3A2%7D%2C%7B%22block%22%3A%22advanced-search__filters%22%2C%22params%22%3A%7B%7D%2C%22version%22%3A2%7D%2C%7B%22block%22%3A%22preview__isWallpaper%22%2C%22params%22%3A%7B%7D%2C%22version%22%3A2%7D%2C%7B%22block%22%3A%22content_type_search%22%2C%22params%22%3A%7B%7D%2C%22version%22%3A2%7D%2C%7B%22block%22%3A%22serp-controller%22%2C%22params%22%3A%7B%7D%2C%22version%22%3A2%7D%5D%2C%22bmt%22%3A%7B%22lb%22%3A%22%22%7D%2C%22amt%22%3A%7B%22las%22%3A%22%22%7D%7D&yu=5383584061512963070&text=%E5%93%88%E5%93%88&" \
                   "itype=gif&" \

        self.keyword = keyword
        self.pageIndex = pageIndex
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0"}
    def parse_gif(self):
        res_temp = requests.get(url=self.url.format(round(time.time()*1000)),headers = generate_UserAgent(),proxies=get_proxies())
        print get_proxies()
        try:
            res = res_temp.content
        except Exception as e:
            res = res_temp.texts

        print res
        print type(res)
        if isinstance(res,str):
            etree_html = etree.HTML(res)
            div_list_bem = etree_html.xpath('//div[contains(@class,"serp-item serp-item_type_search serp-item_group_search serp-item_pos_")]')
            for div in div_list_bem:
                data_bem_json = div.xpath('./@data-bem')[0]
                print data_bem_json
            print len(div_list_bem)
        else:
            return


if __name__ == '__main__':
    yan = YandexGif('nba','1')
    yan.parse_gif()
