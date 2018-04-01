python 3.5.2
https://www.python.org/ftp/python/

第三方库
pip3 install tornado == 4.5.3
pip3 install redis == 2.10.6
pip3 install Pillow == 5.0.0
pip3 install werkzeug == 0.14.1
pip3 install cryptography == 2.1.4
pip3 install redis == 2.10.6
pip3 install mysqlclient == 1.3.12
pip3 install pymysql == 0.8.0
pip3 install torndb == 0.3
#### torndb不支持python3,源码修改如下
/usr/local/lib/python3.5/dist-packages/torndb.py
args = dict(conv=CONVERSIONS, use_unicode=True, charset=charset,
args = dict(conv=CONVERSIONS, charset=charset,
修改
return [Row(itertools.izip(column_names, row)) for row in cursor]
return [Row(itertools.zip_longest(column_names, row)) for row in cursor]



第三方工具
redis 4.0.2
https://redis.io/download


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


需要多个日志按天分割进行不同业务的记录，部署系统日志量很小不考虑高并发问题。不使用logging模块，原因配置复杂，异步写入等问题。直接自己开发的写文件方式。
删除用户，并不是真正从数据中删除记录，而是将该用户密码清除，然后将权限对应关系清除。
git用户为禁用为修改用户状态


# 基础信息。包含title,username,domainname,column
@htmlBaseInfo
# 认证部分。如果不需要认证，则注释掉下面一行
@auth
# 检查输入参数，防止sql注入,黑白名单等
@checkUrl

# 检查权限84
if checkAuth(self.baseInfo['getUserName'], 84) < 1:
    self.render("error.html", baseInfo = self.baseInfo, \
                            err = {'text':'权限异常。'})
    return



git用户建议使用key

产生本地加解密key
from cryptography.fernet import Fernet
key = Fernet.generate_key()



学习文档：
https://github.com/tornadoweb/tornado/wiki/Links