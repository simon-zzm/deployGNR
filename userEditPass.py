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


class userEditPassHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    def get(self):
        self.render("userEditPass.html",  baseInfo = self.baseInfo)


    @htmlBaseInfo
    @auth
    @checkUrl
    def post(self):
        getUserName = self.baseInfo['getUserName']
        try:
            oldPass = self.get_argument('oldpasswd')
        except:
            oldPass = ""
        try:
            newPass1 = self.get_argument('newpasswd1')
        except:
            newPass1 = ""
        try:
            newPass2 = self.get_argument('newpasswd2')
        except:
            newPass2 = ""
        #
        userInfo = rdbUserInfo(getUserName)
        passstr = userInfo['passwd']
        # 
        context = ""
        if len(newPass1) > 0 and newPass1 == newPass2:
            if checkPasswd(oldPass, passstr):
                editCount = wdbChangMePass(toPasswd(newPass1), getUserName)
                if editCount == 1:
                    self.render("login.html", title = title)
                    return 
                else:
                    context = "修改失败"
            else:
                context = "旧密码输入有误"
        else:
            context = "新密码输入有误"
        self.render("global.html",  baseInfo = self.baseInfo, \
                                    text = context, \
                                    backPage = '/index/userEditPass/')
