python 3.5.2
https://www.python.org/ftp/python/

tornado-4.5.3

pip3 install mysqlclient == 1.3.12
pip3 install pymysql 
pip3 install torndb 0.3

/usr/local/lib/python3.5/dist-packages/torndb.py
args = dict(conv=CONVERSIONS, use_unicode=True, charset=charset,
args = dict(conv=CONVERSIONS, charset=charset,

修改
return [Row(itertools.izip(column_names, row)) for row in cursor]
return [Row(itertools.zip_longest(column_names, row)) for row in cursor]

redis-2.10.6
pip3 install redis

PIL-5.0.0
pip3 install Pillow

werkzeug-0.14.1
pip3 install werkzeug
redis-2.10.6
pip3 install redis

第三方
redis 4.0.2
https://redis.io/download

cryptography 2.1.4


https://github.com/tornadoweb/tornado/wiki/Links

需要多个日志按天分割进行不同业务的记录，部署系统日志量很小不考虑高并发问题。不使用logging模块，原因配置复杂，异步写入等问题。直接自己开发的写文件方式。




config.py
dbmodules.py
deployGNR.py
index.py
login.py
modules.py
route.py
userSelf.py      


install/     
logs/
static/
templates/


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



删除用户，并不是真正从数据中删除记录，而是将该用户密码清除，然后将权限对应关系清除。
git用户为禁用为修改用户状态

git用户建议使用key

产生本地加解密key
from cryptography.fernet import Fernet
key = Fernet.generate_key()
