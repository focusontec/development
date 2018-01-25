#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Date  : 2018/1/23
# @Author: lsj
# @File  : translate.py
# @Desc  : 工具类：翻译

pip install PyExecJS

"""
import execjs
import requests


# 谷歌翻译接口
def google_translate(content):
    ctx = execjs.compile(""" 
            function TL(a) { 
            var k = ""; 
            var b = 406644; 
            var b1 = 3293161072; 

            var jd = "."; 
            var $b = "+-a^+6"; 
            var Zb = "+-3^+b+-f"; 

            for (var e = [], f = 0, g = 0; g < a.length; g++) { 
                var m = a.charCodeAt(g); 
                128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
                e[f++] = m >> 18 | 240, 
                e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
                e[f++] = m >> 6 & 63 | 128), 
                e[f++] = m & 63 | 128) 
            } 
            a = b; 
            for (f = 0; f < e.length; f++) a += e[f], 
            a = RL(a, $b); 
            a = RL(a, Zb); 
            a ^= b1 || 0; 
            0 > a && (a = (a & 2147483647) + 2147483648); 
            a %= 1E6; 
            return a.toString() + jd + (a ^ b) 
        }; 

        function RL(a, b) { 
            var t = "a"; 
            var Yb = "+"; 
            for (var c = 0; c < b.length - 2; c += 3) { 
                var d = b.charAt(c + 2), 
                d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
                d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
                a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
            } 
            return a 
        } 
        """)
    tk = ctx.call("TL", content)
    result_zhs = []
    if len(content) > 4891:
        print("content too long!!!")
    else:
        url = 'http://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN' \
              '&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8' \
              '&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2'
        result = requests.get(url, params={'tk': tk, 'q': content})
        if result:
            data_json = result.json()
            try:
                result_zhs.append(data_json[0][0][0])
                result_zh_ss = data_json[5][0][2]
                for result_zh_s in result_zh_ss:
                    result_zhs.append(result_zh_s[0])
            except Exception as e:
                print("get result_zh except", e)
    # return result_zhs[0] if result_zhs else ''
    return result_zhs
    pass
