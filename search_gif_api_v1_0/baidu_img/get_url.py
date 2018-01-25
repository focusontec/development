# coding=utf-8
import requests
import rson
from copy import deepcopy

import threadpool
from gif_api_v1_0 import app
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# from decode_url import DecodeUrl
from baidu_img.decode_url import DecodeUrl
from base.tools import generate_UserAgent
from base import logger
from base.tools import Cleaner,clean_data

class BaiduImgGifApi(object):
    """
    百度动态图片ａｐｉ
    """
    # 周末的url
    # https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=关键字&cl=2&lm=6&ie=utf-8&oe=utf-8&st=-1&ic=0&word=关键字&istype=2&nc=1&pn=90&rn=30&gsm=5a

    def __init__(self,keyword='nba',pnNum = 0,pageSize = 30):
        # 预留三个位置，1,关键词，2,关键词，3,页码步长是30,如第一页0,第二页30,第三页60
        self.url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&fp=result&queryWord={}&cl=2&lm=6&ie=utf-8&oe=utf-8&st=-1&ic=0&word={}&istype=2&pn={}&rn={}'
        self.keyword = keyword
        # 当前页码
        self.pnNum = pnNum
        # 每页的条目数
        self.pageSize = pageSize
        self.headers = {'User-Agent':generate_UserAgent().get('User-Agent'),'Referer':self.url}


    def parse(self):
        """获取,解析json数据"""

        self.url = self.url.format(self.keyword,self.keyword,int(self.pnNum)*int(self.pageSize),self.pageSize)
        try:
            str_res = requests.get(self.url,headers=self.headers).content.decode()
        except Exception as e:
            print(e)
            try:
                str_res = requests.get(self.url,headers=self.headers).text
            except Exception as e:
                logger.info(e)
                str_res = requests.get(self.url,headers=self.headers).content
        try:
            json_res = rson.loads(unicode(str_res).replace('\'','\"'))
        except Exception as e:
            logger.info(e)
            return
        data = json_res.get(u'data')
        total_image_num = json_res.get(u'listNum')
        if data != [{}]:
            data = data[:-1]

            each_page_imges = []
            for item in data:
                image_info = dict()
                image_info[u'mainTag'] = ""
                image_info[u'slaveTag'] = []
                image_info[u'imgTitle'] = item.get(u'fromPageTitle')
                if bool(item.get(u'objURL')):
                    image_info[u'src'] = DecodeUrl().decode(item.get(u'objURL'))
                else:
                    image_info[u'src'] = None
                # 获取图片来源网站
                if bool(item.get(u'fromURL')):
                    image_info[u'fromUrl'] = DecodeUrl().decode(item.get(u'fromURL'))
                else:
                    image_info[u'fromUrl'] = None
                each_page_imges.append(image_info)

        else:
            return [],total_image_num
        # 开线程，请求图片地址，ａｓｓｅｒｔ　＝＝　２００　；　否则删除
        pool = app.pool
        temp_cont = []
        for item in each_page_imges:
            reqs = threadpool.makeRequests(clean_data, [([str(item), temp_cont], None)])
            [pool.putRequest(req) for req in reqs]
        pool.wait()

        return  temp_cont,total_image_num
        cc = Cleaner(each_page_imges)
        cc.task_()
        each_page_imges = cc.clean_data
        return  each_page_imges,total_image_num



if __name__ == '__main__':
    baidu1 = BaiduImgGifApi()
    urls,num = baidu1.parse()
    print(urls,num)


