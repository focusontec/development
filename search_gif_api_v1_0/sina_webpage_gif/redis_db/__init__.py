#coding=utf-8
import rson

from redis import *

# from gif_api_v1_0 import app

sr = StrictRedis()
class Base():
    def __init__(self):
        pass
    def save(self,name,a,b,num = 0):
        # 左边push进去
        sr.lpush(name,'[{},"{}",{}]'.format(a,b,str(num)))
    def get_info(self,name):
        # 获取最后一个
        res = sr.lrange(name,-1,-1)[0]
        return res
    def delete_info(self,name):
        # 弹出最右边的元素，并返回
        res = sr.rpop(name)
        return res
    def update_info(self,count_num):
        # 修改list　中的信息 使用lset,用来修改计数
        sr.lset('UserInfo',-1,count_num)

    def rotation(self):
        pass



class LoginInfo(Base):
    # 用来存储 uid 和 cookie
    def saveCookieNuid(self,uid,cookies):
        self.save("LoginInfo",uid,"{}".format(cookies))
    def getCookieNuid(self):
        # 取出最右边的cookie所在的列表，根据下表拿到cookie 和　uid
        res = self.get_info("LoginInfo")
        res = eval(res)
        cookies = res[1]
        uid = res[0]
        count_num = res[2]
        return uid,cookies,count_num
    def deleteCookieNuid(self):
        # 删除最后的cookie,并且把最右边的user,pass 放到RestUser队列中:－－－－> 改动：把旧的user 和　pass 放到最左边
        res = self.delete_info("LoginInfo")
        UserPass().change_user_pos()

        return res

    def update_cookies_count(self):
        # 使用一次cookie 后，更新其计数　＋１
        res = self.get_info('LoginInfo')
        res = eval(res)
        res[2] = 1+res[2]
        sr.lset("LoginInfo",-1,str(res))

class UserPass(Base):
    # 用来存储username 和 password
    def saveUserNpass(self,username,passwd):
        self.save("UserInfo",username,passwd)
    def getUserNpasswd(self):
        res = self.get_info("UserInfo")
        res = eval(res)
        username = res[0]
        password = res[1]
        return username,password
    def change_user_pos(self):
        res = self.delete_info("UserInfo")
        self.changee_pos_to_left(res)
    def changee_pos_to_left(self,old_u_p):
        sr.lpush("UserInfo",old_u_p)

class ToFixedUser(Base):
    def sava_old(self,username,password):
        self.save("RestUser",username,password)

if __name__ == '__main__':
    # ll = UserPass()
    # ll.saveUserNpass('zhao','password')
    # print ll.getUserNpasswd()
    log = LoginInfo()
    # log.saveCookieNuid('uid1','cookie2')
    print log.getCookieNuid()
