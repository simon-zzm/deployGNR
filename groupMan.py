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


class groupManHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    @checkSubmitAuth(103)
    def get(self):
        # 获取所有用户信息
        optionData = '<option value="u">选择组</option>\n'
        allGroup = rdbAllGroup()
        for one in allGroup:
            optionData = '%s<option value="%s">%s</option>\n' % (optionData, one['id'], one['group_name'])
        self.render("groupMan.html",  baseInfo = self.baseInfo, \
                                     optionData = optionData, allGroup=allGroup)


    @htmlBaseInfo
    @auth
    @checkUrl
    @checkSubmitAuth(104)
    def post(self):
        try:
            typeCon = self.get_argument('type')
        except:
            self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'业务异常。'})
            return
        # 增加组
        if typeCon == "addgroup":
            try:
                getGroupName = self.get_argument('group')
            except:
                self.render("error.html", baseInfo = self.baseInfo, \
                                 err = {'text':'获取组名异常。'})
            try:
                groupMark = self.get_argument('groupmark')
            except:
                groupMark = ""
            # 查看用组名是否存在
            checkGroupNameHave = rdbGroupNameHave(getGroupName)[0]['c']
            if int(checkGroupNameHave) >= 1:
                context = "该组经存在。"
                self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/groupMan/')
                return 
            #
            insertGroupCount = wdbInsertGroup(getGroupName, groupMark)
            context = ""
            if insertGroupCount == 0:
                context = "创建组失败。"
            elif insertGroupCount > 0:
                context = "创建了‘%s ’组。" % (getGroupName)
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/groupMan/')
            return
        # 组用户使用权限
        if typeCon == "groupuseauth":
            # 获取组id
            getGroupId = self.get_argument('groupuseauth')
            # 获取选择使用权id
            try:
                subIdContext = self.get_arguments('subId')
            except:
                subIdContext = []
            # 清理该组所有使用权
            _ = wdbDelGroupUseAuth(getGroupId)
            # 添加组使用权限
            for oneSubId in subIdContext:
                _ = wdbAddGroupUseAuth(getGroupId, oneSubId)
            context = "组使用权限分配完毕"
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/groupMan/')
        # 组用户使用菜单的权限
        if typeCon == "groupusecol":
            # 获取组id
            getGroupId = self.get_argument('groupusecol')
            # 获取选择使用权id
            haveColId = []
            try:
                colIdContext = self.get_arguments('colId')
                for oneData in colIdContext:
                    if oneData.split('-')[0] not in haveColId:
                        haveColId.append(oneData.split('-')[0])
                    if oneData.split('-')[1] not in haveColId:
                        haveColId.append(oneData.split('-')[1])
            except:
                haveColId = []
            # 清理该组所有使用权
            _ = wdbDelGroupUseCol(getGroupId)
            # 添加组使用权限
            for oneColId in haveColId:
                _ = wdbAddGroupUseCol(getGroupId, oneColId)
            context = "组使用菜单分配完毕"
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/groupMan/')


# 
class groupUseAuthHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    def get(self):
        getGroupId = self.get_argument('group')
        # 获得该组使用权限
        groupHaveUseAuth = []
        for single in rdbGroupHaveUseAuth(getGroupId):
            groupHaveUseAuth.append(int(single['submit_id']))
        groupHaveUseAuthContext = ""
        for oneSub in rdbAllSubmit():
            subId = oneSub['submit_id']
            subLoc = oneSub['submit_local']
            if subId in groupHaveUseAuth:
                groupHaveUseAuthContext = '''%s<div class="row"><div class="col-sm-6"><input type="checkbox" name="subId" id="subId%s" value="%s" checked="checked">%s</div></div>''' % \
                       (groupHaveUseAuthContext, subId, subId, subLoc)
            else:
                groupHaveUseAuthContext = '''%s<div class="row"><div class="col-sm-6"><input type="checkbox" name="subId" id="subId%s" value="%s">%s</div></div>''' % \
                       (groupHaveUseAuthContext, subId, subId, subLoc)
        groupHaveUseAuthContext = '''%s&nbsp<div class="row"><div class="col-sm-2"><button type="submit" class="btn btn-default">提交</button></div></div>''' % groupHaveUseAuthContext
        self.write(groupHaveUseAuthContext)


class groupUseColHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    def get(self):
        getGroupId = self.get_argument('group')
        # 获得该组使用权限
        groupHaveUseCol = []
        for single in rdbGroupHaveUseCol(getGroupId):
            groupHaveUseCol.append("%s-%s" % (single['id1'], single['id2']))
        groupHaveUseColContext = ""
        for oneCol in rdbAllColumn():
            colId = "%s-%s" % (oneCol['id1'], oneCol['id2'])
            colName = oneCol['name2']
            if colId in groupHaveUseCol:
                groupHaveUseColContext = '''%s<div class="row"><div class="col-sm-6"><input type="checkbox" name="colId" id="colId%s" value="%s" checked="checked">%s</div></div>''' % \
                       (groupHaveUseColContext, colId, colId, colName)
            else:
                groupHaveUseColContext = '''%s<div class="row"><div class="col-sm-6"><input type="checkbox" name="colId" id="colId%s" value="%s">%s</div></div>''' % \
                       (groupHaveUseColContext, colId, colId, colName)
        groupHaveUseColContext = '''%s&nbsp<div class="row"><div class="col-sm-2"><button type="submit" class="btn btn-default">提交</button></div></div>''' % groupHaveUseColContext
        self.write(groupHaveUseColContext)
