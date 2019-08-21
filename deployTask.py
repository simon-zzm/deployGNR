#!env python3
# -*- coding:utf-8 -*-
# Author:      simonzhang
# Email:       simon-zzm@163.com
# web:         www.simonzhang.net
import os
import sys
import sys
import uuid
sys.path.append('..')
from config import programPath

def now_time():
    from time import strftime
    return strftime('%Y-%m-%d %H:%M:%S')

# 通用写日志，函数
def write_log(log_file, context):
    with open(log_file, "a") as lfile:
        lfile.write("%s %s\n" % (now_time(), context))

# 专写错误和异常日志
def error_log(log_file, line, error_return, context):
    write_log(log_file, line)
    write_log(log_file, error_return)
    write_log(log_file, context)

def str_to_list(str_info):
    from string import strip
    # 初始化一个列表
    rsync_info = []
    # 父级列表之间用"?"分割
    # 循环处理父级的
    f_list = str_info.split('?')
    for f_num in xrange(0, len(f_list)):
        # 每次循环增加一个子列表,如果但是单个数据则直接添加
        if f_list[f_num][0] == "[":
            # 两级列表，要现增加一个新的
            rsync_info.append([])
            for s_one in f_list[f_num][1:-1].split(','):
                rsync_info[f_num].append(strip(s_one))
        else:
            rsync_info.append(f_list[f_num])
    return rsync_info


def getProjectGit(pi, lf):
    # 开始同步项目git代码
    if len(pi['gitBranchName']) >1:
        _line = ("python3 bin/dogit.py -H %s -p '' -P %sdata/%s -g %s -i %s -b %s" % \
                    (pi['deployGitSrcUrl'], \
                     programPath, \
                     pi['deployName'], \
                     pi['deployName'], \
                     pi['gitShaId'], \
                     pi['gitBranchName']))
    else:
        _line = ("python3 bin/dogit.py -H %s -p '' -P %sdata/%s -g %s -i %s " % \
                    (pi['deployGitSrcUrl'], \
                     programPath, \
                     pi['deployName'], \
                     pi['deployName'], \
                     pi['gitShaId']))
    #print(_line)
    try:
        _status = os.popen("%s" % _line).read()
        if _status.find('ok') == -1:
            error_log(lf, _line, _status, "获取程序代码出错")
            return
        write_log(lf, "获取程序代码成功")
    except:
        error_log(lf, _line, _status,"获取程序代码异常")
        return
    """
    # 移除准备上线代码目录
    _line = ("/bin/rm -rf data/%s%s" % (pi['deployName'], work_env))
    try:
        _status = os.system("%s" % _line) >> 8
        if int(_status) > 0 :
            error_log(lf, _line, _status, "删除上线目录出错")
            return
        write_log(lf, "删除上线目录成功")
    except:
        error_log(lf, _line, _status, "删除上线目录异常")
        return
    # 创建新的上线目录
    _line = ("/bin/mkdir -p %sdata/%s" % (programPath, pi['deployName']))
    try:
        _status = os.system("%s" % _line) >> 8
        if int(_status) > 0 :
            error_log(lf, _line, _status, "创建上线目录出错")
            return 
        write_log(lf, "创建上线目录成功")
    except:
        error_log(lf, _line, _status, "创建上线目录异常")
        return
    # 解压线上代码包
    _line = ("/usr/bin/unzip -q %sdata/%s.zip -d %sdata/%s" % (programPath, pi['deployName'], programPath, pi['deployName']))
    try:
        _status = os.system("%s" % _line) >> 8
        if int(_status) > 0 :
            error_log(lf, _line, _status, "解压上线代码包出错")
            return
        write_log(lf, "解压上线代码成功")
    except:
        error_log(lf, _line, _status, "解压上线代码包异常")
        return
    # 清理上压缩文件
    _line = ("/bin/rm -rf %sdata/%s.zip" % (programPath, pi['deployName']))
    try:
        _status = os.system("%s" % _line) >> 8
        if int(_status) > 0 :
            error_log(lf, _line, _status, "清理上线代码压缩包出错")
            return
        write_log(lf, "清理上线代码压缩包成功")
    except:
        error_log(lf, _line, _status, "清理上线代码压缩包异常")
        return
    # 获取配置文件，如果为空则跳过
    if config_env == "None":
        pass
    else:
        # 获取配置文件
        _line = ("python dogit.py -H%s -p%s -P%s/data/%s%s -g %s%s" %
                 (git_ip, git_passwd, base_path, program_git_name, config_env, program_git_name, config_env))
        try:
            _status = os.system("%s" % _line) >> 8
            if int(_status) > 0 :
                error_log(lf, _line, _status, "获取项目配置出错")
                return
            write_log(lf, "获取项目配置成功")
        except:
            #_line = ("python dogit.py -H%s -p%s -P%s/data/%s%s -g %s%s" %
            #         (git_ip, git_passwd, base_path, program_git_name, config_env, program_git_name, config_env))
            error_log(lf, _line, _status, "获取项目配置异常")
            return
        # 线上配置解包
        _line = ("/usr/bin/unzip -q -o data/%s%s.zip -d %s/data/%s%s" %
                 (program_git_name, config_env, base_path, program_git_name, work_env))
        try:
            _status = os.system("%s" % _line) >> 8
            if int(_status) > 0 :
                error_log(lf, _line, _status, "解压线上配置出错")
                return
            write_log(lf, "解压线上配置成功")
        except:
            error_log(lf, _line, _status, "解压线上配置异常")
            return
        # 清理压缩包
        _line = ("/bin/rm -rf data/%s%s.zip" % (program_git_name, config_env))
        try:
            _status = os.system("%s" % _line) >> 8
            if int(_status) > 0 :
                error_log(lf, _line, _status, "清理线上配置包出错")
                return
            write_log(lf, "清理线上配置包成功")
        except:
            error_log(lf, _line, _status, "清理线上配置包异常")
            return
        """

