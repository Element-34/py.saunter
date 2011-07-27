# Copyright 2011 Element 34
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
==============
SeleniumServer
==============

Script for controlling the Selenium Server. Can be used from in a script or standalone. If used standalone, it can be called with either
 * check
 * start
 * stop
"""

import getopt
import os.path
import signal
import socket
import subprocess
import sys
import time
import tempfile

pid_file_path = os.path.join(tempfile.gettempdir(), "selenium-server.pid")

def have_server():
    """
    Checks whether the server is running on localhost:4444 (the defaults)
    
    :returns: Boolean
    """
    # check that the server is running
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("localhost", 4444))
        s.close()
        return True
    except socket.error, e: # Connection Refused
        return False
        
def start_server():
    """
    Starts the included server and writes out the pid
    """
    s = subprocess.Popen(['java', '-jar', 'third_party/selenium/selenium-server-standalone-2.0b2.jar'], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT).pid
    pidfile = open(pid_file, "w")
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
    """
    Stops the process in the selenium server's pid file.
    """
    dead = False
    if os.path.exists(pid_file_path):
        pidfile = open(pid_file_path, "r")
        pid = int(pidfile.read())
        pidfile.close()
        os.kill(pid, signal.SIGTERM)
        os.remove(pid_file_path)
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
