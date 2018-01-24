# coding=utf-8
import random
from Queue import Queue
from threading import Thread

import requests
import time
from werkzeug.routing import BaseConverter
from user_agent import base
import urllib
from gevent import monkey
import gevent
monkey.patch_all()
class RegexConverter(BaseConverter):
    """在路由中使用正则表达式进行提取参数的转换工具"""
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]

def gen_md5(src):
    """
    这个函数的作用是用来做md5加密的
    :param src: 输入的需要加密的数据
    :return: 加密后的md5值
    """
    import hashlib
    m2 = hashlib.md5()
    m2.update(src)
    return m2.hexdigest()


def generate_UserAgent():
    # 这句话用于随机选择user-agent
    ua = base.generate_user_agent()
    if ua is not None:
        return {'User-Agent':ua}

def unquote_url(rawurl):
    # 实现url解码
    url=urllib.unquote(rawurl)
    return url

class Cleaner:
    def __init__(self,image_data):
        self.image_data = image_data
        self.clean_data = []
        self.que = Queue()
        self.spawn_list = []
        for item in image_data:
          self.que.put(item)
    def judge_url(self):

        while not  self.que.empty():
            item = self.que.get()
            pic_url = item.get("src")

            try:
                status_code = requests.head(url=pic_url,timeout=0.2).status_code
                assert  status_code == 200 or 302 or 301
            except Exception :
                # print pic_url
                return

            self.clean_data.append(item)
            time.sleep(0.1)

    def test_url_nornal(self,item):
        # item = self.que.get()
        pic_url = item.get('src')
        if not pic_url.endswith('gif') or 'media.giphy.com' in pic_url:
            return
        else:
            pass
        try:
            headers = requests.head(url=pic_url, timeout=0.6)
            status_code = headers.status_code
            assert status_code == 200
        except Exception as e:
            return
        else:

            self.clean_data.append(item)

    def task_use_thread(self):
        task_list = []
        for i in xrange(15):
            t = Thread(target=self.judge_url)
            task_list.append(t)
            t.start()

        for t in task_list:
            t.join()

    def task_(self):
        # task_list = []
        # for i in xrange(15):
        #     t = Thread(target=self.judge_url)
        #     task_list.append(t)
        #     t.start()
        #
        # for t in task_list:
        #     t.join()
        while not self.que.empty():
            item = self.que.get()
            self.spawn_list.append(gevent.spawn(self.test_url_nornal,item))

        gevent.joinall(self.spawn_list)



