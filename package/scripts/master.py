from os.path import join
from resource_management import *
import sys, os, pwd, grp, signal, time, glob
from distutils.dir_util import copy_tree
from shutil import copy, rmtree, copytree

class TomcatMaster(Script):
    def install(self, env):
        print 'Install the Tomcat Master.'

        # Load the all configuration files
        config = Script.get_config()

        tomcat_user = config['configurations']['common-env']['user']
        tomcat_group = config['configurations']['common-env']['group']
        tomcat_home = config['configurations']['common-env']['catalina_home']
        tomcat_package = os.path.join(os.path.dirname(__file__), '..', 'tomcat')

        # Create  user and group (if they don't exist)
        try: grp.getgrnam(tomcat_group)
        except KeyError: Execute(format('groupadd {tomcat_group}'))

        try: pwd.getpwnam(tomcat_user)
        except KeyError: Execute(format('adduser {tomcat_user} -g {tomcat_group}'))

        Execute(format('mkdir -p {tomcat_home}'),
                user=tomcat_user,
                group=tomcat_group)

        Execute(format('rm -r {tomcat_home}'))

        #copy_tree(tomcat_package, tomcat_home)

        #os.chown(tomcat_home, tomcat_user, tomcat_group)


        os.system(format('cp -a {tomcat_package} {tomcat_home}'))
        os.system(format('mkdir {tomcat_home}/logs'))
        os.system(format('mkdir {tomcat_home}/work'))

        os.system(format('chown {tomcat_user}:{tomcat_group} -R {tomcat_home}'))
        os.system(format('chmod ug+x {tomcat_home}/bin/*.sh'))

        uid = pwd.getpwnam(tomcat_user).pw_uid
        gid = grp.getgrnam(tomcat_group).gr_gid
        #copytree(tomcat_package, tomcat_home)
        #os.chown(tomcat_package, uid, gid)

        #Execute(format('cp -a {tomcat_package} {tomcat_home}'))


        # Install packages
        self.install_packages(env)

        #Directory([tomcat_home],
        #          recursive=True)
        #Execute('cp -r %s/* %s' % (tomcat_package, tomcat_home))


        # Create a new user and group
        #Execute( format("groupadd -f {tomcat_user}") )
        #Execute( format("id -u {tomcat_user} &>/dev/null || useradd -s /bin/bash {tomcat_user} -g {tomcat_user}") )

        ### Continue installing and configuring your service

        print 'Installation complete.'

    def configure(self, env):
        config = Script.get_config()

        tomcat_user = config['configurations']['common-env']['user']
        tomcat_group = config['configurations']['common-env']['group']
        tomcat_home = config['configurations']['common-env']['catalina_home']
        tomcat_lib = join(tomcat_home, "lib")

        hbase_site = "/etc/hbase/conf/hbase-site.xml"
        hdfs_site = "/etc/hadoop/conf/hdfs-site.xml"
        core_site = "/etc/hadoop/conf/core-site.xml"

        copyFile = lambda src, dst: Execute(format('cp {src} {dst}'), user=tomcat_user, group=tomcat_group)

        copyFile(hbase_site, tomcat_lib)
        copyFile(hdfs_site, tomcat_lib)
        copyFile(core_site, tomcat_lib)


    def stop(self, env):
        print 'Stop the Tomcat Master'
        config = Script.get_config()
        tomcat_home = config['configurations']['common-env']['catalina_home']
        Execute("sh "+tomcat_home+"/bin/shutdown.sh")


    def start(self, env):
        print 'Start the Tomcat Master'
        self.configure(env)
        config = Script.get_config()
        tomcat_home = config['configurations']['common-env']['catalina_home']
        Execute("sh "+tomcat_home+"/bin/startup.sh")

    def status(self, env):
        print 'Status of the Tomcat Master'
        config = Script.get_config()
        tomcat_home = config['configurations']['common-env']['catalina_home']
        tomcat_pid=tomcat_home+'/bin/catalina.pid'
        check_process_status(tomcat_pid)

if __name__ == "__main__":
    TomcatMaster().execute()
