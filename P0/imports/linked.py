import socket
import threading
import socketserver
import datetime
import time

class Node():
    '''
    Class that creates a new node for an RFC with the payload information.
    '''
    def __init__(self, RFCNum, RFCTitle, hostname, port):
        self.RFCNumb = RFCNum
        self.RFCTitle = RFCTitle
        self.hostname = hostname
        self.port = port
        self.TTL = datetime.datetime.now() + datetime.timedelta(0, 7200)
        self.next = None

class LinkedList():
    '''
    Class that contains the payloads of the RFC servers. The class is
    initialized at the start of this script which starts the RS server.
    '''
    def __init__(self):
        self.startNode = None

    def addRFCRecordEnd(self, RFCNumb, RFCTitle, hostname, port):
        '''
        Adds an RFC reccord to the linked list
        '''
        newNode = Node(RFCNumb, RFCTitle, hostname, port)
        if self.startNode is None:
            self.startNode = newNode
            return
        n = self.startNode
        while n.next is not None:
            n = n.next
        n.next = newNode
