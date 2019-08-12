#!/bin/env python
# -*- coding:utf-8 -*-
# -------------------------------------------------
# Filename:    dogit.py
# Revision:    1.0
# Date:        2015-04-22
# Author:      simonzhang
# Email:       simon-zzm@163.com
# web:         www.simonzhang.net
# -------------------------------------------------
import os
import sys
import time

def now_time():
    from time import strftime
    return strftime('%Y-%m-%d %H:%M:%S')

# 创建新项目命令
def clone_git(argvs):
    import pexpect
    _line = "/usr/bin/git clone git@%s:%s %s" % \
            (argvs.HOST, argvs.PROGRAM, argvs.PATH)
    # 开始连接
    try:
        p = pexpect.spawn('%s' % _line)
        frist_step = p.expect(['Enter passphrase',
                               pexpect.EOF,
                               pexpect.TIMEOUT,
                               'delta 0'], timeout=120)
    except:
        return "error.连接git库失败%s" % _line
    # 判断是否需要输入密码
    if frist_step == 0:
        try:
            p.sendline("%s" % argvs.PASSWD)
            two_step = p.expect([pexpect.EOF,
                                 pexpect.TIMEOUT], timeout=600)
        except:
            return "error.clone 连接后输入密码异常。请检查连接git服务器。"
        # 输入密码完毕获取结束值
        if two_step == 1:
            return "error.clone 输入密码失败。请检查git账号配置。"
        elif two_step == 2:
            return "error.clone 输入密码部分超时。请检查git服务器和部署服务器之间网络。"
        else:
            return "ok.create program and git clone。"
    elif frist_step == 1:
        return "error.连接git服务器出错。请检查获取git库配置。"
    elif frist_step == 2:
        return "error.连接git服务器超时。请检查git服务器和部署服务器之间网络。"
    elif frist_step == 3:
        p.sendline("\n")
        return "ok.clone end"
    else:
        return "error.反正就是错了"


# 已有新项目获取新代码命令
def update_git(argvs):
    import pexpect
    try:
        os.chdir("%s" % argvs.PATH)
    except:
        return "error.切换到git目录错误"
    # 开始连接
    try:
        p = pexpect.spawn("/usr/bin/git pull")
        frist_step = p.expect(['Enter passphrase',
                               pexpect.EOF,
                               pexpect.TIMEOUT,'Already', 'done'], timeout=10)
    except:
        return "error.pull git库异常。"
    # 判断是否需要输入密码
    if frist_step == 0:
        try:
            p.sendline("%s" % argvs.PASSWD)
            two_step = p.expect([pexpect.EOF,
                                 pexpect.TIMEOUT], timeout=600)
        except:
            return "error.pull 连接后输入密码异常。请检查连接git服务器。"
        # 输入密码完毕获取结束值
        if two_step == 1:
            return "error.pull 输入密码失败。请检查git账号配置。"
        elif two_step == 2:
            return "errro.pull 输入密码部分超时。请检查git服务器和部署服务器之间网络。"
        else:
            return "ok.program pull"
    elif frist_step == 1:
        return "error.pull git服务器出错。请检查获取git库配置。"
    elif frist_step == 2:
        return "error.pull git服务器超时。请检查git服务器和部署服务器之间网络。"
    elif frist_step == 3 or frist_step == 4:
        return "ok.program pull"
    else:
        return "error.反正是错了。"

# 打包压缩出指定版本
def archive_git(argvs):
    _line = "cd %s ;/usr/bin/git archive -o ../%s.zip  %s" % \
                (argvs.PATH, argvs.PROGRAM, argvs.ID)
    # 开始连接
    try:
        p = os.popen("%s" % _line).read()
    except:
        return "error.安gitid打包异常。"
    if len(p) == 0:
        return "ok.archive to zip"
    else:
        return "error.按gitid打包错误:%s。" % p

# 直接用zip打包代码，不带版本信息。
def zip_git(argvs):
    _line = "cd %s;/usr/bin/zip -q -r ../%s.zip *" % \
               (argvs.PATH, argvs.PROGRAM)
    # 开始执行
    try:
        p = os.popen("%s" % _line).read()
    except:
        return "error.不带版本号打zip包异常"
    if len(p) == 0:
        return "ok.to zip"
    else:
        return "error.不带版本号打zip包错误信息:%s" % p

