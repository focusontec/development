# coding=utf-8
import json
import requests
import urllib
test_url = "http://s.weibo.com/ajax/direct/morethan140?mid=4183488066293845&search=gif&absstr=gif&current_uid=3173633817&current_mid=4183488066293845"
def get_complete_cont(url):
    # url加密
    uncoded_url = urllib.unquote(url)
    completeUrl = "http://s.weibo.com/ajax/direct/morethan140?"+uncoded_url
    # 发送
    #　处理
    res_json = requests.get(completeUrl).content
    # print res_json
    dict_res = json.loads(res_json)
    data_cont  = dict_res.get('data')
    html_cont = data_cont.get('html')

    return html_cont


if __name__ == '__main__':
    print get_complete_cont(url=test_url)