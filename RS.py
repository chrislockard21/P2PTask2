import socket
import threading
import socketserver
import datetime
import time

class Node():

    def __init__(self, pier_name, hostname, port, cookie):
        self.pier_name = pier_name
        self.hostname = hostname
        self.port = port
        self.cookie = cookie
        self.status = 'active'
        self.TTL = datetime.datetime.now() + datetime.timedelta(0, 7200)
        self.reg_time = datetime.datetime.now()
        self.reg_num = 1
        self.next = None

    def __repr__(self):
        return 'PEER-NAME {}\nHOST {}\nPORT {}\nTTL {}\nSTATUS {}'.format(self.pier_name, self.hostname, self.port, self.TTL, self.status)


class LinkedList():
    '''
    LinkedList class creates a linked list and establishes methods to append
    the list and walk it's contents.
    '''
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

    def reRegisterRFC(self, cookie):
        if self.startNode is None:
            print('No RFCs to list')
            return
        else:
            n = self.startNode
            while n is not None:
                if cookie == n.cookie:
                    n.status = 'active'
                    n.TTL = datetime.datetime.now() + datetime.timedelta(0, 7200)
                    n.reg_num += 1
                    return (n.TTL, n.reg_num)
                n = n.next

    def leaveRFC(self, cookie):
        if self.startNode is None:
            print('No RFCs to list')
            return
        else:
            n = self.startNode
            while n is not None:
                if cookie == n.cookie:
                    n.status = 'inactive'
                    n.TTL = 0
                    return (n.TTL, n.status)
                n = n.next


    def addRFCEnd(self, pier_name, hostname, port, cookie):
        '''
        Adds a RFC server to the end of the linked list
        '''
        newNode = Node(pier_name, hostname, port, cookie)
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


        #This block handles the clients REGISTER request.

        if parsed[0] == 'REGISTER':
            # For a server who does not yet have a cookie
            if parsed[-1] == 'None':
                linkedRFCServers.addRFCEnd(parsed[1], parsed[3], parsed[5], linkedRFCServers.curr_cookie)
                trans_string = 'REGISTER {} OK\nCOOKIE {}\nTTL {}\nREG-NUM {}\n'.format(parsed[1], linkedRFCServers.curr_cookie, str(7200), str(1))
                self.request.sendall(trans_string.encode())
                linkedRFCServers.curr_cookie += 1
            # All other servers will have a cookie
            else:
                # Resets attributes for the re-registered server since TTL will be
                # less than 0 and status will be active should a peer need to re-register
                reRegInfo = linkedRFCServers.reRegisterRFC(int(parsed[-1]))
                trans_string = 'REGISTER {} OK\nCOOKIE {}\nTTL {}\nREG-NUM {}\n'.format(parsed[1], str(parsed[-1]), str((reRegInfo[0]-datetime.datetime.now()).total_seconds()), reRegInfo[1])
                self.request.sendall(trans_string.encode())



        #This block will handle the clients LEAVE request.

        elif parsed[0] == 'LEAVE':
            # If the server has no cookie they cannot leave because they have
            # not registered
            if parsed[-1] == 'None':
                trans_string = 'LEAVE {} FAILED\nHOST {}\nPORT {}\nHOST is not registered, invoke REGISTER to register host.'.format(parsed[1], parsed[3], parsed[5])
                self.request.sendall(trans_string.encode())
            # If a cookie exists, set the status and TTL of the exiting server
            else:
                leaveInfo = linkedRFCServers.leaveRFC(int(parsed[-1]))
                trans_string = 'LEAVE {} OK\nHOST {}\nPORT {}\nTTL {}\nSTATUS {}\n'.format(parsed[1], parsed[3], parsed[5], leaveInfo[0], leaveInfo[1])
                self.request.sendall(trans_string.encode())






def agent():
    while True:
        time.sleep(5)
        linkedRFCServers.walkList()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    '''
    Class to create the threaded TCP server.
    '''
    pass

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
    # agent_thread = threading.Thread(target=agent)
    # agent_thread.start()
    # exit the server thread when the main thread terminates
    server_thread.daemon = False
    server_thread.start()
