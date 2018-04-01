#!/usr/bin/python3
#-*- coding:utf-8 -*-
# Author:      simonzhang
# web:         www.simonzhang.net
# Email:       simon-zzm@163.com
##########
### END INIT INFO
#import tornado.ioloop
#import tornado.locale
import tornado.web
#from dbmodules import *
from modules import *


class MainHandler(tornado.web.RequestHandler):
    # 基础信息。包含title,username,domainname,colconumn
    @htmlBaseInfo
    # 认证部分。如果不需要认证，则注释掉下面一行
    @auth
    # 检查输入参数，防止sql注入,黑白名单等
    @checkUrl
    def get(self):
        self.render("index.html",  baseInfo = self.baseInfo)

    @auth
    @checkUrl
    def post(self):
        getSessionId = self.get_secure_cookie("userInfo").split(",")[2]
        redisDB.delete("%s" % getSessionId)
        self.clear_all_cookies()
        self.redirect("/")

