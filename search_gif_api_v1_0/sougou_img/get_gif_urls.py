# coding=utf-8
"http://pic.sogou.com/pics?query=%D0%A1%C4%F1&mode=0&st=1&start=0&reqType=ajax&reqFrom=result"
"http://pic.sogou.com/pics?query=%B4%F2%B8%F2%F3%A1&mode=0&leftp=44230502&st=1&start=96&reqType=ajax&reqFrom=result&tn=0"
import requests
import rson
from base.tools import generate_UserAgent, Cleaner
from base import logger
class SougouGIfApi(object):

    def __init__(self,pageNum=0,keyword=u'nba'):
        self.keyword = keyword
        # 页码规则 48*i   ,i = 0 ,i +=1
        self.pageNum = pageNum
        self.gifApi = u'http://pic.sogou.com/pics?query={}&mode=0&leftp=44230502&st=1&start={}&reqType=ajax&reqFrom=result'

    def __parse_gif(self):
        formated_api = self.gifApi.format(self.keyword,int(self.pageNum)*48)
        # 获取json数据
        try:
            str_res = requests.get(formated_api,generate_UserAgent()).text

        except Exception as e:
            logger.info(e)
            print(e)
            str_res = requests.get(self.gifApi.format(self.keyword, self.pageNum)).content.decode()
        if isinstance(str_res,unicode):

            pass
        else:
            return None,None
        try:
            json_res = rson.loads(str_res)
        except Exception as e:
            logger.info(e)
            return
        # 获取总共的条目
        total_images = json_res.get(u'maxEnd')
        gif_list = json_res.get(u'items')
        modelList = []
        for item in gif_list:

            image_info = dict()
            image_info[u'mainTag'] = ''
            image_info[u'slaveTag'] = []
            if item.get(u'picUrl'):
                image_info[u'src'] = item.get(u'pic_url')
            else:
                image_info[u'src'] = item.get(u'pic_url_noredirect')
            image_info[u'fromUrl'] = item.get(u'page_url')
            image_info[u'imgTitle'] = item.get(u'title')
            modelList.append(image_info)
        cc = Cleaner(modelList)
        cc.task_()
        each_page_imges = cc.clean_data
        return each_page_imges,total_images

    def parse_gif(self):

        return self.__parse_gif()


if __name__ == '__main__':
    sougou = SougouGIfApi()
    content = sougou.parse_gif()
    print(content)
    print(len(content))


