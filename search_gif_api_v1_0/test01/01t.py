from copy import deepcopy

import requests
import threadpool
import time
from Queue import Queue

def clean_data(item,emp_li):
    print item
    # pic_url = eval(item).get('src')
    item = eval(item)
    pic_url = item.get('src')
    if requests.head(url=pic_url).status_code == 200 or 'media.giphy.com' not in pic_url:
        emp_li.append(item)
    else:
        pass


if __name__ == '__main__':
    emp_li = []
    a = [
      {
        "fromUrl": "http://tu.duowan.com/scroll/97660/6.html",
        "imgTitle": "\u5168\u7403<strong>\u641e\u7b11</strong>gif\u56fe\u7b2c1028\u5f39",
        "mainTag": "",
        "slaveTag": [],
        "src": "http://s1.dwstatic.com/group1/M00/00/26/bab0b13d80d388f62e8049325669b9ff.gif"
      },
      {
        "fromUrl": "http://yule.sohu.com/20041130/n223248132.shtml",
        "imgTitle": "[<strong>\u641e\u7b11</strong>]\u8d85\u7ea7\u641e\u7b11\u7684\u5341\u4e8c\u661f\u5ea7\u52a8\u6001\u56fe\u7247",
        "mainTag": "",
        "slaveTag": [],
        "src": "http://photo.sohu.com/20041130/Img223248101.gif"
      },
      {
        "fromUrl": "http://pcedu.pconline.com.cn/552/5528616.html",
        "imgTitle": "<strong>\u641e\u7b11</strong>\u8868\u60c5\u52a8\u6001_\u804a\u5929\u52a8\u6001\u641e\u7b11\u8868\u60c5",
        "mainTag": "",
        "slaveTag": [],
        "src": "http://img0.pconline.com.cn/pconline/1410/06/5528616_4604458_2012111814561107551_thumb1_thumb.gif"
      },
      {
        "fromUrl": "http://www.duitang.com/blog/?id=668378326",
        "imgTitle": "\u7eaf\u6587\u5b57\u9017\u903c \u9b54\u6027 <strong>\u641e\u7b11</strong> \u8da3\u5473\u8868\u60c5 \u6597\u56fe \u6076\u641e \u8d31\u840c \u66b4\u8d70 \u52a8\u6f2b\u8868\u60c5 \u8868\u60c5",
        "mainTag": "",
        "slaveTag": [],
        "src": "http://img4.duitang.com/uploads/item/201611/15/20161115204518_tmdWK.gif"
      },
      {
        "fromUrl": "http://www.hugao8.com/63714/",
        "imgTitle": "\u3010<strong>\u641e\u7b11</strong>gif\u3011\u5c0f\u4f19\u5b50\u5728\u5395\u6240\u8fd9\u4e48\u73a9\u4e5f\u662f\u8d31\u9014\u65e0\u91cf\u554a!",
        "mainTag": "",
        "slaveTag": [],
        "src": "http://ww1.sinaimg.cn/bmiddle/005vzZU3jw1emxw3v37hwg30b4069hdt.gif"
      },
      {
        "fromUrl": "http://m.zol.com.cn/article/3146608.html?via=index",
        "imgTitle": "rdoko\u571f\u8c46\u4ed4<strong>\u641e\u7b11</strong>qq\u8868\u60c5\u56fe\u7247",
        "mainTag": "",
        "slaveTag": [],
        "src": "http://2b.zol-img.com.cn/product/94_501x2000/277/ceeAqz56AnCW2.gif"
      },
      {
        "fromUrl": "http://m.zol.com.cn/article/584983.html?j=simple",
        "imgTitle": "\u8d85<strong>\u641e\u7b11</strong>qq\u8868\u60c5\u4e09",
        "mainTag": "",
        "slaveTag": [],
        "src": "http://img2.zol.com.cn/product/12_501x2000/655/ceq7vHVEoo8Gs.gif"
      }
    ]
    rest_item = []
    start_time = time.time()
    pool = threadpool.ThreadPool(100)
    i = 1
    for item in a:

        print '------%d'%i
        i+=1
        reqs = threadpool.makeRequests(clean_data,[([str(item),emp_li],None)])
        [pool.putRequest(req) for req in reqs]
    pool.wait()
    print emp_li
    print len(emp_li)
    print '%d second' % (time.time() - start_time)
