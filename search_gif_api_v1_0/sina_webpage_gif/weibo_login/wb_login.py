#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import binascii
import cookielib
import json
import os
import random
import re
import time
import urllib
import urllib2
import requests
import rsa
from bs4 import BeautifulSoup
from base.tools import generate_UserAgent
from sina_webpage_gif.redis_db import *

wb_client = 'ssologin.js(v1.4.18)'

user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
]


# 获取加密的用户
def encrypt_usr(username):
    """
    对帐号加密
    :param username: 帐号
    :return: su值
    """
    # su:base64加密过后的用户名
    # return base64.b64encode(urllib.quote_plus(str(username)).encode('utf-8')).decode('utf-8')
    return base64.encodestring(urllib.quote(username))[:-1]  # html字符转义并经base64加密


# 获取加密的密码
def encrypt_pwd(password, servertime, nonce, pubkey):
    """
    对密码加密，http://login.sina.com.cn/js/sso/ssologin.js中makeRequest的python实现
    :param password: 密码
    :param servertime: 预登录变量servertime
    :param nonce: 预登录变量nonce
    :param pubkey: 预登录变量pubkey
    :return:sp值
    """
    # 十六进制10001转成十进制为65537
    key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))  # 创建公钥
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文js加密文件中得到
    pwd = rsa.encrypt(message.encode('utf-8'), key)  # 加密
    return binascii.b2a_hex(pwd)  # 将加密信息转换为16进制


# 获取需要提交的表单数据
def get_form_data(username, password, servertime, nonce, pubkey, rsakv):
    """

    :param username: 帐号
    :param password: 密码
    :param servertime: 预登录变量servertime
    :param nonce: 预登录变量nonce
    :param pubkey: 预登录变量pubkey
    :param rsakv: 预登录变量rsakv
    :return: post参数
    """
    usr = encrypt_usr(username)
    pwd = encrypt_pwd(password, servertime, nonce, pubkey)
    form_data = {
        'encoding': 'UTF-8',
        'entry': 'weibo',
        'from': '',
        'gateway': '1',
        'nonce': nonce,
        'pagerefer': '',
        'prelt': '115',
        'pwencode': 'rsa2',
        'returntype': 'META',
        'rsakv': rsakv,
        'savestate': '7',
        'servertime': servertime,
        'service': 'miniblog',
        'sp': pwd,
        'sr': '1366*768',
        'su': usr,
        'useticket': '1',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'vsnf': '1'
    }
    return form_data


# 登陆函数
def login(username, password):
    print username,password
    # 声明CookieJar对象实例，保存cookie，之后写入文件
    # 关系：CookieJar —-派生—->FileCookieJar  —-派生—–>MozillaCookieJar和LWPCookieJar
    cookie_jar = cookielib.MozillaCookieJar()
    # 创建cookie处理器，绑定CookieJar对象实例
    cookie_handler = urllib2.HTTPCookieProcessor(cookie_jar)
    # 构建opener，通过cookie处理器handler与CookieJar对象绑定，另设置一个handler用于处理http的URL的打开
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPHandler)
    # 安装opener,此后调用urlopen()时都会使用安装过的opener对象
    urllib2.install_opener(opener)

    # ******预登录******
    pre_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo'
    pre_url += '&callback=sinaSSOController.preloginCallBack'
    pre_url += '&su=' + encrypt_usr(username) + '&rsakt=mod&checkpin=1'
    pre_url += '&client=' + wb_client + '&_=' + str(int(round(time.time() * 1000)))
    data = urllib2.urlopen(pre_url).read()
    try:
        json_data = re.search(pattern=r'({.*?})', string=data).group(1)
        dict_data = json.loads(json_data)
        servertime, nonce = unicode(dict_data['servertime']), dict_data['nonce']
        pubkey, rsakv = dict_data['pubkey'], dict_data['rsakv']
    except Exception as e:
        print str(e)
        print 'Get server data error!'
        return None

    # ******登录******
    req = urllib2.Request(
        url='http://login.sina.com.cn/sso/login.php?client=' + wb_client,
        data=urllib.urlencode(get_form_data(username, password, servertime, nonce, pubkey, rsakv)),
        headers={'User-Agent': random.choice(user_agent_list)}
    )
    data = urllib2.urlopen(req).read()
    try:
        # print type(data), data
        # 这边有一个重定位网址，包含在脚本中，获取到之后才能真正地登陆
        login_url = re.search(pattern=r'location\.replace\([\'"](.*?)[\'"]', string=data).group(1)
        print login_url
    except Exception as e:
        print str(e)
        print 'Login error!'
        return None,None

    # ******跳转******
    data = urllib2.urlopen(login_url).read()  # 由于之前的绑定，cookies信息会直接写入
    soup = BeautifulSoup(data, 'html.parser')  # 403异常判断
    if soup.title and (u'访问受限' in soup.title.text or u'解冻' in soup.title.text):
        print 'Account has been frozen! %s' % username
        return None,None
    try:
        json_data = re.search(pattern=r'\((\{.*?\})\)', string=data).group(1)  # r'"uniqueid":"(.*)",'
        login_info = json.loads(json_data)
        unique_id = login_info['userinfo']['uniqueid']
        print 'Login success! unique id:%s account:%s' % (unique_id, username)
    except Exception as e:
        print str(e)
        print 'Location error!'
        return None,None

    # 设置保存cookie的文件
    # os.path.abspath(os.curdir)
    # os.path.split(os.path.realpath(sys.argv[0]))[0]
    file_name = os.path.join(os.path.dirname(__file__), 'wb_cookies_%s.txt' % unique_id)
    # 保存cookie到文件
    # ignore_discard的意思是即使cookies将被丢弃也将它保存下来
    # ignore_expires的意思是如果在该文件中cookies已经存在，则覆盖原文件写入
    cookie_jar.save(filename=file_name, ignore_discard=True, ignore_expires=True)

    return unique_id, {item.name: item.value for item in cookie_jar}
    pass

