import asyncore
import socket

clients = {}
print "Loading server..."
class MainServerSocket(asyncore.dispatcher):
    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('',port))
        self.listen(5)
        print "Server is online."
    def handle_accept(self):
        newSocket, address = self.accept( )
        clients[address] = newSocket
        print "New client from:", address
        SecondaryServerSocket(newSocket)

class SecondaryServerSocket(asyncore.dispatcher_with_send):
    def handle_read(self):
        receivedData = self.recv(8192)
        if receivedData:
            every = clients.values()
            print receivedData
            for one in every:
                one.send(receivedData+'\n')
        else: self.close( )
    def handle_close(self):
        print "Client lost from:", self.getpeername( )
        one = self.getpeername( )
        del clients[one]

MainServerSocket(21567)
asyncore.loop( )
