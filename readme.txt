CentOS 7 x86_64 

python 3.5.5
https://www.python.org/ftp/python/

virtualenv 16.3.0

第三方库
pip3 install -r requirements.txt


第三方工具
redis 4.0.2
https://redis.io/download

代码部署在git用户下。

主要文件说明
config.py                全局配置文件。
dbmodules.py             数据库模块，系统中所有SQL都写入该文件。
deployGNR.py             主文件，启动使用。
modules.py               公共方法模块。
route.py                 路由。

主要目录
install/     
logs/
static/
templates/

默认数据库脚本在install中。
本地git库管理，使用gitosis管理。
默认账号admin，密码admin。

需要多个日志按天分割进行不同业务的记录，部署系统日志量很小不考虑高并发问题。
不使用logging模块，原因配置复杂，异步写入等问题。直接的写文件方式。
删除用户，并不是真正从数据中删除记录，而是将该用户密码清除，然后将权限对应关系清除。
git用户为禁用为修改用户状态


# 基础信息。包含title,username,domainname,column
@htmlBaseInfo
# 认证部分。如果不需要认证，则注释掉下面一行
@auth
# 检查输入参数，防止sql注入,黑白名单等
@checkUrl
# 查看权限 
@checkSubmitAuth(101)

还有一中在类中，用于判断单次提交多类。
# 检查权限84
if checkAuth(self.baseInfo['getUserName'], 84) < 1:
    self.render("error.html", baseInfo = self.baseInfo, \
                            err = {'text':'权限异常。'})
    return



git用户建议使用key管理

产生本地加解密key
from cryptography.fernet import Fernet
key = Fernet.generate_key()



学习文档：
https://github.com/tornadoweb/tornado/wiki/Links