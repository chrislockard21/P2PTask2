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
        data = self.request.recv(8192).decode()
        parsed = data.split()

        hostname = parsed[2]
        port = parsed[4]

        if parsed[0] == 'RFCINDEX' and parsed[1] == 'OK':
            if len(parsed) > 6 and parsed[-1] != 'No-List':
                RFC_current = linkedRFCIndex.RFCsActive()
                print(RFC_current)
                i = 7
                while i < len(parsed):
                    RFC = parsed[i].split('|')
                    if RFC[0] not in RFC_current:
                        linkedRFCIndex.addRFCRecordEnd(RFC[0], RFC[1], RFC[2], RFC[3])
                    else:
                        continue
                    i += 1

            linkedRFCIndex.walkList()

        elif parsed[0] == 'RFCINDEX':
            print(data)
            trans_string = 'RFCINDEX OK\nHOST {}\nPORT {}\nRFCs\n'.format(hostname, port)
            RFC = linkedRFCIndex.RFCIndex()
            for R in RFC:
                trans_string += R
            self.request.sendall(trans_string.encode())

        elif parsed[0] == 'SEEKRFCS':
            RFC_staging = linkedRFCIndex.RFCIndex()
            for R in RFC_staging:
                RFC = R.split('|')
                if RFC[2] != HOST:
                    trans_string = 'GETRFC\nHOST {}\nPORT {}\n{}'.format(HOST, PORT, RFC[0]+ ' ' +RFC[1])
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.connect((RFC[2], int(RFC[3])))
                        sock.sendall(trans_string.encode())
                        with open('/var/opt/RFCs/' + RFC[0]+RFC[1], 'w') as f:
                            while True:
                                print('receiving data...')
                                data = sock.recv(1024).decode()
                                if not data:
                                    print('done receiving.')
                                    break
                                # write data to a file
                                f.write(data)

        elif parsed[0] == 'GETRFC':
            print(data)
            parsed = data.split()
            filename = '/var/opt/RFCs/' + parsed[-2] + parsed[-1]
            f = open(filename, 'rb')
            l = f.read(1024)
            print('sending data...')
            while (l):
                self.request.send(l)
                l = f.read(1024)
            f.close()
        
        



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
    RFCPath = '/var/opt/RFCs'

    RFCfiles = [f for f in os.listdir(RFCPath) if os.path.isfile(os.path.join(RFCPath, f))]
    if len(RFCfiles) > 0:
        for f in RFCfiles:
            if f[:1] != '.':
                number = f[:4]
                title = f[4:]
                linkedRFCIndex.addRFCRecordEnd(number, title, HOST, PORT)
    
    ip, port = server.server_address

    # start a thread with the server.
    # the thread will then start one more thread for each request.
    server_thread = threading.Thread(target=server.serve_forever)
    # agent_thread = threading.Thread(target=agent)
    # agent_thread.start()
    # exit the server thread when the main thread terminates
    server_thread.daemon = False
    server_thread.start()
