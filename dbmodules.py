#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author:      simonzhang
# web:         www.simonzhang.net
# Email:       simon-zzm@163.com
### END INIT INFO
from modules import sqlcomm

#### 系统通用
# 获得用户信息
def rdbUserInfo(userName):
    try:
        sql = "select id,name, nick_name, passwd,email, phone_num from d_user where name='%s'" % userName
        data = sqlcomm(sql)[0]
    except:
        data = {}
    return data

# 获得用户菜单
def rdbUserColumn(userId):
    sql = 'select xc2.id as id1, xc2.name as name1, xc2.code as code1, xc2.parent_id as pid1, \
  xc1.name as name2, xc1.code as code2 from ( \
         select id,name,code,parent_id,sort_no from d_column where id in ( \
                select column_id from d_group_column as gr where group_id in( \
                  select group_id from d_group_user where user_id=%s \
                 ) \
    ) and parent_id <>0 ORDER BY parent_id,sort_no \
) as xc1 \
left join d_column as xc2 on xc1.parent_id=xc2.id ' % userId
    data = sqlcomm(sql)
    return data


#### 系统管理->用户信息 userSelf.py
def rdbUserSelf(userName):
    try:
        sql = "select name,nick_name,email, phone_num from d_user where name='%s'" % userName
        data = sqlcomm(sql)[0]
    except:
        data = {}
    return data

#### 系统管理->用户信息 userSelf.py
def wdbUserSelf(getUserName, getNickName, getEmail, getPhonenum):
    try:
        sql = "UPDATE d_user set nick_name='%s', email='%s', phone_num=%s where name='%s'" % \
                  (getNickName, getEmail, getPhonenum, getUserName)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### 系统管理->修改个人密码 userEditPass.py
def wdbChangMePass(newPasswd, getUserName):
    try:
        sql = "UPDATE d_user set passwd='%s' where name='%s'" % \
                  (newPasswd, getUserName)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### 系统管理->用户管理 userMan.py
def rdbAllUserName():
    try:
        sql = "select name from d_user"
        data = sqlcomm(sql)
    except:
        data = {}
    return data

#### 系统管理->用户管理 userMan.py
def rdbUserName():
    try:
        sql = "select name from d_user where passwd != ''"
        data = sqlcomm(sql)
    except:
        data = {}
    return data

#### 系统管理->用户管理 userMan.py 
def wdbChangUserPass(getUserName, getPasswd):
    try:
        sql = "UPDATE d_user set passwd='%s' where name='%s'" % \
                  (getPasswd, getUserName)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### 系统管理->用户管理 userMan.py
def rdbUserNameHave(getUserName):
    try:
        sql = "select count(id) as c from d_user where name='%s'" % \
                  (getUserName)
        data = sqlcomm(sql)
    except:
        data = {}
    return data

#### 系统管理->用户管理 userMan.py
def wdbInsertUser(getUserName, getPasswd):
    try:
        sql = "INSERT INTO d_user(name, nick_name, passwd) VALUE('%s', '%s', '%s')" % \
                  (getUserName, getUserName, getPasswd)
        print(sql)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### 系统管理->用户管理 userMan.py
def wdbDelUser(getUserName):
    try:
        sql = "update d_user set passwd='' where name='%s'" % \
                  (getUserName)
        data = sqlcomm(sql)
        
    except:
        data = 0
    return data

def wdbDelUserAuth(getUserName):
    try:
        sql = "DELETE d_group_user where user_id = \
              (select id from d_user where name='admin')" % (getUserName)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### 系统管理->用户组管理 groupMan.py
def rdbAllGroup():
    try:
        sql = "select id,group_name,mark from d_group"
        data = sqlcomm(sql)
    except:
        data = {}
    return data

#### 系统管理->用户管理 userMan.py 
def rdbUserHaveGroup(getUserName):
    try:
        sql = "select id, group_name from d_group where id in ( \
                   select group_id from d_group_user where user_id = \
                   (select id from d_user where name='%s'))" % getUserName
        data = sqlcomm(sql)
    except:
        data = {}
    return data

