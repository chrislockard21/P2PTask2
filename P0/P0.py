import socket
import threading
import socketserver
import datetime
import time
from imports.linked import Node, LinkedList


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        '''
        Function responsible for handling the incoming client requests
        '''
        data = self.request.recv(1024).decode()
        parsed = data.split()
        print(data)

        if parsed[0] == 'PQUERY' and parsed[7] != 'No-piers-active':
            pass


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    '''
    Class to create the threaded TCP server.
    '''
    pass

if __name__ == "__main__":
    # port 0 means to select an arbitrary unused port
    HOST, PORT = socket.gethostbyname(socket.gethostname()), 10000

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    ip, port = server.server_address

    # start a thread with the server.
    # the thread will then start one more thread for each request.
    server_thread = threading.Thread(target=server.serve_forever)
    # agent_thread = threading.Thread(target=agent)
    # agent_thread.start()
    # exit the server thread when the main thread terminates
    server_thread.daemon = False
    server_thread.start()
