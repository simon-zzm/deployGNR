#!/usr/bin/python3 
# -*- coding:utf-8 -*-
# Author:      simonzhang
# web:         www.simonzhang.net
# Email:       simon-zzm@163.com
### END INIT INFO
import tornado.ioloop
import tornado.web

import os
import sys
import time
import uuid
from io import StringIO
from PIL import Image
from config import *

#### 全局模块部分
# 基础认证
def auth(method):
    def checkUser(self, *args, **kwargs):
        try:
            getUserInfo = self.get_secure_cookie("userInfo").decode()
            getNowUser = getUserInfo.split(",")[0]
            getSessionId = getUserInfo.split(',')[2]
        except:
            getNowUser = ""
            getSessionId = ""
        # 检查是否在redis中
        try:
            if redisDB.get("%s" % getSessionId).decode() == getNowUser:
                return method(self, *args, **kwargs)
            else:
                self.clear_all_cookies()
                self.redirect("/")
                redisDB.delete("%s" % getSessionId)
        except:
            self.clear_all_cookies()
            self.redirect("/")
            redisDB.delete("%s" % getSessionId)
    return checkUser

# 基础信息。包含title,username,domainname,column
def htmlBaseInfo(method):
    def getBaseInfo(self, *args, **kwargs):
        getUserName, getNickName = getName(self)
        getColumnCode = "%s" % creatColumnCode(getUserName)
        self.baseInfo = {'title':title, 'username':getNickName, \
                         'domain':domainName, 'columnCode':getColumnCode, \
                         'getUserName':getUserName, 'getNickName':getNickName}
        return method(self, *args, **kwargs)
    return getBaseInfo
        
# 通过cookie获取用户信息
def getName(self):
    try:
        getUserInfo = self.get_secure_cookie("userInfo").decode()
        getUserName = getUserInfo.split(",")[0]
        getNickName = getUserInfo.split(",")[3]
    except:
        self.clear_all_cookies()
        self.redirect("/")
        return 
    if len(getNickName) == 0 or str(getNickName) == 'None':
        getNickName = getUserName
    return getUserName, getNickName


#### 检查请求url
def checkUrl(method):
    '''
    当前包含检查有
    sql注入
    黑白名单
    '''
    def toCheck(self, *args, **kwargs):
        tmpRes = checkIP(self)
        if len(tmpRes) > 0:
            self.write(tmpRes)
            return 
        tmpRes = sqlInj(self)
        if len(tmpRes) > 0:
            self.write(tmpRes)
            return 
        else:
            return method(self, *args, **kwargs)
    return toCheck

#### 获得远程IP
def getClentIp(tmp):
    try:
        getUserIP = tmp.request.remote_ip
    except:
        getUserIP = "Null"
    try:
        getRealIP = tmp.request.headers["X-Real-Ip"]
    except:
        getRealIP = "Null"
    return getRealIP, getUserIP

#### 检查IP
def checkIP(self):
    response = ''
    getRealIP, getUserIP = getClentIp(self)
    if (getRealIP in whiteList) and (getUserIP in whiteList):
        return response
    elif getRealIP in blackList or '0.0.0.0' in blackList or \
         getUserIP in blackList:
        return '{"code":"922""}'
    else:
        return response

#### 防sql注入
def sqlInj(self):
    response = ''
    try:
        allArgs = self.request.arguments
        for one in allArgs:
            # 不检查安全cookie
            if one == '_xsrf':
                continue
            # 获取参数转小写
            tmpArg = self.get_argument(one).lower()
            # 去空格
            tmpArg = tmpArg.replace(' ', '')
            # 检查是否有注入字符串
            for singleInj in sqlInjData:
                if tmpArg.find(singleInj) > -1:
                    # 处理结果
                    response = '{"code":"921"}'
                    return response
    except:
        response = '{"code":"920"}'
    return response

# 查看提交权限
def checkAuth(userName, submitId):
    userId = rdbUserInfo(userName)['id']
    return int(sqlcomm('select count(id) as c from d_group_submit as xgs where group_id in ( \
                  select group_id from d_group_user where user_id=%s \
                 ) and xgs.submit_id =%s' % (userId, submitId))[0]['c'])

# 将MySQL的数据转为json
def mysqltojson(getList):
    import json
    _createStr = []
    # 循环所有数据字典
    for l in getList:
        # 循环转换所有数据
        _createTmpDict = {}
        for o in l.keys():
            _createTmpDict[o] = l[o]
        _createStr.append(_createTmpDict)
    return json.dumps(_createStr, ensure_ascii=False)


# 加密、解密、创建密码
from werkzeug.security import generate_password_hash, check_password_hash
def toPasswd(passstr):
    return  generate_password_hash("%s" % passstr)

def checkPasswd(passwd, passstr):
    return check_password_hash("%s" % passstr,"%s" % passwd)

def createPasswd():
    import random
    return random.randint(100000, 999999)

#### 获取当时间
# 格式化为 年月日 小时分秒
def getNowTimef6():
    return time.strftime('%Y-%m-%d %T',time.localtime(time.time()))

# 格式化为 年月日
def getNowTimef3():
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))

# 格式化为 小时分秒
def getNowTimeb3():
    return time.strftime('%T',time.localtime(time.time()))

# unixtime int
def getNowUnixTimeInt():
    return int(time.mktime(time.localtime()))

