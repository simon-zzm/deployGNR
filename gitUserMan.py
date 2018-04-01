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


class gitUserManHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    def get(self):
        # 检查权限107
        if checkAuth(self.baseInfo['getUserName'], 107) < 1:
            self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'权限异常。'})
            return
        self.render("gitUserMan.html",  baseInfo = self.baseInfo)


    @htmlBaseInfo
    @auth
    @checkUrl
    def post(self):
        # 检查权限108
        if checkAuth(self.baseInfo['getUserName'], 108) < 1:
            self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'权限异常。'})
            return
        # 
        try:
            typeCon = self.get_argument('type')
        except:
            self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'业务异常。'})
            return
        # 创建git项目用户
        if typeCon == "gitCreateUser":
            try:
                gitUserName = self.get_argument('gitUserName')
            except:
                self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'业务异常。'})
                return
            # 
            try:
                keyFile = self.request.files['keyFile'][0]['body']
            except:
                keyFile = ''
            # 判断输入是否为空
            if len(gitUserName) == 0 :
                context = "用户名不能为空。"
                self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitUserMan/')
                return
            # 判断用户名重复
            gitUserCou = rdbGitUserNameCount(gitUserName)[0]['c']
            if int(gitUserCou) > 0:
                context = "用户名%s已经存在" % (gitUserName)
                self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitUserMan/')
                return
            # git用户名入库
            gitUserCount = wdbGitUserNameCreate(gitUserName, "%s.pub" % (gitUserName))
            context = "git用户入库%s条" % gitUserCount
            # 如果不为空则存储
            if len(keyFile) > 0:
                tmpKey = open("%s%s.pub" % (gitKeyPath, gitUserName), 'wb+')
                tmpKey.write(keyFile)
                tmpKey.close()
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitUserMan/')
        # 修改git项目用户key
        if typeCon == "gitEditUserKey":
            try:
                gitUserName = self.get_argument('gitUserName')
            except:
                self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'业务异常。'})
                return
            # 
            try:
                keyFile = self.request.files['keyFile'][0]['body']
            except:
                keyFile = ''
            # 判断输入是否为空
            if len(gitUserName) == 0:
                context = "输入用户名不能为空。"
                self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitUserMan/')
                return
            # 判断用户名是否存在
            gitUserCou = rdbGitUserNameCount(gitUserName)[0]['c']
            if int(gitUserCou) == 0:
                context = "用户名%s不存在" % (gitUserName)
                self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitUserMan/')
                return
            # 如果不为空则存储
            if len(keyFile) > 0:
                tmpKey = open("%s%s.pub" % (gitKeyPath, gitUserName), 'wb+')
                tmpKey.write(keyFile)
                tmpKey.close()
            context = "git用户key上传完成" 
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitUserMan/')
        # 删除git用户
        if typeCon == "gitDelUser":
            try:
                gitUserName = self.get_argument('gitUserName')
            except:
                self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'业务异常。'})
                return
            # 判断输入是否为空
            if len(gitUserName) == 0:
                context = "输入用户名不能为空。"
                self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitUserMan/')
                return
            # 判断用户名是否存在
            gitUserCou = rdbGitUserNameCount(gitUserName)[0]['c']
            if int(gitUserCou) == 0:
                context = "用户名%s不存在" % (gitUserName)
                self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitUserMan/')
                return
            # 禁用git用户
            gitUserStopCount = wdbGitUserStop(gitUserName)
            context = "git用户禁用%s条" % gitUserStopCount 
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitUserMan/')
