import getopt
import os.path
import signal
import socket
import subprocess
import sys
import time

def have_server():
    # check that the server is running
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("localhost", 4444))
        s.close()
        return True
    except socket.error, e: # Connection Refused
        return False
        
def start_server():
    s = subprocess.Popen(['java', '-jar', 'third_party/selenium/selenium-server-standalone-2.0b2.jar'], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT).pid
    pidfile = open("third_party/selenium/server.pid", "w")
    pidfile.write(str(s))
    pidfile.close()

    # make sure the server is actually up
    server_up = False
    waiting = 0
    while server_up == False and waiting < 60:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("localhost", 4444))
            s.close()
            server_up = True
        except socket.error:
            time.sleep(1)
            server_up = False

    return server_up
    
def stop_server():
    dead = False
    if os.path.exists("third_party/selenium/server.pid"):
        pidfile = open("third_party/selenium/server.pid", "r")
        pid = int(pidfile.read())
        pidfile.close()
        os.kill(pid, signal.SIGTERM)
        os.remove("third_party/selenium/server.pid")
        dead = True
        
    return dead

def help():
    print("monkey")

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "csk", ["check", "start", "stop"])
    for o, a in opts:
        if o == "--check":
            up = have_server()
            if up == True:
                sys.exit(0)
            else:
                sys.exit(1)
        elif o == "--start":
            up = start_server()
            if up == True:
                sys.exit(0)
            else:
                sys.exit(1)
        elif o == "--stop":
            up = stop_server()
            if up == True:
                sys.exit(0)
            else:
                sys.exit(1)

    help()