#### 系统管理->用户管理 userMan.py
def wdbDelUserGroup(getUserName):
    try:
        sql = "delete from d_group_user where user_id = \
               (select id from d_user where name='%s')" % getUserName
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### 系统管理->用户管理 userMan.py
def wdbAddUserGroup(getUserName, gid):
    try:
        sql = "INSERT d_group_user(group_id, user_id) \
                  value(%s, (select id from d_user where name='%s'))" % (gid, getUserName)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### 系统管理->用户组管理 groupMan.py
def rdbGroupNameHave(getGroupName):
    try:
        sql = "select count(id) as c from d_group where group_name='%s'" % (getGroupName)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### 系统管理->用户组管理 groupMan.py
def wdbInsertGroup(getGroupName, groupMark):
    try:
        sql = "INSERT d_group(group_name, mark) value('%s', '%s')" % (getGroupName, groupMark)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### 系统管理->用户组管理 groupMan.py
def rdbGroupHaveUseAuth(getGroupId):
    try:
        sql = "select submit_id,submit_local from d_submit where submit_id in( \
select submit_id from d_group_submit where group_id = %s)" % getGroupId
        data = sqlcomm(sql)
    except:
        data = {}
    return data

#### 系统管理->用户组管理 groupMan.py
def rdbAllSubmit():
    try:
        sql = "select submit_id,submit_local from d_submit"
        data = sqlcomm(sql)
    except:
        data = {}
    return data

#### 系统管理->用户组管理 groupMan.py
def wdbDelGroupUseAuth(getGroupId):
    try:
        sql = "delete from d_group_submit where group_id=%s" % getGroupId
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### 系统管理->用户组管理 groupMan.py
def wdbAddGroupUseAuth(getGroupId, oneSubId):
    try:
        sql = "INSERT d_group_submit(group_id, submit_id) \
                  value(%s, %s)" % (getGroupId, oneSubId)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### 系统管理->用户组管理 groupMan.py
def rdbGroupHaveUseCol(getGroupId):
    try:
        sql = "select xc2.id as id1, xc1.id as id2, xc1.name as name2 from ( \
         select id,name,code,parent_id,sort_no from d_column where id in ( \
                select column_id from d_group_column as gr where group_id =%s \
    ) and parent_id <>0 ORDER BY parent_id,sort_no \
) as xc1 \
left join d_column as xc2 on xc1.parent_id=xc2.id" % getGroupId
        data = sqlcomm(sql)
    except:
        data = {}
    return data

#### 系统管理->用户组管理 groupMan.py
def rdbAllColumn():
    try:
        sql = "select xc2.id as id1, xc1.id as id2, xc1.name as name2 from ( \
         select id,name,code,parent_id,sort_no from d_column \
    where parent_id <>0 ORDER BY parent_id,sort_no \
) as xc1 \
left join d_column as xc2 on xc1.parent_id=xc2.id"
        data = sqlcomm(sql)
    except:
        data = {}
    return data

#### 系统管理->用户组管理 groupMan.py
def wdbDelGroupUseCol(getGroupId):
    try:
        sql = "delete from d_group_column where group_id=%s" % getGroupId
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### 系统管理->用户组管理 groupMan.py
def wdbAddGroupUseCol(getGroupId, oneColId):
    try:
        sql = "INSERT d_group_column(group_id, column_id) \
                  value(%s, %s)" % (getGroupId, oneColId)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### git管理->git项目管理 gitProjectMan.py
def rdbAllGitProject():
    try:
        sql = "select id,gitProjectName,gitUrl from d_git_project"
        data = sqlcomm(sql)
    except:
        data = {}
    return data

#### git管理->git项目管理 gitProjectMan.py
def rdbGitProjectNameCount(gitProjectName):
    try:
        sql = "select count(id) as c from d_git_project where gitProjectName ='%s'" % (gitProjectName)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### git管理->git项目管理 gitProjectMan.py
def wdbGitProjectNameCreate(gitName, gitUrl):
    try:
        sql = "INSERT d_git_project(gitProjectName, gitUrl) \
                  value('%s', '%s')" % (gitName, gitUrl)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### git管理->git项目管理 gitProjectMan.py
