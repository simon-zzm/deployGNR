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


class deployOnlineHandler(tornado.web.RequestHandler):
    @htmlBaseInfo
    @auth
    @checkUrl
    def get(self):
        onlineInfo = wdbOnlineProject()
        self.render("deployOnline.html", baseInfo = self.baseInfo, \
                                         onlineInfo = onlineInfo)

    @htmlBaseInfo
    @auth
    @checkUrl
    @checkSubmitAuth(102)
    def post(self):
        try:
            projectId = self.get_argument('selectprogramid')
            gitId = self.get_argument('gitid')
        except:
            self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'获取参数'})
            return
        try:
            gitBranchName = self.get_argument('gitbranchname')
        except:
            gitBranchName = ""
        if len("%s" % gitId) != 40:
            self.render("error.html", baseInfo = self.baseInfo, \
                                   err = {'text':'您输入的gitid位数异常请检查。'})
            return
        # 开始执行脚本
        log_context = deploy_run(self.baseInfo['username'], projectId, gitId, gitBranchName)
        #self.render("index.html",  baseInfo = self.baseInfo)


# 自动执行部署脚本
def deploy_run(userName, projectId, gitId, gitBranchName):
    from time import strftime
    # 获取该用户的执行权限
    #user_auth = get_user_auth(user_name)
    getDeployInfo = wdbProjectOnlineInfo(projectId)[0]
    program_name = getDeployInfo['deployName']
    # 初始化日志
    now_date = strftime('%Y%m%d%H%M%S')
    get_log_file = "%s%s-%s" % (logsRootPath, projectId, now_date)
    log_file = open("%s.log" % get_log_file, "a")
    # 记录用户执行信息
    nowTime = getNowTimef6()
    if len(gitBranchName) > 0:
        log_file.write("%s %s %s %s %s\n" % (nowTime, userName, program_name, gitBranchName, gitId))
    else:
        log_file.write("%s %s %s %s\n" % (nowTime, userName, program_name, gitId))
    # 数据库中记录日志
    userId = rdbNameToId(userName)
    print('insert into d_deploy_history(projectId, strTime, userName, gitSrcId, gitBanrch) values("%s", "%s", "%s", "%s", "%s")' % \
                     (projectId, now_date, userName, gitId, gitBranchName))
    get = sqlcomm('insert into d_deploy_history(projectId, strTime, userName, gitSrcId, gitBanrch) values("%s", "%s", "%s", "%s", "%s")' % \
                     (projectId, now_date, userName, gitId, gitBranchName))
    # 获得项目记录
    print('select * from d_deploy_project where id ="%s"' % projectId)
    one_program_info = sqlcomm('select * from d_deploy_project where id ="%s"' % projectId)[0]
    print(one_program_info)
    git_name = one_program_info['deployName']
    work_env = one_program_info['']
    config_env = one_program_info['']
    rsync_info = one_program_info[5]
    print('python dispatch.py "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % \
                                 (git_name, program_name, work_env, config_env, rsync_info, git_id, get_log_file, branch_name))
    return 
    try:
        _status = os.system('python dispatch.py "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % \
                                 (git_name, program_name, work_env, config_env, rsync_info, git_id, get_log_file, branch_name)) >> 8
    except:
        _status = 1
    # 在日志里记录部署状态
    try:
            log_file = open('%s.log' % get_log_file, "rb").readlines()
            if log_file[-1].find("上线完成") > 0 :
                _deploy_status = "OK"
            else:
                _deploy_status = "Error"
            sql = 'update history set deploy_status="%s" where str_time="%s" and user_name="%s" and program_id="%s"' % (_deploy_status, now_date, user_name, program_id)
            _get_status = mysql("%s" % sql, "w")
    except:
            pass
    # 打开日志
    if _status == 0:
            log_context = open("%s.log" % get_log_file, "rb").read()
    elif _status == 1:
            log_context = open("%s.log" % get_log_file, "rb").read()
            #log_context = "执行部署命令失败。%s" % ("python %s.py %s %s %s" % (program_name, git_id, get_log_file, get_user_auth["program"]["%s" % program_name]))
    else:
            log_context = "未知错误,需要人工查找。 %s %s %s" % (program_name, git_id, get_log_file)
    return log_context
    #else:
    #    log_file.write("%s %s %s 没有执行该项目的权限\n" % (strftime('%Y-%m-%d %H:%M:%S'), user_name, program_name))
    #    log_file.close()
    #    return "没有执行该项目的权限"
