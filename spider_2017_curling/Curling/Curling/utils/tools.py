#!/bin/python2
# coding=utf-8
"""
这个脚本里面存放的是一些公共的类
"""

import hashlib
import random
import time
import datetime
import uuid
import pytz
import re
import logging as log


def get_yesterday():
    """
    获取当前日期的昨天日期
    :return: 返回昨天的日期
    """
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = (today - oneday).strftime('%Y-%m-%d')
    return yesterday


def get_yesterday_data():
    """
    获取当前日期的昨天日期
    :return: 返回昨天的日期
    """
    return (datetime.date.today() - datetime.timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')


def get_date_day(old, days):
    """
    时间加上一定的月份
    :param old:
    :return:
    """
    return (old + datetime.timedelta(days=days)).strftime('%Y-%m-%d')


def get_today():
    """这个函数的作用是返回当前的时间"""
    today = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return today


def get_today_ymd():
    """
    这个函数的作用是返回当前的时间
    :return:
    """
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    return today


def get_tomorrow_ymd():
    """
    这个函数的作用是返回明天的时间
    :return:
    """
    import datetime
    i = datetime.datetime.now() + datetime.timedelta(days=1)
    return i.strftime('%Y-%m-%d')


def get_yesterday_ymd():
    """
    这个函数的作用是返回昨天的时间
    :return:
    """
    import datetime
    i = datetime.datetime.now() + datetime.timedelta(days=-1)
    return i.strftime('%Y-%m-%d')


def timestamp_to_time(timestamp_str=None):
    """
    时间戳转时间字符串
    注意：这里转换的是一个毫秒的时间戳
    :param timestamp_str:
    :return:
    """
    if timestamp_str is None:
        return None
    else:
        timestamp_str = float(timestamp_str) / 1000
        x = time.localtime(timestamp_str)
        tt_s = time.strftime('%Y-%m-%d %H:%M:%S', x)
        return tt_s


def gen_md5(src):
    """
    这个函数的作用是用来做md5加密的
    :param src: 输入的需要加密的数据
    :return: 加密后的md5值
    """
    m2 = hashlib.md5()
    m2.update(src)
    return m2.hexdigest()


def get_next_month():
    """
    这个函数是用来获取下个月的年份与月份
    :return: 返回的是下个月的年份与月份
    """
    import datetime
    i = datetime.datetime.now() + datetime.timedelta(days=31)
    i_year = int(i.year)
    i_month = i.month
    return "{}-{}".format(i_year, i_month)


def get_now_month():
    """
    这个函数是用来获取下个月的年份与月份
    :return: 返回的是下个月的年份与月份
    """
    import datetime
    i = datetime.datetime.now()
    i_year = int(i.year)
    i_month = i.month
    return "{}-{}".format(i_year, i_month)


def get_year_month():
    """
    这个函数是用来获取下个月的年份与月份
    :return: 返回的是下个月的年份与月份
    """
    import datetime
    i = datetime.datetime.now() + datetime.timedelta(days=31)
    i_year = int(i.year) + 1
    i_month = i.month
    return "{}-{}".format(i_year, i_month)


def get_last_4_month():
    """
    这个函数是用来获取最近4个月
    :return: 返回的是最近4个月的年份与月份
    """
    import datetime
    start_date = datetime.datetime.now() - datetime.timedelta(days=27)
    year = start_date.year
    time_arr = []
    for i in range(4):
        month = start_date.month + i
        if int(month) > 12:
            year = int(start_date.year) + 1
            month = int(month) - 12
        time_arr.append("{}-{}".format(year, month))

    time_arr = filter(lambda x: x if int(unicode(x).split('-')[1]) <= 12 else False, time_arr)
    # 或者
    # time_arr = map(lambda x, y: "{}-{}".format(x.year, x.month + y), [(now_date, i) for i in range(3)])
    return time_arr


def get_now_year_month():
    """
    这个函数是用来获取现在的年份与月份
    :return: 返回的是获取现在的年份与月份
    """
    import datetime
    i = datetime.datetime.now()
    i_year = int(i.year)
    i_month = i.month
    return "{}-{}".format(i_year, i_month)


def utc_to_cn(utc):
    """
    :param utc:
    :return:
    """
    utc_format = "%Y-%m-%dT%H:%M:%SZ"
    try:
        n_data = datetime.datetime.strptime(utc, utc_format) + datetime.timedelta(hours=8)
        return n_data.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        log.error(e.message)
        return None


def str_to_date(in_str):
    """
    把字符串转换为时间
    字符串格式：年-月-日
    :param in_str: 年-月-日
    :return:
    """
    t = time.strptime(in_str, "%Y-%m-%d %H:%M:%S")
    y, m, d, h, M, s = t[0:6]
    return datetime.datetime(y, m, d, h, M, s)


def str_to_data_ymd(input_str=None):
    """
    把字符串转换为时间
    字符串格式：年-月-日
    :param input_str: 年-月-日
    :return:
    """
    input_str = input_str if bool(input_str) else get_today_ymd()
    if len(input_str) > 10:
        t = time.strptime(input_str, "%Y-%m-%d %H:%M:%S")
    else:
        t = time.strptime(input_str, "%Y-%m-%d")
    y, m, d = t[0:3]
    return datetime.datetime(y, m, d)


def range_num():
    """
    这个函数的作用是生成一个随机数
    :return:
    """
    return random.randint(0, 9999999999)


def not_list_rang_num(num_list):
    """
    返回一个不在目标数组中的数值
    :param num_list: 目标数组
    :return: 返回的数值
    """
    num = range_num()
    if num in num_list:
        return not_list_rang_num(num_list)
    else:
        return num


def return_uuid():
    """
    这个函数是用来返回uuid
    :return:
    """
    return uuid.uuid1()


def new_york_to_shanghai(utc_time_str):
    """纽约时间转为中国时间
    """
    result = ""
    tzc = pytz.timezone('Asia/Shanghai')
    tze = pytz.timezone('America/New_York')
    if utc_time_str:
        from datetime import datetime
        str_d = datetime.strptime(utc_time_str, "%Y-%m-%d %H:%M:%S")
        datetime_e = tze.localize(str_d)
        datetime_c = datetime_e.astimezone(tzc)
        result = datetime_c.strftime("%Y-%m-%d %H:%M:%S")
    return result


def handel_re(match, data, num=0, all_column=False):
    """这个函数是用来处理正则表达式"""
    rd = None
    try:
        rd = re.findall(match, data)
    except Exception as e:
        print e.message

    if rd:
        pass
    else:
        return

    if len(rd) > num:
        return unicode(rd[num]).strip()
    elif len(rd) > 0:
        if all_column:
            return rd
    else:
        return


def handel_arr_re(match, data, arr_num=0, num=0):
    """
    这个函数是用来处理正则表达式
    :param match: 正则
    :param data: 数据
    :param arr_num: 要获取的数组的位置
    :param num: 位置,默认为0
    :return:
    """
    if len(data) > arr_num:
        rd = re.findall(match, data[arr_num])
        if len(rd) > num:
            return rd[num]
        else:
            return None
    else:
        return None


def get_arr(arr, num=0):
    """
    这个函数是用来返回数组中的数值，如果不存在，那就返回 None
    :param arr: 数组
    :param num: 数组索引位置
    :return:
    """
    if num >= len(arr):
        return None
    else:
        return unicode(arr[num]).strip()


def replace_w(data):
    rd = re.findall('\(\w+\)', data)
    if len(rd) > 0:
        rep = unicode(rd[0])
        return unicode(data).replace(rep, '').strip()
    else:
        return unicode(data)


def get_24_date_seconds():
    """这个函数是判断当前时间到 24 点的小时
    """
    import datetime
    tomorrow_date = str_to_date_2(get_date_day(datetime.datetime.now(), 1))
    t = tomorrow_date - datetime.datetime.now()
    return int(t.seconds)


def str_to_date_2(in_str):
    """
    把字符串转换为时间
    字符串格式：年-月-日
    :param in_str: 年-月-日
    :return:
    """
    t = time.strptime(in_str, "%Y-%m-%d")
    y, m, d, h, M, s = t[0:6]
    return datetime.datetime(y, m, d, h, M, s)


def complete_data(input_data):
    """返回一个完整的日期

    :param input_data: 输入的时间
    Example: '10月28日 ,  周六'

    :return: 返回一个处理后的完整时间
    Example:
    input : '10月28日 ,  周六'
    return : 2017-10-28

    设计思路：
    （1）获取最近 180 天，共 360 天的日期与星期，之后，组成一个以日期与星期为key的字典
    >>> print date_dict
    >>> {'02-18 Sunday': '2018-02-18', '01-17 Wednesday': '2018-01-17',....}

    （2）解析输入的字符串

    （3）返回第（1）步处理好的字典中的日期

    注意：超过360天就匹配不了了，也就是距离当前时间 180 天内的
    """
    # 获取最近的 300 天
    date_dict = dict()
    for x in xrange(-180, 180):
        k = (datetime.datetime.now() + datetime.timedelta(days=x)).strftime('%m-%d %A')
        v = (datetime.datetime.now() + datetime.timedelta(days=x)).strftime('%Y-%m-%d')
        date_dict[k] = v

    week_name = {
        u"周一": "Monday",
        u"周二": "Tuesday",
        u"周三": "Wednesday",
        u"周四": "Thursday",
        u"周五": "Friday",
        u"周六": "Saturday",
        u"周日": "Sunday",
    }
    input_data = unicode(input_data).replace('\r', '').replace('\n', '').replace('\t', '').strip()
    return date_dict.get("{} {}".format(
        '-'.join(re.findall(u'(\w+)月(\w+)日', input_data)[0]).strip(),
        week_name.get(re.findall(u'(周.+)', input_data)[0].strip())
    ))


# 一个函数，取出数组中的指定数值
get_items = lambda arr_list, sp_list: list(map(lambda x: unicode(arr_list[x]).strip(), sp_list))

# 一些切割的 xpath 表达式
xpath_ahref_first = lambda x: x.xpath('a/@href').extract_first().strip() if bool(x) else None
xpath_text_first = lambda x: x.xpath('text()').extract_first().strip() if bool(x) else None
xpath_aspan_text_first = lambda x: x.xpath('a/span/text()').extract_first().strip() if bool(x) else None
xpath_span_atext_first = lambda x: x.xpath('span/a/text()').extract_first().strip() if bool(x) else None
xpath_atext_first = lambda x: x.xpath('a/text()').extract_first().strip() if bool(x) else None
xpath_string = lambda x: x.xpath('string(.)').extract_first().strip() if bool(x) else None
xpath_text_and_pspan_text = lambda x: x.xpath('p/span/text()|p/text()').extract() if bool(x) else None
xpath_p_text = lambda x: x.xpath('p/text()').extract() if bool(x) else None
xpath_div_ahref_first = lambda x: x.xpath('div/a/@href').extract_first().strip() if bool(x) else None
xpath_span_text = lambda x: x.xpath('span/text()').extract() if bool(x) else None


# 通过比赛时间推算赛季
def get_season_by_date(game_date=None):
    # 中国男子篮球职业联赛
    # 自每年的10月或11月开始至次年的4月左右结束
    game_date = str_to_data_ymd(game_date)  # str_to_data_ymd 获取到的是字符串转换后的时间

    year, month = game_date.year, game_date.month
    season = '{}-{}'.format(year, year + 1) if month >= 7 else '{}-{}'.format(year - 1, year)
    return season


if __name__ == '__main__':
    ss = '2017-02-12'
    # ss = '2017-02-12 00:00:00'
    print get_season_by_date()
    # print get_season(ss)
    # print date_ymd(ss)
