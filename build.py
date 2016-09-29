#!/usr/bin/env python
import os
import sys
from shutil import copy, rmtree
from distutils.dir_util import copy_tree

from os.path import join

project = lambda file='': os.path.abspath(os.path.dirname(sys.argv[0])) + "/" + file
target = lambda file='': project() + 'target/' + file

tomcat = target("apache-tomcat-"+sys.argv[1])
tomcatLib = tomcat+"/lib"
tomcatWebapp = tomcat+"/webapps"
tomcatConf = tomcat+"/conf"
tomcatBin = tomcat+"/bin"


def configureTomcat():
    copy(project("tomcat-conf/server.xml"), tomcatConf)
    copy(project("tomcat-conf/tomcat-users.xml"), tomcatConf)
    copy(project("tomcat-conf/setenv.sh"), tomcatBin)
    copy(project("tomcat-conf/context.xml"), join(tomcatWebapp, "manager", "META-INF"))

def removeWebApps():
    rmtree(tomcatWebapp+"/docs")
    rmtree(tomcatWebapp+"/examples")
    rmtree(tomcatWebapp+"/ROOT")

def copyDependencies():
    copy_tree(target("dependencies"), tomcatLib)

#copy_tree(project("server"), target())

configureTomcat()
removeWebApps()
copyDependencies()