class LinkedList():
    '''
    Class that contains the payloads of the RFC servers. The class is
    initialized at the start of this script which starts the RS server.
    '''
    def __init__(self):
        '''
        Initializes the LinkedList class.

        payload - data from the RFC server. The general form is a dictionary.
        '''
        self.startNode = None

    def walkList(self):
        '''
        Traverses the linked list providing the payloads for each item in the
        list.
        '''
        if self.startNode is None:
            print('No RFCs to list')
            return
        else:
            n = self.startNode
            while n is not None:
                print(n.payload, ' ')
                n = n.next

    # def addRFCStart(self, payload):
    #     newNode = Node(payload)
    #     newNode.next = self.startNode
    #     self.startNode = newNode

    def addRFCEnd(self, payload):
        '''
        Adds a new RFC to the linked list at the end.

        payload - data from the RFC server. The general form is a dictionary.
        '''
        newNode = Node(payload)
        if self.startNode is None:
            self.startNode = newNode
            return
        n = self.startNode
        while n.next is not None:
            n = n.next
        n.next = newNode


class Node():
    '''
    Class that creates a new node for an RFC with the payload information.
    '''
    def __init__(self, payload):
        '''
        Initializes the RFCNode class.

        payload - data from the RFC server. The general form is a dictionary.
        '''
        self.payload = payload
        self.next = None