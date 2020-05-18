#!/usr/bin/python
import argparse
import logging
import os
softwares={'gcc':'gcc-7.x',
           'maven':'maven-3.6.1',
           'openjdk':'openjdk 1.8.x'
           }
#argument parser
parser = argparse.ArgumentParser(description='A tool for installing some dev softwares automatically for centos or ubuntu based on Kunpeng920. Supported software: %s'%str(softwares))
parser.add_argument('-i','--install',type=str,required=True,nargs='+',choices=softwares.keys())
args = parser.parse_args()

#log
logger=logging.getLogger()
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler('/var/log/bld.log')
formatter=logging.Formatter('%(asctime)s [%(name)s] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
def loginfo(s):
    print(s)
    logger.info(s)
def logwarn(s):
    print(s)
    logger.warning(s)
def logerror(s):
    print(s)
    logger.error(s)

#Step1: define the software dependence
dpendence = {
    'maven':['openjdk']
}
#Step2: define the version_check method
check_version = {
    'gcc':'gcc --version | grep -E 7.[0-9].[0-9]',
    'maven':'mvn -v',
    'openjdk':'java -version',

}
#Step3: define the env
env_dic = {
    'maven': ['MAVEN_HOME=/usr/local/apache-maven-3.6.1','export PATH=\${MAVEN_HOME}/bin:\$PATH'],
    'openjdk_centos': ['export JAVA_HOME=/home/jdk/jdk1.8.0_232','export PATH=\${JAVA_HOME}/bin:\$PATH'],
    'openjdk_ubuntu':['export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64']
}

#define installer
def installer(fun):
    def myinstaller():
        ostype = 'centos' if 'centos' in os.popen('cat /etc/*release | grep centos').read() else 'ubuntu'
        logger.name = fun.__name__
        loginfo('+Begin install %s' % fun.__name__)
        #check if already installed
        if 0 == os.system(check_version[fun.__name__]):
            loginfo('%s already installed' % fun.__name__)
            loginfo('+End install %s' % fun.__name__)
            return 0
        #install depndence
        if fun.__name__ in dpendence.keys():
            loginfo('-Installing dpendence for %s' % fun.__name__)
            for i in dpendence[fun.__name__]:
                run(i)
        #install
        res= fun(ostype)
        #add env
        env = []
        if fun.__name__ in env_dic.keys():
            env = env_dic[fun.__name__]
        if ostype == 'centos':
            if '%s_centos' % fun.__name__ in env_dic.keys():
                env = env_dic['%s_centos' % fun.__name__]
            for i in env:
                os.system('echo "%s" >> ~/.bash_profile' % i)
        else:
            if '%s_ubuntu' % fun.__name__ in env_dic.keys():
                env = env_dic['%s_ubuntu' % fun.__name__]
            for i in env:
                os.system('echo "%s" >> ~/.bashrc' % i)
        loginfo('+End install %s' % fun.__name__)
        return res
    return myinstaller()

#template

# def install_gcc():
#     @installer
#     def gcc(ostype):
#         cmds = []
#         if ostype == 'centos':
#             pass
#         else:
#             pass
#         for cmd in cmds:
#             os.system(cmd)

#Step4: define the install function
def install_gcc():
    @installer
    def gcc(ostype):
        cmds = []
        if ostype == 'centos':
            cmds = ['yum install -y gcc gcc-c++ bzip2',
                    'wget https://ftp.gnu.org/gnu/gcc/gcc-7.3.0/gcc-7.3.0.tar.gz'\
                if not 0 == os.system('ls gcc-7.3.0.tar.gz') else '',
                    'tar -zxvf gcc-7.3.0.tar.gz -C /usr/local/src',
                    'wget https://gcc.gnu.org/pub/gcc/infrastructure/gmp-6.1.0.tar.bz2 -P /usr/local/src/gcc-7.3.0'\
                if not 0 == os.system('ls /usr/local/src/gcc-7.3.0/gmp-6.1.0.tar.bz2') else '',
                    'wget https://gcc.gnu.org/pub/gcc/infrastructure/isl-0.16.1.tar.bz2 -P /usr/local/src/gcc-7.3.0'\
                if not 0 == os.system('ls /usr/local/src/gcc-7.3.0/isl-0.16.1.tar.bz2') else '',
                    'wget https://gcc.gnu.org/pub/gcc/infrastructure/mpc-1.0.3.tar.gz -P /usr/local/src/gcc-7.3.0'\
                if not 0 == os.system('ls /usr/local/src/gcc-7.3.0/mpc-1.0.3.tar.gz') else '',
                    'wget https://gcc.gnu.org/pub/gcc/infrastructure/mpfr-3.1.4.tar.bz2 -P /usr/local/src/gcc-7.3.0'\
                if not 0 == os.system('ls /usr/local/src/gcc-7.3.0/mpfr-3.1.4.tar.bz2') else '',
                    'cd /usr/local/src/gcc-7.3.0 && ./contrib/download_prerequisites',
                    'cd /usr/local/src/gcc-7.3.0 && ./configure --prefix=/usr',
                    'cd /usr/local/src/gcc-7.3.0 && make -j4 && make install']
        else:
            cmds = ['apt-get instlal gcc']
        for cmd in cmds:
            os.system(cmd)

def install_maven():
    @installer
    def maven(ostype):
        cmds=['wget http://mirrors.tuna.tsinghua.edu.cn/apache/maven/maven-3/3.6.1/binaries/apache-maven-3.6.1-bin.tar.gz' \
            if not 0 == os.system('ls apache-maven-3.6.1-bin.tar.gz') else '',
              'tar -zxvf apache-maven-3.6.1-bin.tar.gz -C /usr/local/']
        for cmd in cmds:
            os.system(cmd)

def install_openjdk():
    @installer
    def openjdk(ostype):
        cmds=[]
        if ostype == 'centos':
            cmds=['wget https://portal-www-software.obs.cn-north-1.myhuaweicloud.com/%E7%BC%96%E8%AF%91%E5%B7%A5%E5%85%B7/jdk-8u232-linux-aarch64.tar.gz' \
                if not 0 == os.system('ls jdk-8u232-linux-aarch64.tar.gz') else '',
                  'mkdir -p /home/jdk',
                  'tar -zxvf jdk-8u232-linux-aarch64.tar.gz -C /home/jdk']
        else:
            cmds=['apt-get install -y openjdk-8-source']
        for cmd in cmds:
            #print(cmd)
            os.system(cmd)

#Step5: register the install function
installer_dic = {
    'gcc':install_gcc,
    'maven':install_maven,
    'openjdk':install_openjdk
}

def run(f):
    return installer_dic[f]()
if __name__ == '__main__':
    ostype = 'centos' if 'centos' in os.popen('cat /etc/*release | grep centos').read() else 'ubuntu'
    loginfo('ostype = %s' % ostype)
    if not 0==os.system('%s install -y curl wget' %('yum' if 'centos' == ostype else 'apt-get')):
        logerror('run cmd "yum install -y curl wget" failed')
        exit(1)
    loginfo('Begin checking internet connect')
    if '' == os.popen('curl baidu.com').read():
        logerror('connect to the internet failed, please check the network!')
        exit(1)
    loginfo('internet connected')
    for f in args.install:
        try:
            run(f)
        except Exception as e:
            logerror(str(e))



