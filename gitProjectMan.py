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


class gitProjectManHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    @checkSubmitAuth(105)
    def get(self):
        # 获取所有项目名
        optionData = '<option value="u">项目名</option>\n'
        allGitPro = rdbAllGitProject()
        for one in allGitPro:
            optionData = '%s<option value="%s">%s</option>\n' % (optionData, one['id'], one['gitProjectName'])
        self.render("gitProjectMan.html",  baseInfo = self.baseInfo, \
                                     optionData = optionData, allGitPro = allGitPro)


    @htmlBaseInfo
    @auth
    @checkUrl
    @checkSubmitAuth(106)
    def post(self):
        try:
            typeCon = self.get_argument('type')
        except:
            self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'业务异常。'})
            return
        # 创建git项目
        if typeCon == "gitCreateProject":
            try:
                gitProjectName = self.get_argument('gitProjectName')
            except:
                self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'业务异常。'})
                return
            try:
                gitProjectUrl = self.get_argument('gitProjectUrl')
            except:
                gitProjectURL = ""
            # 判断输入是否为空
            if len(gitProjectName) == 0:
                context = "输入的项目名%s，地址%s异常" % (gitProjectName, gitProjectUrl)
                self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitProjectMan/')
            # 判断git项目名重复
            gitProCou = rdbGitProjectNameCount(gitProjectName)[0]['c']
            if int(gitProCou) > 0:
                context = "项目名%s已经存在" % (gitProjectName)
                self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitProjectMan/')
            # git项目入库
            gitProjectCount = wdbGitProjectNameCreate(gitProjectName, gitProjectUrl)
            context = "git项目入库%s条" % gitProjectCount
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitProjectMan/')
        # 修改git项目URL
        if typeCon == "gitEditProjectGitUrl":
            try:
                gitProjectId = self.get_argument('gitProjectId')
                gitProjectUrl = self.get_argument('gitProjectUrl')
            except:
                self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'业务异常。'})
                return
            # 判断输入是否为空
            if len(gitProjectId) == 0 or len(gitProjectUrl) == 0:
                context = "输入的项目名%s，地址%s异常" % (gitProjectId, gitProjectUrl)
                self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitProjectMan/')
            # git项目url入库
            gitProjectCount = wdbGitProjectUrlChange(gitProjectId, gitProjectUrl)
            context = "git项目入库%s条" % gitProjectCount
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitProjectMan/')
        # 删除git项目
        if typeCon == "gitDelProject":
            try:
                gitProjectId = self.get_argument('gitProjectId')
            except:
                self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'业务异常。'})
                return
            # 判断输入是否为空
            if len(gitProjectId) == 0:
                context = "项目不存在"
                self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitProjectMan/')
            # git项目url入库
            gitProjectCount = wdbGitProjectDel(gitProjectId)
            context = "git项目入库%s条" % gitProjectCount
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitProjectMan/') 
