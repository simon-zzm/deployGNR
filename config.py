#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author:      simonzhang
# web:         www.simonzhang.net
# Email:       simon-zzm@163.com
### END INIT INFO
import os

# 监听部分
listenIp = '182.92.186.219'
listenPort = 9988
domainName = 'http://182.92.186.219:9988'
title = 'deployGNR'

# 当前路径
programPath = "%s/" % os.getcwd()

# 图片存储路径(不建议与项目放到一个目录里)
imgRootPath = "/program/img/"

# 日志保存路径
logsRootPath = "/home/git/deployGNR/deployGNR/logs/"

# 调试模式为True。代码错误会打印到浏览器上，代码修改后立即生效
# 运行模式为False。执行速度快，但是代码修改后需要重启服务。
debugMode = True

# cookie 安全 key
cookieKey = 'if38u2g4i898#439#yg439h8g9438hy4g93'
# cookie 超时(天)
cookieTimeoutDays = 3
# session超时时间，写入redis中，单位为秒
sessionTimeout = 60*60*24*3
# passkey 本地存储密码加解密使用
passKey = b'H7pFRBEdYmIwy6g3vlDq8VZzidfWpYpdyxzk0x9_wNc='

# 系统全局设置
settings = {
    "cookie_secret": cookieKey,
    "xsrf_cookies":True,
    "login_url": "/",
    "template_path":os.path.join(os.path.dirname(__file__), "templates"),
    "static_path":os.path.join(os.path.dirname(__file__), "static"),
    "debug":debugMode,
}

# SSL部分，实现https
# 将私钥和签名文件放到项目跟目录下即可
# 如果不需要此项为空
crtFile = '' 
keyFile = ''

# mysql
# 单个数据库信息格式为：IP 端口 账号 密码 库名 时区 模式(默认为严格模式)
# 多个库以列表形势配置
MySqlWriteInfo = [['127.0.0.1', 3306, 'deployGNR', 'deploy8675', 'deployGNR', '+8:00'],]
MySqlReadInfo = [['127.0.0.1', 3306, 'deployGNR', 'deploy8675', 'deployGNR', '+8:00'],]
poolsDEBUG = True

# redis 数据超时时间为7天。socket超时单位秒
redisIp = "10.171.53.171"
redisPort = "6379"
redisDB = 3
redisSocketTimeout = 3.0
redisSocketConnTimeout = 1.5
reidsTimeout = 60*60*24*3

# 异步默认线程数
sendDefaultThreadLoops = 20

# 如果要记录日志，需要使用toWrite返回数据
# 慢日志
# 当前接口超时n秒后记录慢日志
# 慢日志默认位置在logs目录下，文件名为slow.log(未测试)
slowTimeout = 2

# 记录详细日志(默认关闭,会出现按IO阻塞问题)
# true为开启，False为关闭
# 文件名detailedLog.log
# 日志格式:请求时间 远程ip 返回耗时 请求地址 请求协议 请求模式 请求路径 浏览器信息
logStatus = True

# 日志路径(不建议与项目放到一个目录里)
logPath = './logs/'

# 黑白名单那设置
# 格式为['192.168.1.1', '192.168.1.2']
# 如果为'0.0.0.0'为所有
blackList = []
whiteList = []

# 每秒中可以访问的次数（未实现）
secondRate = 0

# 防SQL注入关键字。只在modules.py中使用。
sqlInjData = ["'", 'and', 'or', 'exec', 'insert', 
              'select', 'delete', 'update', 'count', 
              'chr', 'mid', 'master', 'truncate', 'char', 
              'declare', '=', '{', '}', '\\', 
              ';', '<', '>', '?', ',', '`', '~', 
              '!', '$', '*', '%', '^', '(', ')', 
              'script']

# git服务器配置
gitRootPath = "/home/git/gitosis-admin/"
# git存放位置
gitKeyPath = gitRootPath+'keydir/'
# git管理用户
gitManName = "git@iZ25jrz67c4Z"
# 系统管理账号ID和组ID
gitSYSAuth = "9990.9990"
# git库存放位置
gitLocalPath = "/home/git/gitroot/"
