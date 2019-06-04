import socket
import threading
import socketserver
import datetime
from imports.linked import Node, LinkedList
from imports.agent import agent


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        '''
        Function responsible for handling the incoming client requests
        '''
        data = self.request.recv(1024).decode()
        parsed = data.split()
        print(data)


        #This block handles the clients REGISTER request.-----------------------

        if parsed[0] == 'REGISTER':
            # For a server who does not yet have a cookie
            if parsed[-1] == 'None':
                linkedRFCServers.addPierEnd(parsed[1], parsed[3], parsed[5], linkedRFCServers.curr_cookie)
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

        #-----------------------------------------------------------------------


        #This block will handle the clients LEAVE request.----------------------

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

        #-----------------------------------------------------------------------


        # This block will handle the clients PQUERY request.--------------------

        elif parsed[0] == 'PQUERY':
            if parsed[-1] == 'None':
                trans_string = 'PQUERY {} FAILED\nHOST {}\nPORT {}\nHOST is not registered, invoke REGISTER to query RS.'.format(parsed[1], parsed[3], parsed[5])
                self.request.sendall(trans_string.encode())
            else:
                piers = linkedRFCServers.pqueryRFC(int(parsed[-1]))
                if piers is not None:
                    trans_string = 'PQUERY {} OK\nHOST {}\nPORT {}\nPIERS:'.format(parsed[1], parsed[3], parsed[5])
                    for pier in piers:
                        trans_string += pier
                else:
                    trans_string = 'PQUERY {} OK\nHOST {}\nPORT {}\nPIERS\n{}'.format(parsed[1], parsed[3], parsed[5], 'No-piers-active')

                self.request.sendall(trans_string.encode())

        elif parsed[0] == 'RFCINDEX':
            print('got')

        #-----------------------------------------------------------------------


        # This block will handle the clients KEEPALIVE request.-----------------

        elif parsed[0] == 'KEEPALIVE':
            pass

        #-----------------------------------------------------------------------


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    '''
    Class to create the threaded TCP server.
    '''
    pass


if __name__ == "__main__":
    HOST, PORT = socket.gethostbyname(socket.gethostname()), 9999
    linkedRFCServers = LinkedList()
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    # Sample nodes
    linkedRFCServers.addPierEnd('P2', socket.gethostbyname(socket.gethostname()), 9999, 2)
    linkedRFCServers.addPierEnd('P1', socket.gethostbyname(socket.gethostname()), 9999, 3)
    linkedRFCServers.addPierEnd('P3', socket.gethostbyname(socket.gethostname()), 9999, 4)
    ip, port = server.server_address
    # start a thread with the server.
    # the thread will then start one more thread for each request.
    server_thread = threading.Thread(target=server.serve_forever)
    agent_thread = threading.Thread(target=agent, args=(linkedRFCServers,))
    agent_thread.start()
    server_thread.daemon = False
    server_thread.start()
