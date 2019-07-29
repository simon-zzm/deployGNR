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


class gitAuthManHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    def get(self):
        # 项目
        optionData1 = '<option value="u">项目名</option>\n'
        allGitPro = rdbAllGitProject()
        for one in allGitPro:
            optionData1 = '%s<option value="%s">%s</option>\n' % (optionData1, one['id'], one['gitProjectName'])
        # 用户
        optionData2 = '<option value="u">用户</option>\n'
        for one in rdbAllGitUser():
            optionData2 = '%s<option value="%s">%s</option>\n' % (optionData2, one['id'], one['gitUser'])
        self.render("gitAuthMan.html",  baseInfo = self.baseInfo, \
                                       optionData1 = optionData1, \
                                       optionData2 = optionData2)


    @htmlBaseInfo
    @auth
    @checkUrl
    def post(self):
        try:
            typeCon = self.get_argument('type')
        except:
            self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'业务异常。'})
            return
        # 根据项目修改用户
        if typeCon == "gitProjectDisUser":
            checkSubmitAuth(109)
            # 获取项目id
            try:
                gitProjectId = self.get_argument('gitProjectId')
            except:
                self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'获取项目id异常。'})
                return
            # 获取用户id
            try:
                gitUserIds = self.get_arguments('guid')
            except:
                self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'获取用户id异常。'})
                return
            # 项目应对用户权限
            _ = wdbDelGitProjectUser(gitProjectId)
            for oneGitUserId in gitUserIds:
                _ = wdbProjectGitDisUser(gitProjectId, oneGitUserId) 
            context = "git项目分配用户完成。"
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitAuthMan/')
        # 根据用户修改项目
        if typeCon == "gitUserDisProject":
            checkSubmitAuth(110)
            # 项目id
            try:
                gitUserId = self.get_argument('gitUserId')
            except:
                self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'获取用户id异常。'})
                return
            # 获取用户id
            try:
                gitProjectIds = self.get_arguments('gproid')
            except:
                self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'获取项目id异常。'})
                return
            # 用户对应项目权限入库
            _ = wdbDelGitUserProject(gitUserId)
            for oneGitProjectId in gitProjectIds:
                _ = wdbProjectGitDisUser(oneGitProjectId, gitUserId)
            context = "用户分配git项目完成。"
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitAuthMan/')


# 异步获取项目分配用户信息
class projectHaveUserAllUserHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    def get(self):
        getGitProjectId = self.get_argument('projectid')
        # 该项目已有用户
        projectHaveGitUser = []
        for single in rdbUserHaveGitProject(getGitProjectId):
            projectHaveGitUser.append(int(single['gitUserId']))
        haveGitContext = ""
       
        for oneGitUser in rdbAllGitUser():
            gid = oneGitUser['id']
            gname = oneGitUser['gitUser']
            if oneGitUser['id'] in projectHaveGitUser:
                haveGitContext = '''%s&nbsp<input type="checkbox" name="guid" id="guid%s" value="%s" checked="checked">%s''' % \
                       (haveGitContext, gid, gid, gname)
            else:
                haveGitContext = '''%s&nbsp<input type="checkbox" name="guid" id="guid%s" value="%s">%s''' % \
                       (haveGitContext, gid, gid, gname)
        haveGitContext = '''%s&nbsp&nbsp<button type="submit" class="btn btn-default">提交</button>''' % \
                       (haveGitContext)
        self.write(haveGitContext)

# 异步获取用户分配项目信息
class userHavePorjectAllProjectHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    def get(self):
        getGitUserId = self.get_argument('userid')
        # 该用户已有的项目
        gitUserHaveProject = []
        for single in rdbProjectHaveGitUser(getGitUserId):
            gitUserHaveProject.append(int(single['gitProjectId']))
        haveProjectContext = ""
        for oneGitProject in rdbAllGitProject():
            gid = oneGitProject['id']
            gproject = oneGitProject['gitProjectName']
            if gid in gitUserHaveProject:
                haveProjectContext = '''%s&nbsp<input type="checkbox" name="gproid" id="gproid%s" value="%s" checked="checked">%s''' % \
                       (haveProjectContext, gid, gid, gproject)
            else:
                haveProjectContext = '''%s&nbsp<input type="checkbox" name="gproid" id="gproid%s" value="%s">%s''' % \
                       (haveProjectContext, gid, gid, gproject)
        haveProjectContext = '''%s&nbsp&nbsp<button type="submit" class="btn btn-default">提交</button>''' % \
                       (haveProjectContext)
        self.write(haveProjectContext)
