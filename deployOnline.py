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
        self.render("deployOnline.html", baseInfo = self.baseInfo)

    @htmlBaseInfo
    @auth
    @checkUrl
    @checkSubmitAuth(102)
    def post(self):
        try:
            projectName = self.get_argument('project')
            gitId = self.get_argument('gitId')
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
        log_context = deploy_run(program_id, program_git_id, user_name, branch_name)
        self.render("index.html",  baseInfo = self.baseInfo)


# 自动执行部署脚本
def deploy_run(program_id, git_id, user_name, branch_name):
    from time import strftime
    os.chdir("%s" %  base_path)
    # 获取该用户的执行权限
    user_auth = get_user_auth(user_name)
    program_name = "%s%s" % (get_single_program_name(program_id)[0], get_single_program_name(program_id)[1])
    program_info = get_program_info(user_auth)
    programs_info = {}
    for one in program_info:
        programs_info[one[1]+one[3]] = "%s|%s" % (one[0], one[2])
    # 初始化日志
    now_date = strftime('%Y%m%d%H%M%S')
    get_log_file = "logs/%s-%s" % (program_id, now_date)
    log_file = open("%s.log" % get_log_file, "ab")
    # 判断该用户是否有执行项目权限。
    # 如没有则写日志返回值
    # 如有权限记录用户执行信息
    if "%s" % program_id in user_auth.split(','):
        if len(branch_name) > 0:
            log_file.write("%s %s %s %s %s\n" % (strftime('%Y-%m-%d %H:%M:%S'), user_name, program_name, branch_name, git_id))
        else:
            log_file.write("%s %s %s %s\n" % (strftime('%Y-%m-%d %H:%M:%S'), user_name, program_name, git_id))
        log_file.close()
        # 数据库中记录日志
        user_id = get_user_id(user_name)
        get = mysql('insert into history(program_id, str_time, user_id, user_name, git_id, git_banrch) values("%s", "%s", %s, "%s", "%s", "%s")' % \
                     (program_id, now_date, user_id, user_name, git_id, branch_name), 'w')
        # 获得项目记录
        one_program_info = mysql('select * from program where id ="%s"' % program_id, 'r')[0]
        git_name = one_program_info[2]
        work_env = one_program_info[3]
        config_env = one_program_info[4]
        rsync_info = one_program_info[5]
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
    else:
        log_file.write("%s %s %s 没有执行该项目的权限\n" % (strftime('%Y-%m-%d %H:%M:%S'), user_name, program_name))
        log_file.close()
        return "没有执行该项目的权限"
