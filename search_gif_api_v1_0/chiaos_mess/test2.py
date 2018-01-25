# coding=utf-8
import time
import requests
from threading import Thread
from Queue import Queue
class Cleaner:
    def __init__(self,image_data):
        self.image_data = image_data
        self.clean_data = []
        self.que = Queue()
        for item in image_data:
          self.que.put(item)
    def judge_url(self):

        while not  self.que.empty():
            item = self.que.get()
            pic_url = item.get("picUrl")

            try:
                status_code = requests.head(url=pic_url).status_code
                print status_code,'--------'
                assert  status_code == 200
            except Exception :
                # print pic_url
                return

            self.clean_data.append(item)
            time.sleep(0.1)

    def task_(self):
        task_list = []
        for i in xrange(15):
            t = Thread(target=self.judge_url)
            task_list.append(t)
            t.start()

        for t in task_list:
            t.join()

if __name__ == '__main__':

    a = [
        {
            "fromUrl": "http://dy.163.com/article/T1374479210225/9V81NQ6A00964KHQ.html",
            "imgTitle": "\u4e16\u754c\u676f\u745e\u58ebvs\u6cd5\u56fd\u76f4\u64adgif \u5409\u9c81\u52a9\u653b\u74e6\u5c14\u5e03\u57c3\u90a3<strong>\u5f97\u5206</strong>",
            "mainTag": "",
            "picUrl": "http://easyread.ph.126.net/NbRK9u9hyOZ6mOWhxWJ9pg==/7806649105442203293.gif",
            "slaveTag": []
        },
        {
            "fromUrl": "http://sports.qq.com/a/20170608/017101.htm?qqcom_pgv_from=aio",
            "imgTitle": "\u5206\u6790\u5e08:\u4e2d\u950b\u63a9\u62a4\u524d\u63d2<strong>\u5f97\u5206</strong> \u540e\u8170\u4f4d\u7f6e\u611f\u5f31\u8c03\u5ea6\u5dee",
            "mainTag": "",
            "picUrl": "http://mat1.gtimg.com/sports/2022yl/gif/10hbwsw.gif",
            "slaveTag": []
        },
        {
            "fromUrl": "http://www.aiyuke.com/view-8058.html",
            "imgTitle": "(\u7ea2\u8863\u5973\u540a\u7403 \u6740\u7403 \u642d\u6863\u5c01\u7f51<strong>\u5f97\u5206</strong>)",
            "mainTag": "",
            "picUrl": "http://img2.aiyuke.com/upload/2017/05/15/17051516440694249.gif",
            "slaveTag": []
        },
        {
            "fromUrl": "http://www.yinhang123.net/zixun/yulenews/2016/0821/228902.html",
            "imgTitle": "\u4e2d\u56fd\u961f\u4e00\u4f20\u76f4\u63a5<strong>\u5f97\u5206</strong>!",
            "mainTag": "",
            "picUrl": "http://p6.qhimg.com/dmfd/__90/t012313bdbff4b45999.gif?size=439x213",
            "slaveTag": []
        },
        {
            "fromUrl": "http://www.aiyuke.com/view-7868.html",
            "imgTitle": "(\u9ed1\u8863\u63a7\u7f51 \u5f3a\u653b\u76f4\u7ebf<strong>\u5f97\u5206</strong>)",
            "mainTag": "",
            "picUrl": "http://img2.aiyuke.com/upload/2017/04/14/1521537299.gif",
            "slaveTag": []
        },
        {
            "fromUrl": "http://m.sohu.com/n/484268841/?mv=3&partner=nokiaelle",
            "imgTitle": "\u6bd4\u5982,\u53d1\u5e73\u7403,\u7528\u6ed1\u677f\u540a\u5bf9\u65b9\u7f51\u524d<strong>\u5f97\u5206</strong>.",
            "mainTag": "",
            "picUrl": "http://s9.rr.itc.cn/r/wapChange/20173_22_18/a2usur2442743987542.gif",
            "slaveTag": []
        },
        {
            "fromUrl": "http://sports.qq.com/a/20160731/022328.htm?qqcom_pgv_from=aio",
            "imgTitle": "gif-\u5e03\u9c81\u8bfa\u95e8\u524d\u626b\u5c04<strong>\u5f97\u5206</strong> \u83ab\u96f7\u7f57\u6413\u5c04\u518d\u4e0b\u4e00\u57ce",
            "mainTag": "",
            "picUrl": "http://mat1.gtimg.com/sports/qiuzhenmei/20160731yataijinqiu2.gif",
            "slaveTag": []
        },
        {
            "fromUrl": "http://sports.sina.com.cn/l/2016-03-10/doc-ifxqhmvc2239186.shtml",
            "imgTitle": "\u4f0a\u5e03\u7834\u95e8<strong>\u5f97\u5206</strong>",
            "mainTag": "",
            "picUrl": "http://n.sinaimg.cn/sports/transform/20160310/gp4n-fxqhmvc2236663.gif",
            "slaveTag": []
        },
        {
            "fromUrl": "http://www.sanqin.com/2017/0306/283508.shtml",
            "imgTitle": "\u52a0\u6bd4\u4e9a\u8fea\u5c3c\u7684\u5723\u5f92\u9996\u79c0,\u53cd\u51fb\u4e2d\u6740\u5165\u7981\u533a\u5de6\u811a\u7206\u5c04<strong>\u5f97\u5206</strong>.",
            "mainTag": "",
            "picUrl": "http://upload.sanqin.com/2017/0306/1488732584940.gif",
            "slaveTag": []
        },
        {
            "fromUrl": "http://www.sohu.com/a/111154255_362124",
            "imgTitle": "\u96be\u5ea6\u7cfb\u65703.2,<strong>\u5f97\u5206</strong>91.20,\u7d2f\u8ba1\u5206\u6570439.25\u5206,\u6392\u540d\u7b2c\u4e00",
            "mainTag": "",
            "picUrl": "http://n1.itc.cn/img8/wb/recom/2016/08/19/147156236900695197.GIF",
            "slaveTag": []
        }
    ]
    print len(a)
    cc = Cleaner(a)
    cc.task_()
    print len(cc.clean_data)
    print cc.clean_data


