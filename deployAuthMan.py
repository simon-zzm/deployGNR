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


class projectAuthManHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    def get(self):
        # 项目
        optionData1 = '<option value="u">项目名</option>\n'
        allProject = rdbAlldeployProject()
        for one in allProject:
            optionData1 = '%s<option value="%s">%s</option>\n' % (optionData1, one['id'], one['deployName'])
        self.render("deployAuthMan.html",  baseInfo = self.baseInfo, \
                                       optionData1 = optionData1)


    @htmlBaseInfo
    @auth
    @checkUrl
    def post(self):
        try:
            projectId = self.get_argument('projectId')
            guid = self.get_arguments('guid')
        except:
            self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'业务异常。'})
        # 项目应对用户权限
        _ = wdbDelProjectGroup(projectId)
        for oneGuid in guid:
            _ = wdbProjectGroup(projectId, oneGuid) 
        context = "项目分配用户完成。"
        self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/deployAuth/')


# 异步获取项目分配用户组
class projectHaveGroupAllUserHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    def get(self):
        getProjectId = self.get_argument('projectid')
        # 该项目已有组
        projectHaveGroup = []
        for single in rdbGroupHaveProject(getProjectId):
            projectHaveGroup.append(int(single['deploy_group_id']))
        haveContext = ""
        for one in rdbAllGroup():
            gid = one['id']
            gname = one['group_name']
            if int(gid) in projectHaveGroup:
                haveContext = '''%s&nbsp<input type="checkbox" name="guid" id="guid%s" value="%s" checked="checked">%s''' % \
                       (haveContext, gid, gid, gname)
            else:
                haveContext = '''%s&nbsp<input type="checkbox" name="guid" id="guid%s" value="%s">%s''' % \
                       (haveContext, gid, gid, gname)
        haveContext = '''%s&nbsp&nbsp<button type="submit" class="btn btn-default">提交</button>''' % \
                       (haveContext)
        self.write(haveContext)

