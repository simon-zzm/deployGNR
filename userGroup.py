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


class userGroupHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    def get(self):
        # 检查权限103
        if checkAuth(self.baseInfo['getUserName'], 103) < 1:
            self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'权限异常。'})
            return
        # 
        optionData = ''
        for one in rdbAllUserName():
            optionData = '%s<option value="%s">%s</option>\n' % (optionData, one['name'], one['name'])
        self.render("userMan.html",  baseInfo = self.baseInfo, \
                                     optionData = optionData)


    @htmlBaseInfo
    @auth
    @checkUrl
    def post(self):
        # 检查权限102
        if checkAuth(self.baseInfo['getUserName'], 101) < 1:
            self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'权限异常。'})
            return
        # 
        try:
            typeCon = self.get_argument('type')
            getUserName = self.get_argument('user')
        except:
            self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'业务异常。'})
            return
        # 重置密码
        if typeCon == "editpass":
            changPasswd = createPasswd()
            changPasswdCount = wdbChangePass(getUserName, toPasswd(changPasswd))
            context = ""
            if editCountLine == 0:
                context = "重置失败"
            elif editCountLine > 0:
                context = "用户:%s,密码修改为:%s" % (getUserName, changPasswd)
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/userMan')
            return
        # 增加用户
        if typeCon == "adduser":
            # 查看用户名是否存在
            checkUserNameHave = rdbUserNameHave(getUserName)[0]['c']
            if int(checkUserNameHave) >= 1:
                context = "该用户名已经存在"
                self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/userMan')
                return 
            #
            changPasswd = createPasswd()
            insertUserCount = wdbInsertUser(getUserName, toPasswd(changPasswd)) 
            context = ""
            if editCountLine == 0:
                context = "创建用户失败"
            elif editCountLine > 0:
                context = "用户:%s,密码修改为:%s" % (getUserName, changPasswd)
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/userMan')
            return 
        # 删除用户
        if typeCon == "deluser":
            # 查看用户名是否存在
            checkUserNameHave = rdbUserNameHave(getUserName)[0]['c']
            if int(checkUserNameHave) == 0:
                context = "该用户名不存在"
                self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/userMan')
                return
            #
            delUserCount = wdbDelUser(getUserName)
            delUserAuthCount = wdbDelUserAuth(getUserName)
            context = "用户:%s,已经停用。清理该用户租信息%s条。" % (getUserName, delUserAuthCount)
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/userMan')
            return
