from inspect import EndOfBlock
from queue import Empty
import sys
import getpass
import telnetlib
import time
from tkinter import END


HOST = "127.0.0.1"
USERNAME_PROMPTS = [b"Username:", b"login:"]
PASSWORD_PROMPTS = [b"Password:", b"password:"]
LOGGEDIN_PROMPTS = [b">", b"#"]
FAILED_MSGS = [b"failed", b"incorrect"]

loggedin = False
host = input("Enter Hostname: ")

while loggedin == False:
    username = input("Username: ")
    password = getpass.getpass()

    tn = telnetlib.Telnet(host)
    tn.set_debuglevel(1)

    tn.expect(USERNAME_PROMPTS)
    tn.write(username.encode('ascii') + b"\r\n")
    tn.expect(PASSWORD_PROMPTS)
    tn.write(password.encode('ascii') + b"\r\n")

    print(tn.expect(FAILED_MSGS, timeout=1))

    # if isFailed:
    #     print("Authentication Failed")
    # else:
    #     tn.expect(LOGGEDIN_PROMPTS)
    #     tn.write(b"dir\r\n")
