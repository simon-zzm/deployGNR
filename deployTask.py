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
    with open("%s%s" % (logsRootPath, log_file), "a") as lfile:
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
    print("=" * 10)
    print(pi)
    # 开始同步项目git代码
    if len(pi['gitBranchName']) >1:
        _line = ("python bin/dogit.py -H%s -p%s -P%s/data/%s -g %s -i %s -b %s" % \
                    (pi['deployGitSrcUrl'], \
                     '', \
                     programPath, \
                     pi['deployName'], \
                     pi['deployName'], \
                     pi['gitShaId'], \
                     pi['gitBranchName']))
    else:
        _line = ("python bin/dogit.py -H%s -p%s -P%s/data/%s -g %s -i %s " % \
                    (pi['deployGitSrcUrl'], \
                     '', \
                     programPath, \
                     pi['deployName'], \
                     pi['deployName'], \
                     pi['gitShaId']))
    print(_line)
    try:
        _status = os.popen("%s" % _line).read()
        if _status.find('ok') == -1:
            error_log(lf, _line, _status, "获取程序代码出错")
            sys.exit()
        write_log(lf, "获取程序代码成功")
    except:
        error_log(lf, _line, _status,"获取程序代码异常")
        sys.exit()
    # 移除准备上线代码目录
    _line = ("/bin/rm -rf data/%s%s" % (pi['deployName'], work_env))
    try:
        _status = os.system("%s" % _line) >> 8
        if int(_status) > 0 :
            error_log(lf, _line, _status, "删除上线目录出错")
            sys.exit()
        write_log(lf, "删除上线目录成功")
    except:
        error_log(lf, _line, _status, "删除上线目录异常")
        sys.exit()
    # 创建新的上线目录
    _line = ("/bin/mkdir -p data/%s%s" % (program_git_name, work_env))
    try:
        _status = os.system("%s" % _line) >> 8
        if int(_status) > 0 :
            error_log(lf, _line, _status, "创建上线目录出错")
            sys.exit()
        write_log(lf, "创建上线目录成功")
    except:
        error_log(lf, _line, _status, "创建上线目录异常")
        sys.exit()
    # 解压线上代码包
    _line = ("/usr/bin/unzip -q data/%s.zip -d data/%s%s" % (pi['deployName'], pi['deployName'], work_env))
    try:
        _status = os.system("%s" % _line) >> 8
        if int(_status) > 0 :
            error_log(lf, _line, _status, "解压上线代码包出错")
            sys.exit()
        write_log(lf, "解压上线代码成功")
    except:
        error_log(lf, _line, _status, "解压上线代码包异常")
        sys.exit()
    # 清理上压缩文件
    _line = ("/bin/rm -rf data/%s.zip" % (pi['deployName']))
    try:
        _status = os.system("%s" % _line) >> 8
        if int(_status) > 0 :
            error_log(lf, _line, _status, "清理上线代码压缩包出错")
            sys.exit()
        write_log(lf, "清理上线代码压缩包成功")
    except:
        error_log(lf, _line, _status, "清理上线代码压缩包异常")
        sys.exit()
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
                sys.exit()
            write_log(lf, "获取项目配置成功")
        except:
            #_line = ("python dogit.py -H%s -p%s -P%s/data/%s%s -g %s%s" %
            #         (git_ip, git_passwd, base_path, program_git_name, config_env, program_git_name, config_env))
            error_log(lf, _line, _status, "获取项目配置异常")
            sys.exit()
        # 线上配置解包
        _line = ("/usr/bin/unzip -q -o data/%s%s.zip -d %s/data/%s%s" %
                 (program_git_name, config_env, base_path, program_git_name, work_env))
        try:
            _status = os.system("%s" % _line) >> 8
            if int(_status) > 0 :
                error_log(lf, _line, _status, "解压线上配置出错")
                sys.exit()
            write_log(lf, "解压线上配置成功")
        except:
            error_log(lf, _line, _status, "解压线上配置异常")
            sys.exit()
        # 清理压缩包
        _line = ("/bin/rm -rf data/%s%s.zip" % (program_git_name, config_env))
        try:
            _status = os.system("%s" % _line) >> 8
            if int(_status) > 0 :
                error_log(lf, _line, _status, "清理线上配置包出错")
                sys.exit()
            write_log(lf, "清理线上配置包成功")
        except:
            error_log(lf, _line, _status, "清理线上配置包异常")
            sys.exit()



def run(proInfo, logFile):
    print(programPath)
    os.chdir('%s' % programPath)
    # 获取git
    getProjectGit(proInfo, logFile)
    print("ok")
