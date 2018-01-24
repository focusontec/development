import requests
from base.tools import get_proxies,generate_UserAgent
from lxml import etree
class YandexGif(object):
    def __init__(self,keyword,pageIndex):
        self.url = "https://yandex.com/images/search?p={}&text={}&itype=gif&rpt=image"
        self.keyword = keyword
        self.pageIndex = pageIndex
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0"}
    def parse_gif(self):
        res_temp = requests.get(url=self.url.format(self.pageIndex,self.keyword),headers = generate_UserAgent(),proxies=get_proxies())
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
