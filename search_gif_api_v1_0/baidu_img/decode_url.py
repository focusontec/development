# -*- coding: utf-8 -*-
# @Author: zzc
# @Date:   2017.12.01


"""解码百度图片搜索json中传递的url
抓包可以获取加载更多图片时，服务器向网址传输的json。
其中originURL是特殊的字符串
解码前：
ippr_z2C$qAzdH3FAzdH3Ffl_z&e3Bftgwt42_z&e3BvgAzdH3F4omlaAzdH3Faa8W3ZyEpymRmx3Y1p7bb&mla
解码后：
http://s9.sinaimg.cn/mw690/001WjZyEty6R6xjYdtu88&690
使用下面两张映射表进行解码。http://47.95.217.48/api/v1.0/baiduGif?search_engine=1&keyword=%E5%B0%8F%E9%B8%9F&pageNum=1
"""
class DecodeUrl(object):
    def __init__(self):
        self.str_table = {
            '_z2C$q': ':',
            '_z&e3B': '.',
            'AzdH3F': '/'
        }

        self.char_table = {
            'w': 'a',
            'k': 'b',
            'v': 'c',
            '1': 'd',
            'j': 'e',
            'u': 'f',
            '2': 'g',
            'i': 'h',
            't': 'i',
            '3': 'j',
            'h': 'k',
            's': 'l',
            '4': 'm',
            'g': 'n',
            '5': 'o',
            'r': 'p',
            'q': 'q',
            '6': 'r',
            'f': 's',
            'p': 't',
            '7': 'u',
            'e': 'v',
            'o': 'w',
            '8': '1',
            'd': '2',
            'n': '3',
            '9': '4',
            'c': '5',
            'm': '6',
            '0': '7',
            'b': '8',
            'l': '9',
            'a': '0'
        }

        # str 的translate方法需要用单个字符的十进制unicode编码作为key
        # value 中的数字会被当成十进制unicode编码转换成字符
        # 也可以直接用字符串作为value
        self.char_table = {ord(key): ord(value) for key, value in self.char_table.items()}



    def decode(self,url):
        # 先替换字符串
        for key, value in self.str_table.items():
            url = url.replace(key, value)
        # 再替换剩下的字符

        return url.translate(self.char_table)


if __name__ == '__main__':
    # url = "ippr_z2C$qAzdH3FAzdH3Ft4w2jdc_z&e3Bnma15v_z&e3Bv54AzdH3FD5ogs5w1I42AzdH3Fda88AzdH3FanAzdH3F8n8nAzdH3Fll9mdn8_80_z&e3B3r2"
    url = u'ad1f5b5c4961ba5a-7ec4f3a5611f5dc5-19dc33301cd7a0dc7b48e53b23c572ae'
    encoder = DecodeUrl()
    a = encoder.decode(url)
    print a