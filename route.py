import tornado
from modules import *
from login import *
from index import *
from userSelf import *
from userEditPass import *
from userMan import *
from groupMan import *
from gitProjectMan import *
from gitUserMan import *
from gitAuthMan import *
from gitLocalCon import *
from deployConfig import *


application = tornado.web.Application([
    (r"/", LoginHandler),              #login.py
    (r"/index/", MainHandler),         #index.py
    (r"/index/userSelf/", userSelfHandler),         #userSelf.py
    (r"/index/userEditPass/", userEditPassHandler),         #userEditPass.py
    (r"/index/userMan/", userManHandler),         #userMan.py
    (r"/index/userManGroupHave/", userManGroupHaveHandler),         #userMan.py
    (r"/index/groupMan/", groupManHandler),         #groupMan.py
    (r"/index/groupuseauth/", groupUseAuthHandler),         #groupMan.py
    (r"/index/groupusecol/", groupUseColHandler),         #groupMan.py
    (r"/index/gitProjectMan/", gitProjectManHandler),         #gitProjectMan.py
    (r"/index/gitUserMan/", gitUserManHandler),         #gitUserMan.py
    (r"/index/gitAuthMan/", gitAuthManHandler),         #gitAuthMan.py
    (r"/index/getproinuser/", projectHaveUserAllUserHandler),         #gitAuthMan.py
    (r"/index/getuserinpro/", userHavePorjectAllProjectHandler),         #gitAuthMan.py
    (r"/index/gitLocalCon/", gitLocalConHandler),         #gitLocalCon.py
    (r"/index/deployConfig/", deployConfigHandler),         #deployConfig.py
    (r"/index/addDeployProject/", addDeployConfigHandler),         #deployConfig.py
    (r"/images/(.*)", tornado.web.StaticFileHandler, {"path":imgRootPath},),
    (r".*", BaseErrorHandler),         #modules.py
], **settings)
