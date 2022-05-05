from ast import match_case
import time
import telnetlib
import getpass
from bdcom import BdcomEpon
from bdcom import BdcomGpon

# HOST = "127.0.0.1"
USERNAME_PROMPTS = [b"Username:", b"login:"]
PASSWORD_PROMPTS = [b"Password:", b"password:"]
LOGGEDIN_PROMPTS = [b">", b"#"]
FAILED_MSGS = [b"failed", b"incorrect"]
CHECK_FAILED_MSGS = ["failed", "incorrect"]

loggedin = False
havemore = False
host = input("Enter Hostname: ")


def CheckPrivilegedMode():
    if ">" in isFailed:
        privileged = False
        tn.write(b"enable\r\n")
        time.sleep(2)  # wait 2 seconds before going to next code
        var = tn.read_eager()
        if b"#" in var:
            privileged = True
        while not privileged:
            enablepassword = input("Enter enable password: ")
            tn.write(enablepassword.encode('ascii') + b"\r\n")
            time.sleep(2)
            var = tn.read_eager()
            if b"#" in var:
                privileged = True
                break


while loggedin == False:
    username = input("Username: ")
    password = getpass.getpass()

    tn = telnetlib.Telnet(host)
    tn.expect(USERNAME_PROMPTS)
    tn.write(username.encode('ascii') + b"\r\n")
    tn.expect(PASSWORD_PROMPTS)
    tn.write(password.encode('ascii') + b"\r\n")

    isFailedObject = tn.expect(FAILED_MSGS, timeout=1)
    isFailed = isFailedObject[2].decode('ascii')

    """ checks if isFailed contains any string which indicates failed logged
        and displays failure message and returns to start of while loop
    """
    if any(key in isFailed for key in CHECK_FAILED_MSGS):
        print("Authentication Failed")
    else:
        loggedin = True
        CheckPrivilegedMode()

olt = BdcomEpon()


def ReadOperations(i):
    match i:
        case "1":
            return tn.write(olt.showInterface)
        case "2":
            return tn.write(olt.showMacTable)
        case "3":
            return tn.write(olt.showActiveOnu)
        case "4":
            return tn.write(olt.showInactiveOnu)
        case "5":
            return tn.write(olt.showRejectedOnu)
        case "6":
            return tn.write(olt.showOnuInfo)
        case default:
            pass


def ShowReadOpeartions():
    print("1. Show Interfaces\r\n")
    print("2. Show Mac Address Table\r\n")
    print("3. Show Active Onu\r\n")
    print("4. Show Inactive Onu\r\n")
    print("5. Show Rejected Onu\r\n")
    print("6. Show Onu Information\r\n")
    option = input("Choose a option: ")

    return print(ReadOperations(option))


def ShowWriteOperations():
    return print("Feature Under Development")


def ShowMainMenu():
    print("1. Read Operations\r\n")
    print("2. Write Operations\r\n")
    option = input("Choose a operation: ")
    match option:
        case "1":
            ShowReadOpeartions()
        case "2":
            ShowWriteOperations()
        case default:
            ShowMainMenu()


ShowMainMenu()


"""Reads output from telnet line by line and automatically scrolls if there are
    more output to fetch on screen
"""
while True:
    tnResponse = tn.read_until(b"\r\n", 2)
    print(tnResponse.decode('ascii'))
    if b"More" in tnResponse:
        havemore = True
        while havemore == True:
            tn.write(b"\r\n")
            tnResponse = tn.read_until(b"\r\n", 2)
            print(tnResponse.decode('ascii'))
            if b"#" in tnResponse:
                break
    if b"#" in tnResponse:
        break
tn.close()