def wdbGitProjectUrlChange(gitId, gitUrl):
    try:
        sql = "UPDATE d_git_project set gitUrl='%s' where id='%s'" \
                % (gitUrl, gitId)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### git管理->git用户管理 gitUserMan.py
def rdbGitUserNameCount(gitUserName):
    try:
        sql = "select count(id) as c from d_git_user where gitUser ='%s'" % (gitUserName)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### git管理->git用户管理 gitUserMan.py
def wdbGitUserNameCreate(gitUserName, gitKeyFileName):
    try:
        sql = "INSERT d_git_user(gitUser, keyFile) \
                  value('%s', '%s')" % (gitUserName, gitKeyFileName)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### git管理->git用户管理 gitUserMan.py
def wdbGitUserKeyChange(gitUserName, keyFile):
    try:
        sql = "UPDATE d_git_user set keyFile='%s' where gitUser='%s'" % (keyFile, gitUserName)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### git管理->git用户管理 gitUserMan.py
def wdbGitUserStop(gitUserName):
    try:
        sql = "UPDATE d_git_user set status=1 where gitUser='%s'" % (gitUserName)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### git管理->git权限管理 gitAuthMan.py
def rdbAllGitUser():
    try:
        sql = "select id,gitUser from d_git_user where status=0"
        data = sqlcomm(sql)
    except:
        data = {}
    return data

#### git管理->git权限管理 gitAuthMan.py
def rdbUserHaveGitProject(gitProId):
    try:
        sql = "select gitUserId from d_git_project_user where gitProjectId in ( \
select id from  d_git_project where id=%s) " % gitProId
        data = sqlcomm(sql)
    except:
        data = {}
    return data

#### git管理->git权限管理 gitAuthMan.py
def wdbProjectGitDisUser(gitProjectId, gitUserId):
    try:
        sql = "INSERT d_git_project_user(gitUserId, gitProjectId) \
                  value('%s', '%s')" % (gitUserId, gitProjectId)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### git管理->git权限管理 gitAuthMan.py
def rdbProjectHaveGitUser(getGitUserId):
    try:
        sql = "select gitProjectId from d_git_project_user where gitUserId in ( \
select id from  d_git_user where id=%s and status=0)" % (getGitUserId)
        data = sqlcomm(sql)
    except:
        data = {}
    return data

#### git管理->git权限管理 gitAuthMan.py
def wdbDelGitProjectUser(gitProjectId):
    try:
        sql = "delete from d_git_project_user where gitProjectId = %s" % (gitProjectId)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### git管理->git权限管理 gitAuthMan.py
def wdbDelGitUserProject(gitUserId):
    try:
        sql = "delete from d_git_project_user where gitUserId = %s" % (gitUserId)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### git管理->git权限管理 gitAuthMan.py
def rdbGitProjectHaveGitUser(gitProjectId):
    try:
        sql = "select gitUser from d_git_user where id in ( \
select gitUserId from d_git_project_user where gitProjectId=%s) and status=0" % gitProjectId
        data = sqlcomm(sql)
    except:
        data = {}
    return data

#### git管理->git权限管理 gitAuthMan.py
def rdbGitProIdCount(gitProjectId):
    try:
        sql = "select count(id) as c,gitProjectName from d_git_project where id=%s and gitStatus in (0,2)" % (gitProjectId)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### 部署管理->部署配置 deployConfig.py
def rdbDeployProName(deployProName):
    try:
        sql = "select count(id) as c from d_deploy_project where deployName='%s'" % (deployProName)
        data = sqlcomm(sql)
    except:
        data = 0
    return data

#### 部署管理->部署配置 deployConfig.py
def rdbAlldeployProject():
    try:
        sql = "select id,deployName from d_deploy_project"
        data = sqlcomm(sql)
    except:
        data = {}
    return data

#### 部署管理->部署配置 deployConfig.py
def rdbDeployProjectInfo(deployProId):
    try:
        sql = "select id,deployName,deployRsyncIP,deployRsyncUser,deployRsyncProjectName,deployRsyncPasswd,deployRsyncExclude,deployGitSrcUrl,deployGitConfUrl \
                    from d_deploy_project where id=%s" % deployProId
        data = sqlcomm(sql)
    except:
        data = {}
    return data

