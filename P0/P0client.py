import socket
import os
import json
import datetime

RSHost = "localhost"
RSPort = 9999
hostname = socket.gethostbyname(socket.gethostname())
port = 6666
peer = 'P0'

filename = 'cookieFile.txt'
if not os.path.isfile(filename):
    cookie = 'None'
else:
    file = open(filename, 'r')
    cookie = file.read()
    file.close()
    # print(cookie)

def REGISTER(host, ip, hostname, port, peer, cookie):
    '''
    Client connection to register the RFC with the RS server
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, ip))
        trans_string = f"REGISTER {peer}\nHost {hostname}\nPort {port}\nCookie {str(cookie)}"
        sock.sendall(trans_string.encode())
        print(trans_string)
        if cookie is not 'None':
            print('Request for extenstion granted')
        else:
            cookie = sock.recv(1024).decode()
            file = open(filename, 'w')
            file.write(cookie)
            file.close()
        
        sock.close()

REGISTER(RSHost, RSPort, hostname, port, peer, cookie)

def LEAVE(host, ip, hostname, port, peer):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, ip))
        trans_string = ''