#!env python3
# -*- coding:utf-8 -*-
# -------------------------------------------------
# Filename:  
# Revision:    1.0
# Date:        2015-04-22
# Author:      simonzhang
# Email:       simon-zzm@163.com
# web:         www.simonzhang.net
# -------------------------------------------------
import os
import sys
import sys
import uuid
sys.path.append('..')
from config import *

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

def main(deploy_log_file, program_git_name, online_project_name, work_env, \
             config_env, service_rsync_info, git_sha_id, branch_name):
    os.chdir('%s' % base_path)
    # 开始同步项目git代码
    if len(branch_name) >1:
        _line = ("python dogit.py -H%s -p%s -P%s/data/%s -g %s -i %s -b %s" %
                (git_ip, git_passwd, base_path, program_git_name, program_git_name, git_sha_id, branch_name))
    else:
        _line = ("python dogit.py -H%s -p%s -P%s/data/%s -g %s -i %s " %
                (git_ip, git_passwd, base_path, program_git_name, program_git_name, git_sha_id))
    #print _line
    try:
        _status = os.popen("%s" % _line).read()
        if _status.find('ok') == -1:
            error_log(deploy_log_file, _line, _status, "获取程序代码出错")
            sys.exit()
        write_log(deploy_log_file, "获取程序代码成功")
    except:
        error_log(deploy_log_file, _line, _status,"获取程序代码异常")
        sys.exit()
    # 移除准备上线代码目录
    _line = ("/bin/rm -rf data/%s%s" % (program_git_name, work_env))
    try:
        _status = os.system("%s" % _line) >> 8
        if int(_status) > 0 :
            error_log(deploy_log_file, _line, _status, "删除上线目录出错")
            sys.exit()
        write_log(deploy_log_file, "删除上线目录成功")
    except:
        error_log(deploy_log_file, _line, _status, "删除上线目录异常")
        sys.exit()
    # 创建新的上线目录
    _line = ("/bin/mkdir -p data/%s%s" % (program_git_name, work_env))
    try:
        _status = os.system("%s" % _line) >> 8
        if int(_status) > 0 :
            error_log(deploy_log_file, _line, _status, "创建上线目录出错")
            sys.exit()
        write_log(deploy_log_file, "创建上线目录成功")
    except:
        error_log(deploy_log_file, _line, _status, "创建上线目录异常")
        sys.exit()
    # 解压线上代码包
    _line = ("/usr/bin/unzip -q data/%s.zip -d data/%s%s" % (program_git_name, program_git_name, work_env))
    try:
        _status = os.system("%s" % _line) >> 8
        if int(_status) > 0 :
            error_log(deploy_log_file, _line, _status, "解压上线代码包出错")
            sys.exit()
        write_log(deploy_log_file, "解压上线代码成功")
    except:
        error_log(deploy_log_file, _line, _status, "解压上线代码包异常")
        sys.exit()
    # 清理上压缩文件
    _line = ("/bin/rm -rf data/%s.zip" % (program_git_name))
    try:
        _status = os.system("%s" % _line) >> 8
        if int(_status) > 0 :
            error_log(deploy_log_file, _line, _status, "清理上线代码压缩包出错")
            sys.exit()
        write_log(deploy_log_file, "清理上线代码压缩包成功")
    except:
        error_log(deploy_log_file, _line, _status, "清理上线代码压缩包异常")
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
                error_log(deploy_log_file, _line, _status, "获取项目配置出错")
                sys.exit()
            write_log(deploy_log_file, "获取项目配置成功")
        except:
            #_line = ("python dogit.py -H%s -p%s -P%s/data/%s%s -g %s%s" %
            #         (git_ip, git_passwd, base_path, program_git_name, config_env, program_git_name, config_env))
            error_log(deploy_log_file, _line, _status, "获取项目配置异常")
            sys.exit()
        # 线上配置解包
        _line = ("/usr/bin/unzip -q -o data/%s%s.zip -d %s/data/%s%s" %
                 (program_git_name, config_env, base_path, program_git_name, work_env))
        try:
            _status = os.system("%s" % _line) >> 8
            if int(_status) > 0 :
                error_log(deploy_log_file, _line, _status, "解压线上配置出错")
                sys.exit()
            write_log(deploy_log_file, "解压线上配置成功")
        except:
            error_log(deploy_log_file, _line, _status, "解压线上配置异常")
            sys.exit()
        # 清理压缩包
        _line = ("/bin/rm -rf data/%s%s.zip" % (program_git_name, config_env))
        try:
            _status = os.system("%s" % _line) >> 8
            if int(_status) > 0 :
                error_log(deploy_log_file, _line, _status, "清理线上配置包出错")
                sys.exit()
            write_log(deploy_log_file, "清理线上配置包成功")
        except:
            error_log(deploy_log_file, _line, _status, "清理线上配置包异常")
            sys.exit()
    # 开始同步代码
    #python dorsync.py  -H 192.168.1.17 -d1978 -P $base_path/data/$project_name$work_env/ -g $online_project_name
    #python dorsync.py  -H 192.168.1.17 -d1978 -P $base_path/data/$project_name$work_env/ -e 'apllication/controllers/test' -g $online_project_name
    for rsync_info in service_rsync_info:
        # 拼接命令行
        if len(rsync_info[2]) == 0:
            _line = ("python dorsync.py  -H %s -d %s -P %s/data/%s%s/ -g %s" %
                      (rsync_info[0], rsync_info[1], base_path, program_git_name, work_env, rsync_info[3]))
        else:
            _line = ("python dorsync.py  -H %s -d %s -P %s/data/%s%s/ -e '%s' -g %s" %
                      (rsync_info[0], rsync_info[1], base_path, program_git_name, work_env, rsync_info[2], rsync_info[3]))
        # 执行命令
        rsync_status = 0
        try:
            get_status = os.popen("%s" % _line).read()
            if get_status.find('ok') == -1 :
                error_log(deploy_log_file, _line, _status, "同步到%s出错" % rsync_info[0])
                rsync_status = 1
            else:
                write_log(deploy_log_file, "同步到%s成功" % rsync_info[0])
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
                    write_log(deploy_log_file, "同步版本文件到%s成功" % rsync_info[0])
        except:
            error_log(deploy_log_file, _line, _status, "同步到%s异常" % rsync_info[0])
            rsync_status = 1
    # 记录rsync状态日志
    if rsync_status == 0:
        write_log(deploy_log_file, "本次上线完成。全部成功。")
    else:
        write_log(deploy_log_file, "本次上线完成。有部分错误，请详查日志。")
    # 展示所有日志
    log_file = open("%s" % deploy_log_file, "rb").read()
    return log_file

