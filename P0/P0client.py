import socket
import os
import datetime
import time

RSHost = "localhost"
RSPort = 9999
try:
    hostname = socket.gethostbyname(socket.gethostname())
except:
    hostname = 'localhost'
port = 6666
pier = 'P0'

filename = 'cookieFile.txt'


def openCookie(filename):
    if not os.path.isfile(filename):
        cookie = 'None'
    else:
        file = open(filename, 'r')
        cookie = file.read()
        file.close()
    return cookie


def REGISTER(host, ip, hostname, port, pier, filename):
    '''
    Client connection to register the RFC with the RS server
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, ip))
        cookie = openCookie(filename)
        trans_string = "REGISTER {}\nHost {}\nPort {}\nCOOKIE {}\n".format(pier, hostname, port, str(cookie))
        sock.sendall(trans_string.encode())
        response = sock.recv(1024).decode()
        print(response)
        if cookie is not 'None':
            pass
        else:
            getCookie = response.split()

            file = open(filename, 'w')
            file.write(getCookie[4])
            file.close()

        sock.close()


def LEAVE(host, ip, hostname, port, pier, filename):
    '''
    Initiates the leave process for an RFC server
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, ip))
        cookie = openCookie(filename)
        trans_string = "LEAVE {}\nHOST {}\nPORT {}\nCOOKIE {}\n".format(pier, hostname, port, str(cookie))
        sock.sendall(trans_string.encode())
        response = sock.recv(1024).decode()
        print(response)
        sock.close()


def PQUERY(host, ip, hostname, port, pier, filename):
    '''
    Function that initiates a query of all registered and active piers
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, ip))
        cookie = openCookie(filename)
        trans_string = "PQUERY {}\nHOST {}\nPORT {}\nCOOKIE {}".format(pier, hostname, port, cookie)
        sock.sendall(trans_string.encode())
        response = sock.recv(1024).decode()
        print(response)
        sock.close()


def KEEPALIVE(host, ip, hostname, port, pier, filename):
    '''
    Function to tell the RS to reset TTL and status
    '''
    pass


# Tests:

# REGISTER(RSHost, RSPort, hostname, port, pier, filename)
# time.sleep(2)
# LEAVE(RSHost, RSPort, hostname, port, pier, filename)
# time.sleep(2)
# PQUERY(RSHost, RSPort, hostname, port, pier, filename)
