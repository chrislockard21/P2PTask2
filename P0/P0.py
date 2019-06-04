import socket
import threading
import socketserver
import datetime
import time
from imports.linked import Node, LinkedList
import os


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        '''
        Function responsible for handling the incoming client requests
        '''
        data = self.request.recv(1024).decode()
        parsed = data.split()
        print(data)

        if parsed[0] == 'RFCINDEX':
            trans_string = 'RFCINDEX {} OK\nHOST {}\nPORT {}\nRFCs\n'.format(parsed[1], parsed[3], parsed[5])
            RFC = linkedRFCIndex.RFCIndex()
            for R in RFC:
                trans_string += R
            self.request.sendall(trans_string.encode())

        elif parsed[0] == 'RFCINDEX' and parsed[2] == 'OK':
            i = 7
            RFCList = []
            while i < len(parsed):
                RFC = parsed[i].split('\t')
                currentList = linkedRFCIndex.RFCIndex()
                print(currentList)
                linkedRFCIndex.addRFCRecordEnd(RFC[0], RFC[1], RFC[2], RFC[3])
            


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    '''
    Class to create the threaded TCP server.
    '''
    pass

if __name__ == "__main__":
    # port 0 means to select an arbitrary unused port
    HOST, PORT = socket.gethostbyname(socket.gethostname()), 10000

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    linkedRFCIndex = LinkedList()
    RFCPath = 'RFCs'
    RFCfiles = [f for f in os.listdir(RFCPath) if os.path.isfile(os.path.join(RFCPath, f))]
    for f in RFCfiles:
        number = f[:4]
        title = f[4:]
        linkedRFCIndex.addRFCRecordEnd(number, title, HOST, PORT)

    linkedRFCIndex.walkList()
    ip, port = server.server_address

    # start a thread with the server.
    # the thread will then start one more thread for each request.
    server_thread = threading.Thread(target=server.serve_forever)
    # agent_thread = threading.Thread(target=agent)
    # agent_thread.start()
    # exit the server thread when the main thread terminates
    server_thread.daemon = False
    server_thread.start()