def zLoginGenCookie():
    # 利用账号密码生成ｃｏｏｋｉｅ，不要重复登陆，只有在zzcCheck_login不起作用的时候才被调用
    userNpass = UserPass()
    tupleU_P = userNpass.getUserNpasswd()
    username = tupleU_P[0]
    password = tupleU_P[1]
    res = login(str(username),str(password))
    if res != (None,None):
        LoginInfo().saveCookieNuid(res[0],res[1])
    return res[0],res[1]

def popExpCookie():
    LoginInfo().deleteCookieNuid()

def zBackCookie():
    # 获取最后一个ｃｏｏｋｉｅ,
    uidNcookies = LoginInfo().getCookieNuid()
    uid = uidNcookies[0]
    cookies = eval(uidNcookies[1])
    count_num = uidNcookies[2]
    return uid,cookies,count_num

def check_login():
    """
    就是检验ｕｉｄ是否在相应里面
    :return:
    """
    dir_path = os.path.dirname(__file__)
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):
            match = re.match(pattern=r'wb_cookies_(\w+?)\.txt', string=file_name)
            if match:
                unique_id = match.group(1)
                # 创建一个MozillaCookieJar对象
                cookie = cookielib.MozillaCookieJar()
                # 从文件中的读取cookie内容到变量
                cookie.load(file_path, ignore_discard=True, ignore_expires=True)
                # 利用获取到的cookie创建一个opener
                handler = urllib2.HTTPCookieProcessor(cookie)
                opener = urllib2.build_opener(handler)
                res = opener.open('http://weibo.com/')
                data = res.read()
                if "'uid'" in data:
                    print 'Login success by history! unique id:%s' % unique_id
                    return unique_id, {item.name: item.value for item in cookie}

                else:
                    return None,None
                    # print 'This cookies is expired.Please re-login!'



# 登陆函数
def login2(username, password):
    session = requests.session()
    session.headers['User-Agent'] = random.choice(user_agent_list)

    # ******预登录******
    pre_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo'
    pre_url += '&callback=sinaSSOController.preloginCallBack'
    pre_url += '&su=' + encrypt_usr(username) + '&rsakt=mod&checkpin=1'
    pre_url += '&client=' + wb_client + '&_=' + str(int(round(time.time() * 1000)))
    data = session.get(pre_url).text
    try:
        # print type(data), data
        json_data = re.search(pattern=r'({.*?})', string=data).group(1)
        dict_data = json.loads(json_data)
        servertime, nonce = unicode(dict_data['servertime']), dict_data['nonce']
        pubkey, rsakv = dict_data['pubkey'], dict_data['rsakv']
    except Exception as e:
        print str(e)
        print 'Get server data error!'
        return None, None

    # ******登录******
    data = session.post(url='http://login.sina.com.cn/sso/login.php?client=' + wb_client,
                        data=get_form_data(username, password, servertime, nonce, pubkey, rsakv)).content.decode('GBK')
    try:
        # print type(data), data
        # 这边有一个重定位网址，包含在脚本中，获取到之后才能真正地登陆
        login_url = re.search(pattern=r'location\.replace\([\'"](.*?)[\'"]', string=data).group(1)
        print login_url
    except Exception as e:
        print str(e)
        print 'Login error!'
        return None, None

    # ******跳转******
    data = session.get(login_url).content.decode('gb2312')
    soup = BeautifulSoup(data, 'html.parser')  # 403异常判断
    if soup.title and (u'访问受限' in soup.title.text or u'解冻' in soup.title.text):
        print 'Account has been frozen! %s' % username
        return None, None
    try:
        # print type(data), data
        unique_id = re.search(pattern=r'"uniqueid":"(.*)",', string=data).group(1)
        print 'Login success! unique id:%s account:%s' % (unique_id, username)
        return unique_id, session.cookies.get_dict()
    except Exception as e:
        print str(e)
        print 'Location error!'
        return None, None
    pass


if __name__ == '__main__':

    # ua = 'sdulsj@sina.com'
    # print base64.b64encode(urllib.quote_plus(str(ua)).encode('utf-8')).decode('utf-8')
    # print encrypt_usr(ua)
    # print get_server_data(ua)
    # print login('13240323601', 'ztc6550052')
    # check_login()
    # print(login('18864932834','ZHao1990625'))
    # zzcLogin()
    print zBackCookie()