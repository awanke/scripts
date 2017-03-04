# encoding:utf-8

import os, sys, time, random, thread

start_operation = ['startup', 'start']
stop_operation  = ['shutdown', 'stop']
status_operation  = ['status']
show_operation  = ['show', 'log']
restart_operation  = ['reload']
env = '-Xms128m -Xmx128m'

# search tale-xxx.jar
def search(path, word):
    for filename in os.listdir(path):
        fp = os.path.join(path, filename)
        if os.path.isfile(fp) and word in filename:
            return fp
        elif os.path.isdir(fp):
            search(fp, word)

# get tale pid
def get_pid():
    output = os.popen("ps -ef | grep tale.jar | grep -v grep | awk '{print $2}'")
    return output.read()

# determine whether there is tale process
def exist():
    pid = get_pid()
    return pid != ''

# startup tale
def startup(jar_name):
    if exist():
        print 'Tale already startup!'
    else:
        # start tale
        cmd = 'java '+ env +' -jar '+ jar_name +' > ./tale.out < /dev/null &'
        print 'cmd: ' + cmd
        os.system(cmd)
        show_log()
    pass

# shutdown tomcat
def shutdown():
    if exist():
        pid = get_pid()
        os.system('kill -9 ' + str(pid))
    pass

def show_log():
    os.system('tail -f ./tale.out')
    pass

def show_help():
    print '\r\n\t欢迎使用Tale Blog :)'
    print '\r\nUsage: tale start|stop|reload|status|log'
    print '\r\n可选参数: [-env] [-h]'
    print '\t-env\t\tjvm相关参数'
    print '\t-h\t\t帮助信息'

def show_status():
    if exist():
        print 'Tale is running with pid:', get_pid()
    else:
        print 'Tale is stop!'
    pass

def main():
    operation = ''
    sleeptime = 0
    arglen = len(sys.argv)
    
    if arglen >= 3:
        if isinstance(sys.argv[2], int):
            sleeptime = sys.argv[2]
    	if sys.argv[2] == '-env':
            global env 
            env = sys.argv[3]
        if sys.argv[1] == '-h':
            show_help()
            sys.exit(0)   
    try:
	    operation = sys.argv[1]
    except:
        show_help()
        sys.exit(0)
    
    jar_name = search(os.path.pardir,'.jar')
    if operation in start_operation:
        startup(jar_name)
    elif operation in stop_operation:
        if exist() == False:
            print 'Tale already shutdown!'
        else:
            print 'Stoping Tale...'
            shutdown()
            show_status()
    elif operation in restart_operation:
        shutdown()
        time.sleep(float(sleeptime))
        startup(jar_name)
    elif operation in status_operation:
        show_status()
    elif operation in show_operation:
        show_log()
    else:
        show_help()
        sys.exit(0)

if __name__=="__main__":
    main()