def pushRsync(pi, lf):
    # 开始同步代码
    # python3  dorsync.py  -H 182.92.186.219 -d 22 -L /home/git/deployGNR/deployGNR/data/test99/ -e '123.txt|.git' -u root -p pass -R /program/www/test99
    for rsyncIp in pi['deployRsyncIP'].split(','):
        # 拼接命令行
        if len(pi['deployRsyncExclude']) == 0:
            _line = ("python3 bin/dorsync.py  -H %s -d %s -L %sdata/%s/ -u %s -p %s -R %s" %
                      (rsyncIp.split(":")[0], rsyncIp.split(":")[1],  programPath, pi['deployName'], pi['deployRsyncUser'], pi['deployRsyncPasswd'], pi['deployRsyncPath']))
        else:
            _line = ("python3 bin/dorsync.py  -H %s -d %s -L %sdata/%s/ -e '%s' -u %s -p %s -R %s" %
                      (rsyncIp.split(":")[0], rsyncIp.split(":")[1], programPath, pi['deployName'], pi['deployRsyncExclude'], pi['deployRsyncUser'], pi['deployRsyncPasswd'], pi['deployRsyncPath']))
        #print(_line)
        # 执行命令
        rsync_status = 0
        try:
            get_status = os.popen("%s" % _line).read()
            if get_status.find('ok') == -1 :
                error_log(deploy_log_file, _line, _status, "同步到%s出错" % rsync_info[0])
                rsync_status = 1
            else:
                write_log(lf, "同步到%s成功" % rsync_info[0])
                # 同步版本文件
                try:
                    vf = open("%s/data/%s%s/version.txt" % (base_path, program_git_name, work_env), 'wb')
                    vf.write("%s" % git_sha_id)
                    vf.close()
                except:
                    pass
                get_status = os.popen("%s" % _line).read()
                if get_status.find('ok') == -1 :
                    error_log(deploy_log_file, _line, _status, "同步版本文件到%s出错" % rsync_info[0])
                    rsync_status = 1
                else:
                    write_log(lf, "同步版本文件到%s成功" % rsync_info[0])
        except:
            error_log(deploy_log_file, _line, _status, "同步到%s异常" % rsync_info[0])
            rsync_status = 1
    # 记录rsync状态日志
    if rsync_status == 0:
        write_log(lf, "本次上线完成。全部成功。")
    else:
        write_log(lf, "本次上线完成。有部分错误，请详查日志。")
    # 展示所有日志
    log_file = open("%s" % deploy_log_file, "rb").read()
    return log_file


def run(proInfo, logFile):
    os.chdir('%s' % programPath)
    # 获取git
    getProjectGit(proInfo, logFile)
    # 推送程序
    pushRsync(proInfo, logFile)
    #print("ok")
