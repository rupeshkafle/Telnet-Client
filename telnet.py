import sys
import getpass
import telnetlib
import time

# HOST = "127.0.0.1"
USERNAME_PROMPTS = [b"Username:", b"login:"]
PASSWORD_PROMPTS = [b"Password:", b"password:"]
LOGGEDIN_PROMPTS = [b">", b"#"]
FAILED_MSGS = [b"failed", b"incorrect"]
CHECK_FAILED_MSGS = ["failed", "incorrect"]

loggedin = False
havemore = False
host = input("Enter Hostname: ")

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

        # Check for  privileged mode
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

tn.write(b"show interface brief\r\n")
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