# 切换分支部分
def switch_branch(argvs):
    try:
        os.chdir("%s" % argvs.PATH)
    except:
        return "error.切换分支过程，切换到git目录错误%s" % argvs.PATH
    from string import strip
    _line = "cd %s;/usr/bin/git branch" % \
               (argvs.PATH)
    try:
        p = os.popen("%s" % _line).read()
    except:
        return "error.获取branch信息出错"
    getStatus = "error"
    for one in p.split('\n'):
        if one.find("*") > -1 and \
           strip(one).split(' ')[1] == "%s" % (argvs.BRANCH):
               getStatus = "ok"
    #如果不在分支则切换
    if getStatus == "error":
        _line = "cd %s;/usr/bin/git checkout %s" % \
                   (argvs.PATH, argvs.BRANCH)
        # 开始执行
        try:
            p = os.popen("%s" % _line).read()
        except:
            return "error.进入部署环境中的项目git目录异常。"
        if p.find("Branch") == 0 or len(p) == 0 or p.find("can be fast-forwarded") > -1:
            return "ok.checkout ok."
        else:
            return "error.切换主干或分支错误信息:%s" % p
    else: 
        return "ok.已经是该分支不用切换"

# 检查输入id是否存在，
def check_shaid(argvs):
    try:
        os.chdir("%s" % argvs.PATH)
    except:
        return "error.验证gitid，切换到git目录错误"
    _line = "cd %s;/usr/bin/git log -500 |grep commit|awk ' ''{print $2}'" % \
            (argvs.PATH)
    try:
        p = os.popen("%s" % _line).read()
    except:
        return "error.获取该项目全部gitid 异常"
    # 开始判断
    get_num = p.find("%s" % argvs.ID)
    if get_num > -1:
        _status =  "ok.sha id have"
    else:
        _status = "error.没有找到要部署的gitid。"
    return _status


def main():
    from optparse import OptionParser
    usage = "python dogit.py [-H] [-p] [-P] [-g] [-h] [-i] [-b]\
python dogit.py -Hx.x.x.x -pxxxx -P/home/git/deployData/app -g app -i git_id -b branch"
    parser = OptionParser(usage=usage)
    parser.add_option('-H', '--HOST',
                      help='git server is ip.',
                      action='store', dest='HOST')
    parser.add_option('-p', '--PASSWD',
                      default = "",
                      help='get git sshkey password',
                      action='store', dest='PASSWD')
    parser.add_option('-P', '--PATH',
                      #default="NUll",
                      help='the program save local path',
                      action='store', dest='PATH')
    parser.add_option('-g', '--PROGRAM',
                      #default="NUll",
                      help='the program name',
                      action='store', dest='PROGRAM')
    parser.add_option('-i', '--ID',
                      default="0",
                      help='the program git SHA-1',
                      action='store', dest='ID')
    parser.add_option('-b', '--branch',
                      default="master",
                      help='the program branch name',
                      action='store', dest='BRANCH')
    opts, args = parser.parse_args()

    if len(sys.argv) == 1:
        print('python dogit.py -h')
    elif type(opts.HOST) == type(None):
        print("must have git IP.")
    elif type(opts.PROGRAM) == type(None):
        print('must have program name')
    elif type(opts.PATH) == type(None):
        print('must have save local path')
    else:
        # 判断项目是否存在
        # 不存在调用创建，存在调用获取
        from os import path
        if not path.isdir(opts.PATH):
            get_v = clone_git(opts)
            if get_v.split('.')[0] == 'error':
                print(get_v.split('.')[1])
                sys.exit()
        # 如果branch name为空则切git master，不为空则切branch目录
        from string import strip
        if len(strip(opts.BRANCH)) == 0:
            opts.BRANCH = 'master'
        # 切换分支或主干
        get_v = switch_branch(opts)
        time.sleep(1)
        if get_v.split('.')[0] == 'error':
            print(get_v.split('.')[1])
            sys.exit()
        # 获取最新代码
        get_v = update_git(opts)
        time.sleep(1)
        if get_v.split('.')[0] == 'error':
            print(get_v.split('.')[1])
            sys.exit()
        # 是否有指定git id。有使用archive打包，没有用zip直接打所有文件包,剔除git版本库信息。
        # print "git id %s" % opts.ID
        if opts.ID == "0":
            get_v = zip_git(opts)
            if get_v.split('.')[0] == 'error':
                print(get_v.split('.')[1])
                sys.exit()
        else:
            # 判断项目中是否包含输入id,不包含则退出
            get_v = check_shaid(opts)
            if get_v.split('.')[0] == 'error':
                print(get_v.split('.')[1])
                sys.exit()
            # gitid存在开始按照gitid打包
            else:
                get_v = archive_git(opts)
                if get_v.split('.')[0] == 'error':
                    print(get_v.split('.')[1])
                    sys.exit()
                else:
                    print("ok.更新完成")
        sys.exit()


if __name__ == "__main__":
    main()
