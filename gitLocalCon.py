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


class gitLocalConHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    def get(self):
        # 获取所有项目名
        optionData = '<option value="u">项目名</option>\n'
        allGitPro = rdbAllGitProject()
        for one in allGitPro:
            optionData = '%s<option value="%s">%s</option>\n' % (optionData, one['id'], one['gitProjectName'])
        self.render("gitLocalCon.html",  baseInfo = self.baseInfo, \
                                         optionData = optionData)


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
        # 增加组
        if typeCon == "createGitConf":
            # 检查权限111
            if checkAuth(self.baseInfo['getUserName'], 111) < 1:
                self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'权限异常。'})
                return
            try:
                createStatus = ""
                createStatus = createGitConf()
            except:
                self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'创建失败'})
                return
            if len(createStatus) == 0:
                context = "配置创建异常"
            else:
                context = createStatus
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitLocalCon/')
            return
        # 本地创建新库
        if typeCon == "createLocalGitProject":
            # 检查权限112
            if checkAuth(self.baseInfo['getUserName'], 112) < 1:
                self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'权限异常。'})
                return
            # git项目id
            try:
                gitProjectId = self.get_argument('gitProject')
            except:
                self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'获取项目异常'})
                return
            # 确认数据中有该项目
            getGitProjectIdCount = rdbGitProIdCount(gitProjectId)
            if int(getGitProjectIdCount[0]['c']) == 1:
                createStatus = ""
                createStatus = createLocalGit(getGitProjectIdCount[0]['gitProjectName'])
            else:
                context = "该库已经存在，不能被创建"
                self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitLocalCon/')
                return
            if len(createStatus) == 0:
                context = "创建库异常"
            else:
                context = createStatus
            self.render("global.html",  baseInfo = self.baseInfo, \
                                        text=context, \
                                        backPage= '/index/gitLocalCon/')
            return


def createGitConf():
    status = ""
    try:
        confFile = open('gitosis.tmp', 'w')
    except:
        status = "创建本地文件失败。"
        return status
    # 开始创建配置头
    confFile.write("[gitosis]\n")
    confFile.write("")
    confFile.write("[group gitosis-admin]\n")
    confFile.write("members = %s\n" % gitManName)
    confFile.write("writable = gitosis-admin\n")
    confFile.write("\n")
    # 循环创建用户部分
    for oneGitProject in rdbAllGitProject():
        confFile.write("[group %s]\n" % oneGitProject['gitProjectName'])
        confFile.write("writable = %s\n" % oneGitProject['gitProjectName'])
        memContext = "members = %s " % gitManName
        # 循环写入管理用户
        for oneGitUser in rdbGitProjectHaveGitUser(oneGitProject['id']): 
            memContext = "%s %s " % (memContext, oneGitUser['gitUser'])
        confFile.write("%s\n" % memContext)
        confFile.write("\n")
    # 写入完成
    confFile.close()
    status = "本地创建配置完成。"
    # 移动到git配置并赋值
    import os
    from shutil import copy2,move
    # 备份
    try:
        copy2('%sgitosis.conf' % gitRootPath, '%sgitosis.%s' % (gitRootPath, getNowUnixTimeInt()))
        status = "%s。备份完成。" % status
    except:
        status = "%s。备份原始文件失败。" % status
        pass
    # 复制
    try:
        move('gitosis.tmp', '%sgitosis.conf' % gitRootPath)
        status = "%s。复制配置完成。" % status
    except:
        status = "%s。复制失败。" % status
    # 变更权限
    try:
        os.chown('%sgitosis.conf' % gitRootPath, int(gitSYSAuth.split('.')[0]), int(gitSYSAuth.split('.')[1]))
        status = "%s。权限变更完成。" % status
    except:
        status = "%s。权限变更失败。" % status
    # 提交到服务器
    try:
        os.chdir(gitRootPath)
        os.system('git add .')
        os.system("git commit -am 'conf change at %s'" % getNowUnixTimeInt())
        os.system('git push origin master')
        status = "%s。git提交完成。" % status
    except:
        status = "%s。git提交失败。" % status
    return status



def createLocalGit(gitProjectName):
    import os
    status = "开始初始化git库"
    # 进入主目录
    try:
        os.chdir(gitLocalPath)
        status = "%s进入初始化目录完成。" % status
    except:
        status = "%s进入初始化目录失败。" % status
    # 初始化项目目录
    try:
        os.mkdir(gitProjectName)
        os.chdir("%s%s" % (gitLocalPath, getiProjectName))
        status = "%s创建项目目录完成。" % status
    except:
        status = "%s创建项目目录失败。" % status
    # 项目初始化
    try:
        os.system("git init")
        os.mknod("readmet.txt")
        os.system("git add .")
        status = "%s本地初始化完成。" % status
    except:
        status = "%s本地初始化失败。" % status
    # 项目提交
    try:
        os.system("git commit -am 'create project %s'" % gitProjectName)
        os.system("git remote add origin %s:%s" % (gitManName, gitProjectName))
        os.system("git push origin master ")
        status = "%s项目提交完成。" % status
    except:
        status = "%s项目提交失败。" % status
    return status
