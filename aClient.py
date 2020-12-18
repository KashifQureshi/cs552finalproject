'''
Created on Oct 24, 2020

@author: Kashif
'''
import socket
import time
import sys

HOST = input("What IP would you like to connect to? Type d for ilab1: ")
PORT = 6000

# From testing, using small packet sizes skews results when the bandwidth is really high.  Bumping it up by multiplying by ten solves this.
# Sending more packets might also solve this issue.

multiplierCheck = ""
while(True):
    multiplierCheck = input("Is this supposed to be a high bandwidth connection? Y/N: ")
    multiplierCheck = multiplierCheck.upper()
    if(multiplierCheck == "Y" or multiplierCheck == "N"):
        break
if(multiplierCheck == "Y"):
    multiplier = 10
else:
    multiplier = 1
    
if(HOST == "d"):
    HOST = "128.6.4.101"


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Attempts to open a socket to a waiting server.  Fails gracefully if the server is not hosting.
                try:
                    sock.connect((HOST,PORT))
                except Exception as er:
                    print("Error occurred: " + str(er))

                packet = "";
                beginning = time.time()
                measurements = []          
                ADRlist = []

                # 100 packet sizes are received from the client
                for runs in range(100):
                    packetSize = (1460*multiplier) * (runs+1)
                    print("Run number: " + str(runs))
                    print("Packet Size: " + str(packetSize))
                    measuredPacketLength = 0
                    
                    # A packet train of five packet pairs is sent in this loop
                    for runAtThisSize in range(5):
                        for i in range(2):
                            # From initial testing, sometimes the size from recv() can vary.  This ensures it doesn't stop too early
                            while(measuredPacketLength < packetSize):
                                packet = sock.recv(packetSize-measuredPacketLength)
                                measuredPacketLength += len(packet)
                            if(i == 0):
                                initialTime = time.time()
                                # This and the print statement in else were used to initially see if packets were being sent correctly print("Finished receiving first packet")
                                measuredPacketLength = 0
                                if(runAtThisSize == 1):
                                    trainStart = time.time()
                            else:
                                secondTime = time.time()
                                # print("Finished receiving second packet")
                                measuredPacketLength = 0

                        dispersion = secondTime-initialTime
                        print("Time difference: " + str(dispersion))
                        # On a rare occasion, dispersion is reported as 0.  Likely a result of not taking timestamps at the hardware level.
                        # Dividing by 0 is impossible though so 
                        if(dispersion > 0):
                            speed = round((packetSize/125000)/dispersion)
                            print(str(speed) + " Mbps")
                            measurements.append(speed)
                        else:
                            print("Crisis")
                        print()                
                    trainEnd = time.time()
                    trainDispersion = trainEnd-trainStart
                    cumulativePacketSize = packetSize*9
                    if(trainDispersion > 0):
                        ADRlist.append(round((cumulativePacketSize/125000)/trainDispersion))
                measurements.sort()
                currentNumber = 0
                mode = 0
                count = 0
                longestCount = 0
                total = 0
                
                for number in measurements:
                    total += number
                    
                mean = total / len(measurements)
                total = 0
                ADRlist.sort()
                
                # This loop sums all the values of the packet train dispersions and finds the mode of them
                
                for number in ADRlist:
                    if(number != currentNumber):
                        # Nicer output, but not useful for pasting into Excel: print("Counted: " + str(count) + " instances of " + str(currentNumber))
                        print(str(currentNumber) + " " + str(count))
                        if(count > longestCount):
                            mode = currentNumber
                            longestCount = count
                        currentNumber = number
                        count = 0
                    count += 1
                    total += number

                print("Mode from packet train dispersions: " + str(mode))
                print("ADR: " + str(total/len(ADRlist)))
                print("Mean of all measurements: " + str(mean))

                currentNumber = 0
                count = 0
                longestCount = 0
                mode = 0

                # This loop finds the link capacity by finding the mode from the set of numbers greater than the mean of the packet pair bandwidth measurements

                for number in measurements:
                    if(number != currentNumber):
                        # Nicer output, but not useful for pasting into Excel: print("Counted: " + str(count) + " instances of " + str(currentNumber))
                        print(str(currentNumber) + " " + str(count))
                        if(count >= longestCount and currentNumber > mean):
                            mode = currentNumber
                            longestCount = count
                        currentNumber = number
                        count = 0
                    count += 1
                print("Link capacity rated at: " + str(mode))
