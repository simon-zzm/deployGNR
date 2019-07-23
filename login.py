#!/usr/bin/python3
#-*- coding:utf-8 -*-
# Author:      simonzhang
# web:         www.simonzhang.net
# Email:       simon-zzm@163.com
### END INIT INFO
#import sys
#import re
#import uuid
import tornado.ioloop
import tornado.web

from config import *
from modules import *
from dbmodules import *

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        getLoginIP = checkIP(self)
        if (len(getLoginIP) == 0):
            try:
               getNowUser = self.get_secure_cookie("userInfo").split(",")[0]
               getSessionId = self.get_secure_cookie("userInfo").split(",")[2]
            except:
               getNowUser = "Null"
               getSessionId = ""
            # 检查是否在redis中
            if redisDB.get("%s" % getSessionId) == getNowUser:
                self.redirect("/index/")
            else:
                self.set_secure_cookie("userInfo", ",," , \
                                           path="/", expires_days = cookieTimeoutDays)
                self.render("login.html", title = title)
        else:
            self.redirect("%s:%s" % (domainName, listenPort))

    def post(self):
        try:
            userName = self.get_argument("user")
            passwd = self.get_argument("passwd")
            userInfo = rdbUserInfo(userName)
            passstr = userInfo[3]
            if passwd is not None:
                if checkPasswd(passwd, passstr):
                    if getClentIp(self)[0] == "Null":
                        uIP = getClentIp(self)[1]
                    else:
                        uIP = getClentIp(self)[0]
                    # 获得昵称
                    try:
                        nickName = userInfo['nick_name']
                    except:
                        nickName = ''
                    # 用uuid做sessionId
                    sessionId = str(uuid.uuid3(uuid.uuid1(), str(userName)))
                    self.set_secure_cookie("userInfo", "%s,%s,%s,%s" % (userName, uIP, sessionId, nickName), \
                                           path="/", expires_days = cookieTimeoutDays)
                    # session写入 redis
                    try:
                         redisDB.setex("%s" % sessionId, sessionTimeout, "%s" % userName)
                         self.redirect("/index/")
                    except:
                         self.write("redis 异常")
                else:
                    self.render("login.html", title = title) 
            else:
               self.render("login.html", title = title)
        except:
            self.render("login.html", title = title)
            return
