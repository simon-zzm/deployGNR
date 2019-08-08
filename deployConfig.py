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


class deployConfigHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    def get(self):
        allDeployProject = rdbAlldeployProject()
        # 获取所有项目名
        optionData = '<option value="u">部署项目名</option>\n'
        allDeployProject = rdbAlldeployProject()
        for one in allDeployProject:
            optionData = '%s<option value="%s">%s</option>\n' % (optionData, one['id'], one['gitProjectName'])
        self.render("deployConfig.html", baseInfo = self.baseInfo, \
                                         allDeployProject = allDeployProject, \
                                         optionData = optionData)


    @htmlBaseInfo
    @auth
    @checkUrl
    @checkSubmitAuth(113)
    def post(self):
        # 获取提交类型
        try:
            typeCon = self.get_argument('type')
        except:
            self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'业务异常。'})
            return
        if typeCon == "deployCreateProject":       
            # 
            try:
                deployProName = self.get_argument('deployProjectName')
            except:
                self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'业务异常。'})
                return
            # 检查部署项目名是否存在
            deployProNameCount = int(rdbDeployProName(deployProName)[0]['c'])
            if deployProNameCount > 0:
                context = "输入的项目名%s,已经存在" % (deployProName)
                self.render("global.html",  baseInfo = self.baseInfo, \
                                    text=context, backPage= '/index/deployConfig/')
                return
            ipPort = ""
            user = ""
            passwd = ""
            gitSrc = ""
            gitConf = ""
            exc = ""
        if typeCon == "deployEditProject":
            try:
                deployProId = self.get_argument('deployProjectId')
            except:
                self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'获取项目ID异常。'})
                return
            # 获取项目信息
            deployProjectInfo = rdbDeployProjectInfo(deployProId)[0]
            deployProName = deployProjectInfo['deployName']
            ipPort = deployProjectInfo['deployRsyncIP']
            user = deployProjectInfo['deployRsyncUser']
            passwd = deployProjectInfo['deployRsyncPasswd']
            gitSrc = deployProjectInfo['deployGitSrcUrl']
            gitConf = deployProjectInfo['deployGitConfUrl']
            exc = deployProjectInfo['deployRsyncExclude']
        self.render("addDeployConfig.html",  baseInfo = self.baseInfo, \
                                             deployProName = deployProName, ipPort = ipPort, \
                                             user = user, passwd = passwd, gitSrc = gitSrc, \
                                             gitConf = gitConf, exc = exc)


class addDeployConfigHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    @checkSubmitAuth(115)
    def post(self):
        print("start")
        try:
            deployProName = self.get_argument('deployProjectName')
            ipPort = self.get_argument('ipPort')
            user = self.get_argument('userName')
            passwd = self.get_argument('passwd')
            gitSrc = self.get_argument('gitSrcUrl')
            gitConf = self.get_argument('gitConfUrl')
            exc = self.get_argument('exc')
        except:
            self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'参数异常。'})
            return
        _ = wdbAddDeployProjectInfo(deployProName, ipPort, user, passwd, gitSrc, gitConf, exc)
        self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'录入完成。'})
        return
