'''
Created on Oct 24, 2020

@author: Kashif
'''
import socketserver
import socket
import time

class MyTCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
        

        '''
        Legacy code from testing for raw TCP throughput
        file = open(r"fileTransfer.zip", "rb")
        data = file.read(75000)
        while(data):
            print("sending...")
            self.connection.send(data)
            data = file.read(75000)
        print("finished sending")
        self.connection.shutdown(socket.SHUT_WR)
        file.close();
        '''

        print("Starting to send ")
        packetSize = 1460
        
        # Sends 100 different packet sizes in trains of five packet pairs
        
        for runs in range(100):
            packetSize = (1460 * multiplier) * (runs+1)
            for runAtThisSize in range(5):
                # Doesn't appear to be necessary time.sleep(0.1)
                for i in range(2):
                    self.connection.send(bytes(packetSize))

        self.connection.shutdown(socket.SHUT_WR)

    def setMultiplier(number):
        global multiplier
        multiplier = number


if __name__ == "__main__":
    # From testing, using small packet sizes skews results when the bandwidth is really high.  Bumping it up by multiplying by ten solves this.
    # Sending more packets might also solve this issue.
        
    while(True):
        multiplierCheck = input("Is this supposed to be a high bandwidth connection? Y/N: ")
        multiplierCheck = multiplierCheck.upper()
        if(multiplierCheck == "Y" or multiplierCheck == "N"):
            break
    if(multiplierCheck == "Y"):
        MyTCPHandler.setMultiplier(10)
    else:
        MyTCPHandler.setMultiplier(1)
        
    HOST, PORT = "0.0.0.0", 6000
    socketserver.TCPServer((HOST, PORT), MyTCPHandler).serve_forever()
