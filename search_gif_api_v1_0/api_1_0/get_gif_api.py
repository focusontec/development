# coding=utf-8
import time
from base import logger
from flask import request, jsonify
from naver.get_naver_gif import NaverGif
from sina_webpage_gif.show_more_article import get_complete_cont
from yahoo.get_yahoo_gif import Yahoo_gif
from baidu_img.get_url import BaiduImgGifApi
from sougou_img.get_gif_urls import SougouGIfApi
from sina_webpage_gif.get_webpage_gif import Sina
from . import api
import urllib
@api.route('/gif/searchByQuery/<string:searchBy>',methods = ["GET"])
def get_gif_img(searchBy):
    headers = request.headers
    key_word = request.args.get('query','nba')
    # 页码
    pnNum = request.args.get('pageIndex','0')
    # 默认每页返回30 条
    pageSize = request.args.get('pageSize','20')
    # 校验参数完整性
    type = request.args.get("type","all")
    print request.headers
    if not key_word:
        response = jsonify(status='-1',message=u"参数缺失",data="false")
        response.headers['Access-Control-Allow-Origin'] = "*"
        response.headers['Access-Control-Allow-Credentials'] = "true"
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        response.headers['Host'] = "secret"
        return response

    # 校验参数的正确性
    try:
        a = [int(pageSize),int(pnNum)]
    except Exception as e:
        print e
        response =  jsonify(status='-1', message=u"参数错误", data="false")
        response.headers['Access-Control-Allow-Origin'] = "http://mp.alphagif.com"
        response.headers['Access-Control-Allow-Credentials'] = "true"
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        response.headers['Host'] = "secret"
        return response


    if (searchBy not in ["baidu","sougou","yahoo","weibo","naver"]):

        response = jsonify(status='-1', message=u"搜索引擎选择错误", data="false")
        response.headers[u'Access-Control-Allow-Origin'] = u"http://mp.alphagif.com"
        response.headers[u'Access-Control-Allow-Credentials'] = u"true"
        response.headers[u'Access-Control-Allow-Methods'] = u'GET,POST'
        response.headers[u'Access-Control-Allow-Headers'] = u'x-requested-with,content-type'
        response.headers[u'Host'] = "secret"
        return response
    else:
        if searchBy == 'baidu':
            # 1,实现百度搜索的业务
            # 百度每页上限60条,如果大于60 按照60传递
            if int(pageSize) > 60:
                pageSize = 60
            else:
                pageSize = pageSize
            time_start_baidu = time.time()
            image_data,total_img_num = BaiduImgGifApi(key_word,pnNum,pageSize).parse()
            time_end_baidu = time.time()
            logger.info("百度搜索一个页面耗时" + str(time_end_baidu - time_start_baidu) + "搜索关键词为:%s"%key_word)
            # 2. 解析response ,提取　图片url
            # 3. 组装数据
            if total_img_num is not None:

                pageTotal = int(total_img_num)//int(pageSize)

            else:
                pageTotal = 0
            # print image_data
            response = jsonify(status=0, message='ok',
                           data={"modelList": image_data, "pageCount": pageTotal, "pageIndex": int(pnNum)})
        elif searchBy == 'sougou':
            # 实现搜狗搜图的业务
            # 搜狗默认每页48条数据，暂时没有找到更改条目的方法
            # 获取的pagesize并没有用。
            time_start_sougou = time.time()
            image_data , total_images= SougouGIfApi(pageNum=pnNum,keyword=key_word).parse_gif()
            time_end_sougou = time.time()
            logger.info(u"搜狗搜索一个页面耗时" + str(time_end_sougou - time_start_sougou) + "搜索关键词为:%s"%key_word)
            if total_images is not None:
                pageTotal = int(total_images)//48
            else:
                pageTotal = 0
            if int(pnNum) > pageTotal:
                pnNum = pageTotal
            response = jsonify(status=0,message = 'ok',data = {"modelList":image_data,"pageCount":pageTotal,"pageIndex":int(pnNum)})
            response.headers['Access-Control-Allow-Origin'] = "http://mp.alphagif.com"
            response.headers['Access-Control-Allow-Credentials'] = "true"
            response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
            return response
        elif searchBy == 'weibo':
            # 此处默认是第一页，如果登陆后可以查看更多页,否则会没有内容
            if type == "all":
                pass
            elif type == 'tag':
                key_word = '#{}#'.format(key_word)
                key_word = urllib.quote(key_word)
            pnNumTemp = int(pnNum)+1
            isNormal = 1
            try:
                time_start_weibo = time.time()
                modelList,pageTotal = Sina(keyword= key_word,pageNum= str(pnNumTemp),isNormal=isNormal).get_all_info()
                time_end_weibo = time.time()
                logger.info(u"微博搜索一个页面耗时" + str(time_end_weibo - time_start_weibo) + u"搜索关键词为:%s" % key_word)
                while modelList == [] and pnNumTemp < pageTotal:
                    time.sleep(0.1)
                    pnNumTemp +=1
                    modelList,pageTotal = Sina(keyword=key_word,pageNum=pnNumTemp,isNormal=isNormal).get_all_info()
            except Exception as e :
                print e,'-------get_gif_api'
                isNormal = -1
                modelList, pageTotal = Sina(keyword=key_word, pageNum=pnNumTemp,isNormal=isNormal).get_all_info()
                # print modelList, pageTotal

            response = jsonify(status=0, message='ok',
                           data={"modelList": modelList, "itemCount": len(modelList), "pageIndex": pnNumTemp - 1,
                                 'pageTotal': int(pageTotal) - 1}, isNormal=isNormal)

        elif searchBy == 'yahoo':
            time_start_yahoo = time.time()
            image_data,total_images = Yahoo_gif(keyword=key_word,startNum=int(pnNum)*60+1).get_yahoo_gif()
            time_end_yahoo = time.time()
            logger.info("yahoo搜索一个页面耗时" + str(time_end_yahoo - time_start_yahoo) + "搜索关键词为:%s"%key_word)
            if total_images:
                pageTotal = int(total_images) // 60
            else:
                pageTotal = 0
            if int(pnNum) > pageTotal:
                pnNum = pageTotal
            response = jsonify(status = 0,message = 'ok',data = {'modelList':image_data,'pageCount':pageTotal,'pageIndex':pnNum})

        elif searchBy == 'naver':
            # 输出符合要求的gif动图，数量小于 pagesize的数量
            temp_tuple = NaverGif(keyword= key_word,eachPageItemNum= pageSize,pnNum=pnNum,start= int(pageSize)*int(pnNum)+1).parse_res()
            if temp_tuple:
                image_data, total_images = temp_tuple
            else:
                response = jsonify(status = 0,message = "ok",data = {"modelList":[],'pageCount':0,'pageIndex':pnNum})
                response.headers['Access-Control-Allow-Origin'] = "http://mp.alphagif.com"
                response.headers['Access-Control-Allow-Credentials'] = "true"
                response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
                response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
                return response
            if image_data is not None:
                pageTotal = int(total_images)//int(pageSize)
                # print pageTotal,pageSize,pnNum
                if int(pnNum) > pageTotal:
                    response = jsonify(status = 0,message = "ok",data = {'modelList':[],'pageCount':pageTotal,'pageIndex':pnNum})

                else:
                    response = jsonify(status=0, message="ok",
                               data={'modelList': image_data, 'pageCount': pageTotal, 'pageIndex': pnNum})
            else:
                response = jsonify(status = 0,message = "ok",data = {"modelList":[],'pageCount':0,'pageIndex':pnNum})

        response.headers['Access-Control-Allow-Origin'] = "http://mp.alphagif.com"
        response.headers['Access-Control-Allow-Credentials'] = "true"
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        response.headers['Host'] = "secret"

        return response

@api.route('/gif/searchByQuery/weibo/ShowMore/<moreUrl>')
def getMoreArticle(moreUrl):
    html_content =  get_complete_cont(moreUrl)
    return jsonify(html = html_content)