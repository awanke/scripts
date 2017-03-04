# encoding:utf-8

import os, sys, time, random, thread

start_operation = ['startup', 'start']
stop_operation  = ['shutdown', 'stop']
status_operation  = ['status']
show_operation  = ['show', 'log']
restart_operation  = ['reload']

# get tale pid
def get_pid():
    output = os.popen("ps -ef | grep tale.jar | grep -v grep | awk '{print $2}'")
    return output.read()

# determine whether there is tale process
def exist():
    pid = get_pid()
    return pid != ''

# startup tale
def startup():
    if exist():
        print 'Tale already startup!'
    else:
        # start tale
        os.system('java -jar ../tale.jar > ./tale.out < /dev/null &')
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
    print 'Usage: tale start|stop|reload|status|log]'

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
    if arglen == 3:
    	sleeptime = sys.argv[2]
    try:
	    operation = sys.argv[1]
    except:
        show_help()
        sys.exit(0)
        
    if operation in start_operation:
        startup()
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
        startup()
    elif operation in status_operation:
        show_status()
    elif operation in show_operation:
        show_log()
    else:
        show_help()
        sys.exit(0)

if __name__=="__main__":
    main()
