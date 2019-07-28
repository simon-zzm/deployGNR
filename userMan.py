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


class userManHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    @checkSubmitAuth(101)
    def get(self):
        # 获取所有用户信息
        optionData = '<option value="u">选择用户</option>\n'
        for one in rdbAllUserName():
            optionData = '%s<option value="%s">%s</option>\n' % (optionData, one['name'], one['name'])
        # 获取未禁用用户信息
        useOptionData = '<option value="u">选择用户</option>\n'
        for two in rdbUserName():
            useOptionData = '%s<option value="%s">%s</option>\n' % (useOptionData, two['name'], two['name'])
        self.render("userMan.html",  baseInfo = self.baseInfo, \
                                     optionData = optionData, \
                                     useOptionData = useOptionData)


    @htmlBaseInfo
    @auth
    @checkUrl
    @checkSubmitAuth(102)
    def post(self):
        try:
            typeCon = self.get_argument('type')
        except:
            self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'业务异常。'})
            return
        try:
            getUserName = self.get_argument('user')
        except:
            getUserName = ""
        # 重置密码
        if typeCon == "editpass":
            changPasswd = createPasswd()
            changPasswdCount = wdbChangUserPass(getUserName, toPasswd(changPasswd))
            context = ""
            if int(changPasswdCount) == 0:
                context = "重置失败"
            elif int(changPasswdCount) > 0:
                context = "用户:%s,密码修改为:%s" % (getUserName, changPasswd)
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/userMan/')
            return
        # 增加用户
        if typeCon == "adduser":
            try:
                addUser = self.get_argument('adduser')
            except:
                self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'获取新增用户名异常。'})
            # 查看用户名是否存在
            checkUserNameHave = rdbUserNameHave(addUser)[0]['c']
            if int(checkUserNameHave) >= 1:
                context = "该用户名已经存在"
                self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/userMan/')
                return 
            #
            changPasswd = createPasswd()
            insertUserCount = wdbInsertUser(addUser, toPasswd(changPasswd)) 
            context = ""
            if int(insertUserCount) == 0:
                context = "创建用户失败"
            elif int(insertUserCount) > 0:
                context = "用户:%s,密码修改为:%s" % (addUser, changPasswd)
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/userMan/')
            return 
        # 禁用用户
        if typeCon == "deluser":
            # 查看用户名是否存在
            checkUserNameHave = rdbUserNameHave(getUserName)[0]['c']
            if int(checkUserNameHave) == 0:
                context = "该用户名不存在"
                self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/userMan/')
                return
            #
            delUserCount = wdbDelUser(getUserName)
            delUserAuthCount = wdbDelUserAuth(getUserName)
            context = "用户:%s,已经停用。清理该用户组信息%s条。" % (getUserName, delUserAuthCount)
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/userMan/')
            return
        # 用户分组
        if typeCon == "subgroup":
            #
            try:
                getUserName = self.get_argument('user')
                if getUserName == 'u':
                    self.render("error.html", baseInfo = self.baseInfo, \
                                       err = {'text':'用户选择异常。'})
                # 查看用户名是否存在
                checkUserNameHave = rdbUserNameHave(getUserName)[0]['c']
                if int(checkUserNameHave) == 0:
                    context = "该用户名不存在"
                    self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/userMan/')
            except:
                self.render("error.html", baseInfo = self.baseInfo, \
                                       err = {'text':'业务异常。'})
            # 获取选择组id
            try:
                gidContext = self.get_arguments('gid')
            except:
                gidContext = []
            # 清理该用户所有权限
            _ = wdbDelUserGroup(getUserName)
            # 添加用户归属的组
            for onegid in gidContext:
                _ = wdbAddUserGroup(getUserName, onegid)
            context = "用户分配组权限完毕"
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/userMan/')
                

# 异步获取用户组权限信息
class userManGroupHaveHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    def get(self):
        getUserName = self.get_argument('user')
        # 获得该用户所属组权限
        userHaveGroup = []
        for single in rdbUserHaveGroup(getUserName):
            userHaveGroup.append(int(single['id']))
        haveGroupContext = ""
        for oneGroup in rdbAllGroup():
            gid = oneGroup['id']
            gname = oneGroup['group_name']
            if oneGroup['id'] in userHaveGroup:
                haveGroupContext = '''%s&nbsp<input type="checkbox" name="gid" id="gid%s" value="%s" checked="checked">%s''' % \
                       (haveGroupContext, gid, gid, gname)
            else:
                haveGroupContext = '''%s&nbsp<input type="checkbox" name="gid" id="gid%s" value="%s">%s''' % \
                       (haveGroupContext, gid, gid, gname)
        haveGroupContext = haveGroupContext = '''%s&nbsp&nbsp<button type="submit" class="btn btn-default">提交</button>''' % \
                       (haveGroupContext)
        self.write(haveGroupContext)

