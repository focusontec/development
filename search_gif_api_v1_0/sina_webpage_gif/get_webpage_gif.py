# coding=utf-8
import json
import re

from sina_webpage_gif.redis_db import LoginInfo
from weibo_login.wb_login import zLoginGenCookie,zBackCookie,popExpCookie
import urllib
import requests
from lxml import etree
from base import logger
from base.tools import generate_UserAgent

class Sina(object):
    def __init__(self,keyword='nba',pageNum = 1,isNormal = 1):
        self.keyword = keyword
        self.headers = generate_UserAgent()
        self.pageNum = pageNum
        # 未登陆状态，只能page=1，否则会取不到内容
        # 登陆后可动态处理page
        self.url = "http://s.weibo.com/weibo/{}&b=1&page={}"
        self.isNormal = isNormal
    def __parse_page(self):
        print self.keyword,u'-----关键字是------'
        if self.isNormal == 1:
            try:
                # 获取cookies信息
                uid,cookies,count_num = zBackCookie()
                print u'获取成功－－－－－－'
                if count_num >= 500:
                    # 当做过期的cookie　清理掉，生成新的cookie
                    popExpCookie()
                    # 生成新的cookie
                    uid,cookies = zLoginGenCookie()
                    print u'删除旧的，获取新的'
            except Exception as e:
                # 获取cookie失败的情况下，直接请求页面
                print e,u'获取cookie失败'
                # 重新从账号redis 库中获取账号，生成cookie，再次获取cookie
                zLoginGenCookie()
                uid, cookies,count_num = zBackCookie()
                s = requests.session()
                s.cookies.update(cookies)
                res_obj = s.get(url=self.url.format(self.keyword, self.pageNum), headers=self.headers)
                # todo 添加邮件提醒机制
                # logger.info(e)
                # res_obj = requests.get(url=self.url.format(self.keyword, self.pageNum), headers=self.headers)
            else:
                # 没有发生异常的情况下，session请求网页
                s  = requests.session()
                s.cookies.update(cookies)
                # 让cookie计数＋１，
                print u'没有发生异常通道'
                try:
                    LoginInfo().update_cookies_count()
                except Exception as e:
                    print u'------更新ｃｏｏｋｉｅ的操作异常',e
                res_obj = s.get(url=self.url.format(self.keyword,self.pageNum),headers = self.headers)
                res_text = res_obj.text
                if str(uid) not  in res_text:
                    print u'uid 不再response中，cookie失效'
                    logger.info(u"cookie失效")
                    # 重新登陆获取cookie
                    popExpCookie()
                    zLoginGenCookie()
                    uid, cookies,count_num = zBackCookie()
                    s.cookies.update(cookies)
                    res_obj = s.get(url=self.url.format(self.keyword, self.pageNum), headers=self.headers)
                print u'开始判断是否机器人'
                if '\u5f02\u5e38' in res_text or '\u9a8c\u8bc1\u7801' in res_text:
                    print u'出现异常需要验证码'
                    logger.info(u'账号出现异常，被当作机器人了,需要输入验证码')
                    res_obj = requests.get(url = self.url.format(self.keyword,1),headers = self.headers)

        else:
            # 不登陆，直接发送请求，不携带cookie
            res_obj = requests.get(url = self.url.format(self.keyword,1),headers = self.headers)
        response = res_obj.text
        eres = etree.HTML(response)
        # 提取包含html内容的script标签内容
        content_in_script = eres.xpath('//script[last()-6]/text()')
        if content_in_script:
            # 获取到了json
            cont_json_str = re.search(r'.*?\.view\((.*?}).*', content_in_script[0]).group(1)
            # print cont_json_str
            dic_data = json.loads(cont_json_str)
            # 获取动态加载的网页代码 html
            str_html = dic_data['html']
            # etree 处理，后续使用xpath方法，获取节点信息 todo : important hint
            estr_html = etree.HTML(str_html)
            # 获取最后一页的页码：
            pageTotal = len(estr_html.xpath('//div[@class="layer_menu_list W_scroll"]/ul/li'))
            # 只取用户发的微博的节点 ：todo ：important hint
            feedback_items = estr_html.xpath('//div[contains(@class,"WB_cardwrap S_bg2 clearfix")]')
            # 循环便利取到的这些微博
            modelList = []
            for single_item  in feedback_items:
                # {"user_face_img":xxx,"user_nickname":xxx,"title_info":[xxx],"image_list":[xxx,xxx,xxx]}
                weibo_detail = dict()
                weibo_detail['user_face_img'] = single_item.xpath('.//div[@class="face"]/a/img/@src')[0] if single_item.xpath('.//div[@class="face"]/a/img/@src') else None
                try:
                    weibo_detail['user_nickname'] = single_item.xpath('.//div[@class="face"]/a/@title')[0]
                except Exception as e:
                    weibo_detail['user_nickname'] = single_item.xpath('.//a[@nick-name]/@nick-name')
                article_in_list = single_item.xpath('.//div[@class="feed_content wbcon"]//p//text()')
                weibo_detail['article_info'] = self.handle_article_list(article_in_list)
                weibo_detail['article_tag'] = re.findall(r"#(.+)#",weibo_detail['article_info'])
                weibo_detail['TailAndComeFrom'] = single_item.xpath('.//div[@class="feed_from W_textb"]//text()')
                temp_str = ''
                for parts in weibo_detail['TailAndComeFrom']:
                    temp_str+=parts
                weibo_detail['TailAndComeFrom'] = temp_str.strip()
                weibo_detail['moreContentHref'] = single_item.xpath('.//a[@class="WB_text_opt"]/@action-data') if\
                    len(single_item.xpath('.//a[@class="WB_text_opt"]'))>0 else None
                if weibo_detail['moreContentHref'] is not None:
                    temp_url =  weibo_detail['moreContentHref'][0]
                    weibo_detail['moreContentHref'] = urllib.quote(temp_url)
                else:
                    weibo_detail['moreContentHref'] = ''
                image_li = single_item.xpath('.//div[@class="media_box"]/ul/li')
                image_list = []
                if image_li:
                    # 提取li 下面的图片，判断后缀是否gif，否则跳过continue
                    for image in image_li:
                        image_href = image.xpath('.//img[1]/@src')[0]
                        image_href= self.handle_image_href(image_href)
                        image_list.append(image_href)
                weibo_detail['image_list'] = image_list
                if weibo_detail['user_nickname'] and weibo_detail['article_info']:
                    modelList.append(weibo_detail)
            return modelList,pageTotal
        else:
            # todo 应该是发生页面事故，发送邮件
            return [],0


    @staticmethod
    def handle_article_list(li):
        temp = ''
        for i in li:
            temp+=i
        return temp
    @staticmethod
    def handle_image_href(str_href):
        return re.sub(r'square|thumbnail','bmiddle',str_href)

    def get_all_info(self):
        # try:
        #     return self.__parse_page()
        # except Exception as e:
        #     print e
        #     logger.info(e)
        #     return [],0
        return self.__parse_page()


if __name__ == '__main__':
    s = Sina(keyword='韩寒发长文',isNormal= 1)
    a,b = s.get_all_info()
    print a
