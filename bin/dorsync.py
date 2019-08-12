#!/bin/env python
# -*- coding:utf-8 -*-
# -------------------------------------------------
# Filename:    dorsync.py
# Revision:    1.0
# Date:        2015-04-22
# Author:      simonzhang
# Email:       simon-zzm@163.com
# web:         www.simonzhang.net
# -------------------------------------------------
import os
import sys

def now_time():
    from time import strftime
    return strftime('%Y-%m-%d %H:%M:%S')

# rsync src
def rsync(argvs):
    _line = "rsync -avz --delete --exclude '/README.TXT' --exclude '.git/' %s \
            %s rsync://%s:%s/%s" % \
            (argvs.EXC, argvs.PATH, argvs.HOST, argvs.PORT, argvs.PROGRAM)
    # 开始连接
    try:
        p = os.popen("%s" % _line).read()
    except:
        return "error.rsync 命令 %s。异常错误信息:%s。" % (_line, p)
    # 判断是否成功
    if len(p) > 0 and p.find("total size") > 0:
        return "ok.rsync"
    else:
        return "error.rsync 命令 %s。出错错误信息:%s。" % (_line, p)


def main():
    from optparse import OptionParser
    usage = "python dorsync.py [-H] [-d] [-p] [-P] [-g] [-e] [-h] \
python dorsync.py  -H x.x.x.x -d 1978 -P /home/git/deployData/app -e 'data/|log/' -g app"
    parser = OptionParser(usage=usage)
    parser.add_option('-H', '--HOST',
                      help='resync server is ip.',
                      action='store', dest='HOST')
    parser.add_option('-d', '--PORT',
                      default = "1979",
                      help='get rsync server port',
                      action='store', dest='PORT')
    parser.add_option('-p', '--PASSWD',
                      default = "",
                      help='get rsync sshkey password',
                      action='store', dest='PASSWD')
    parser.add_option('-P', '--PATH',
                      #default="NUll",
                      help='the program save local path',
                      action='store', dest='PATH')
    parser.add_option('-g', '--PROGRAM',
                      #default="NUll",
                      help='the program name',
                      action='store', dest='PROGRAM')
    parser.add_option('-e', '--EXCLUDE',
                      default="",
                      help='the program exclude file or dir',
                      action='store', dest='EXC')
    opts, args = parser.parse_args()

    if len(sys.argv) == 1:
        print('python dorsync.py -h')
    elif type(opts.HOST) == type(None):
        print("must have rsync server IP.")
    elif type(opts.PROGRAM) == type(None):
        print('must have program name')
    elif type(opts.PATH) == type(None):
        print('must have save local path')
    else:
        # 如果有需要需要过滤的则进行拼写语句
        exc_line = ""
        if len(opts.EXC) > 1:
            for ll in opts.EXC.split('|'):
                exc_line = "%s --exclude '%s'" % (exc_line, ll)
            opts.EXC = exc_line
        # 不存在则报错
        from os import path
        if path.isdir(opts.PATH):
            get_v = rsync(opts)
            if get_v.split('.')[0] == 'error':
                    print(get_v.split('.')[1])
                    sys.exit()
            else:
                print("ok.rsync同步正常。")
        else:
            print("本地不存在要rsync的部署目录。")

if __name__ == "__main__":
    main()
    sys.exit()