if __name__ == "__main__":
    argv_status = "T"
    # 日志名称
    try:
        deploy_log_file = "%s.log" % sys.argv[7]
    except:
        deploy_log_file = "system.log"
        write_log(deploy_log_file, "获取日志文件名异常")
        argv_status = "F"
    try:
        # git name
        program_git_name = sys.argv[1].strip()
        # program name
        online_project_name = sys.argv[2].strip()
        # "Test" "Pro" "Preview"
        work_env = sys.argv[3].strip()
        #"ConfTest" "ConfPro" "ConfPreview"
        config_env = sys.argv[4].strip()
        # 上线信息列表，单服务器格式['rsync ip', 'rsync 端口'，'排除设置'，'rsync服务名称']
        # 排除部分如有多处用文件或目录|隔开即可,如果没有则为空
        _rsync_info = sys.argv[5].strip()
        service_rsync_info = str_to_list(_rsync_info)
        #get_id
        git_sha_id = sys.argv[6].stip()
        # branch
        branch_name = sys.argv[8].stip()
    except:
        write_log(deploy_log_file, "获得执行参数信息异常")
        argv_status = "F"
    if argv_status == "T":
        main(deploy_log_file, program_git_name, online_project_name, work_env, \
             config_env, service_rsync_info, git_sha_id, branch_name)
    else:
        pass
    sys.exit()
