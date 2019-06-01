import socket
import threading
import socketserver
import datetime
import time

class Node():

    def __init__(self, peer_name, hostname, port, cookie):
        self.peer_name = peer_name
        self.hostname = hostname
        self.port = port
        self.cookie = cookie
        self.status = 'active'
        self.TTL = datetime.datetime.now() + datetime.timedelta(0, 7200)
        self.reg_time = datetime.datetime.now()
        self.next = None

    def __repr__(self):
        return f'{self.peer_name}, {self.hostname}, {self.port}, {self.cookie}, {self.status}, {self.TTL}, {self.reg_time}'


class LinkedList():

    def __init__(self):
        self.startNode = None
        self.curr_cookie = 1

    def walkList(self):
        if self.startNode is None:
            print('No RFCs to list')
            return
        else:
            n = self.startNode
            while n is not None:
                print(n.__repr__(), ' ')
                n = n.next


    def addRFCEnd(self, peer_name, hostname, port, cookie):
        newNode = Node(peer_name, hostname, port, cookie)
        if self.startNode is None:
            self.startNode = newNode
            return
        n = self.startNode
        while n.next is not None:
            n = n.next
        n.next = newNode


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).decode()
        parsed = data.split()
        print(data)
        if parsed[0] == 'REGISTER':
            if parsed[-1] == 'None':
                self.request.sendall(str(linkedRFCServers.curr_cookie).encode())
                linkedRFCServers.addRFCEnd(parsed[1], parsed[3], parsed[5], linkedRFCServers.curr_cookie)
                linkedRFCServers.curr_cookie += 1
            else:
                self.request.sendall('Request for extension valid'.encode())

        elif parsed[0] == 'KEEPALIVE':
            pass
        elif data == 'CheckPiers':
            self.request.sendall('there'.encode())
            # linkedRFCServers.walkList()
        elif parsed[0] == 'LEAVE':
            pass
        
         
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def agent():
    while True:
        time.sleep(2)
        linkedRFCServers.walkList()


if __name__ == "__main__":
    # port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 9999
    linkedRFCServers = LinkedList()
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    current_cookie = 1
    ip, port = server.server_address

    # start a thread with the server. 
    # the thread will then start one more thread for each request.
    server_thread = threading.Thread(target=server.serve_forever)
    agent_thread = threading.Thread(target=agent)
    agent_thread.start()
    # exit the server thread when the main thread terminates
    server_thread.daemon = False
    server_thread.start()