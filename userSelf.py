#!/usr/bin/python3
#-*- coding:utf-8 -*-
# Author:      simonzhang
# web:         www.simonzhang.net
# Email:       simon-zzm@163.com
### END INIT INFO
import tornado.ioloop
import tornado.web

from config import *
from modules import *
from dbmodules import *


class userSelfHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    def get(self):
        getUserName = self.baseInfo['getUserName']
        # 获取用户个人信息
        getUserAllInfo = rdbUserSelf(getUserName)
        self.render("userSelf.html",  baseInfo = self.baseInfo, \
                                      userSelf = getUserAllInfo)

    @htmlBaseInfo
    @auth
    @checkUrl
    def post(self):
        getUserName = self.baseInfo['getUserName']
        try:
            getNickName = self.get_argument("nickname")
        except:
            getNickName = ""
        try:
            getEmail = self.get_argument("email")
        except:
            getEmail = ""
        try:
            getPhonenum = self.get_argument("phonenum")
        except:
            getPhonenum = 13
        if len(getPhonenum) == 0:
            getPhonenum = 13
        # 修改用户信息
        editCountLine = wdbUserSelf(getUserName, getNickName, getEmail, getPhonenum)
        context = ""
        if editCountLine == 0:
            context = "修改失败"
        elif editCountLine > 0:
            context = "本次修改了%s条数据" % editCountLine
        self.render("global.html",  baseInfo = self.baseInfo, \
                                    text=context, \
                                    backPage= '/index/userSelf/')
