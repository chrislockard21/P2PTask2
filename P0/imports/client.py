import socket
import os
import datetime
import time

RSHost = socket.gethostbyname(socket.gethostname())
RSPort = 9999
try:
    hostname = socket.gethostbyname(socket.gethostname())
except:
    hostname = 'localhost'
port = 10000
pier = 'P0'
hostname = socket.gethostbyname(socket.gethostname())
filename = 'cookieFile.txt'


def openCookie(filename):
    if not os.path.isfile(filename):
        cookie = 'None'
    else:
        file = open(filename, 'r')
        cookie = file.read()
        file.close()
    return cookie


def REGISTER(rshost, rsport, hostname, port, pier, filename):
    '''
    Client connection to register the RFC with the RS server
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((rshost, rsport))
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


def LEAVE(rshost, rsport, hostname, port, pier, filename):
    '''
    Initiates the leave process for an RFC server
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((rshost, rsport))
        cookie = openCookie(filename)
        trans_string = "LEAVE {}\nHOST {}\nPORT {}\nCOOKIE {}\n".format(pier, hostname, port, str(cookie))
        sock.sendall(trans_string.encode())
        response = sock.recv(1024).decode()
        print(response)
        sock.close()


def PQUERY(rshost, rsport, hostname, port, pier, filename):
    '''
    Function that initiates a query of all registered and active piers
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((rshost, rsport))
        cookie = openCookie(filename)
        trans_string = "PQUERY {}\nHOST {}\nPORT {}\nCOOKIE {}".format(pier, hostname, port, cookie)
        sock.sendall(trans_string.encode())
        response = sock.recv(1024).decode()
        print(response)
        sock.close()
    return response
  

def RFCINDEX(response, hostname, port):
    '''
    This function is used to process output from PQUERY and retreive the index from all listening piers
    '''
    parsed = response.split()
    i = 8
    pier_list = []
    while i < len(parsed):
        pier_list.append(parsed[i].split('-'))
        i += 1
    for pier in pier_list:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((pier[1], int(pier[2])))
            trans_string = 'RFCINDEX {}\nHOST {}\nPORT {}\n'.format(pier[0], pier[1], pier[2])
            sock.sendall(trans_string.encode())
            data = sock.recv(1024).decode()
            
            sock.close()
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockHost:
            sockHost.connect((hostname, port))
            sockHost.sendall(data.encode())
            sockHost.close()


def KEEPALIVE(rshost, rsport, hostname, port, pier, filename):
    '''
    Function to tell the RS to reset TTL and status
    '''
    pass


# Tests:

REGISTER(RSHost, RSPort, hostname, port, pier, filename)
time.sleep(2)
# # LEAVE(RSHost, RSPort, hostname, port, pier, filename)
# # time.sleep(2)
RFCINDEX(PQUERY(RSHost, RSPort, hostname, port, pier, filename), hostname, port)