# 判断返回数据速度，记录慢日志
def toWrite(self, context):
    #只判断单位为秒
    useTime = int(self.request.request_time())
    if slowTimeout < useTime:
        slowLog = open("%sslow.log" % logPath, "ab")
        slowLog.write("%s %s %s\n" % (getNowTime(), useTime, self.request.uri))
        slowLog.close()
    if logStatus :
        nowTime = getNowTime()
        getIP = self.request.remote_ip
        getUri = self.request.uri
        getAgent = self.request.headers['User-Agent']
        getHost = self.request.host
        getProtocol =self.request.protocol
        getMethod = self.request.method
        log = open('%sdetailedLog%s.log' % (logPath, nowTime.split()[0]), "ab")
        log.write('%s %s %s %s %s %s %s "%s"\n' % (nowTime, getIP, useTime,
                                                   getHost, getProtocol, 
                                                   getMethod, getUri, getAgent))
        log.close()
    self.write(context)

# 系统日志通用
def wlog(fname, context):
    nowTime = getNowTime()
    try:
        log = open('%s%s-%s.log' % (logPath, fname, nowTime.split()[0]), "ab")
        log.write('%s  %s\n' % (nowTime, context))
        log.close()
    except:
        pass


#### 数据库部分
import pymysql
# 读
def rDB():
    rdbInfo = MySqlReadInfo[0]
    rdb = pymysql.connect(host = rdbInfo[0], port = rdbInfo[1], \
                                      db = rdbInfo[4], \
                                      user = rdbInfo[2], \
                                      passwd = rdbInfo[3], charset = 'utf8')
    return rdb

# 写
def wDB():
    wdbInfo = MySqlWriteInfo[0]
    wdb = pymysql.connect(host = wdbInfo[0], port = wdbInfo[1], \
                                      db = wdbInfo[4], \
                                      user = wdbInfo[2], \
                                      passwd = wdbInfo[3], charset = 'utf8')
    return wdb


# 执行sql，并简单判断返回值类型。
# 如果是插入、更新、删除返回值为执行的id
def sqlcomm(sql):
    if sql.split()[0].lower() != "select":
        try:
            wdb = wDB()
            cursor = wdb.cursor(cursor=pymysql.cursors.DictCursor)
            data = cursor.execute(sql)
            wdb.commit()
            cursor.close()
            wdb.close()
        except:
            wdb.rollback()
    else:
        try:
            rdb = rDB()
            cursor = rdb.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.close()
            rdb.close()
        except:
            rdb.rollback()
    return data

#### redis
import redis
redisDB = redis.StrictRedis(host = redisIp, \
                            port = redisPort, \
                            db = redisDB, \
                            socket_timeout = redisSocketTimeout, \
                            socket_connect_timeout = redisSocketConnTimeout)
#redis_db.setex("key", redis_timeout, "valuse")
#redis_db.get("key")

#### 系统部分
class BaseErrorHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        self.writeError(status_code, **kwargs)
    
    def writeError(self, statusCode, **kwargs):
        if statusCode == 405:
            self.write('{"code":"960"}')
        else:
            self.write('{"code":"'+str(statusCode)+'"}')

#### 生成左侧菜单代码
from dbmodules import rdbUserInfo, rdbUserColumn
def creatColumnCode(userName):
    userId = rdbUserInfo(userName)['id']
    #
    getColumnData = rdbUserColumn(userId)
    columnCode = ''
    colName = []
    secColnum = ''
    for oneData in getColumnData:
        code1 = '''
                    <li>
                        <a href="#%s%s" class="nav-header collapsed" data-toggle="collapse">
                ''' % (oneData['id1'], oneData['pid1'])
        code2 = '''
                               <span class="pull-right glyphicon glyphicon-chevron-down"></span>
                        </a>
                '''
        code3 = '''
                        <ul id="%s%s" class="nav nav-list collapse secondmenu" style="height: 0px;">
                ''' % (oneData['id1'], oneData['pid1'])
        if len(columnCode) == 0:
            colName.append("%s" % oneData['name1'])
            columnCode = "%s" % code1
            columnCode = '%s%s%s' % (columnCode, oneData['name1'], code2)
            try:
                nameLen = len(oneData['name2'])
            except:
                nameLen = 0
            if nameLen > 0:
                columnCode = '%s%s' % (columnCode, code3)
                secColnum = '%s<li><a href="%s/index/%s/">%s</a></li>' % (secColnum, domainName, oneData['code2'], oneData['name2'])
            else:
                columnCode = '%s\n                      </li>' % (columnCode)
        elif oneData['name1'] in colName:
            secColnum = '%s<li><a href="%s/index/%s/">%s</a></li>' % (secColnum, domainName, oneData['code2'], oneData['name2'])
        else:
            colName.append("%s" % oneData['name1'])
            if len(secColnum) == 0:
                columnCode = '%s%s   </li>%s%s%s' % (columnCode, secColnum, code1, oneData['name1'], code2)
            else:
                columnCode = '%s%s   </ul></li>%s%s%s' % (columnCode, secColnum, code1, oneData['name1'], code2)
            secColnum = ''
            try:
                nameLen = len(oneData['name2'])
            except:
                nameLen = 0
            if nameLen > 0:
                columnCode = '%s%s' % (columnCode, code3)
                secColnum = '%s<li><a href="%s/index/%s/">%s</a></li>' % (secColnum, domainName, oneData['code2'], oneData['name2'])
    if len(secColnum) == 0:
        columnCode = '%s   </li>' % (columnCode)
    else:
        columnCode = '%s%s   </ul></li>' % (columnCode, secColnum)
    return columnCode
