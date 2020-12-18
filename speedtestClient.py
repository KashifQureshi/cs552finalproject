'''
Created on Sep 30, 2020

@author: Kashif 
'''

import kivy
import math
import socket
import time

kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class SpeedTest(GridLayout):

    downloadResult = Label(text = 'Will be shown here')
    errorMessage = Label(text = '')
    # Initial testing for upload rate didn't work.  Sending data made the GUI freeze.  I'm likely just missing something simple but for now I'll have to return to it later.
    # uploadResult = Label(text = 'Upload speed')
    # uploadResult.text = "Coming in a future update"

    def runTest(self, instance):
            # This doesn't actually update the GUI.  Why?
            self.downloadResult.text = "Connecting to server"
            #self.uploadResult.text = "Will be tested after download speed"
            PORT = 6000
            measurements = []
            ADRlist = []
            
            # Attempts to connect to a server running on an ilab machine.  Probably a better idea to run the server on AWS in the future
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                try:
                    HOST = socket.gethostbyname("128.6.4.101") #ilab1 
                    sock.connect((HOST,PORT))
                except Exception:
                    try:
                        HOST = socket.gethostbyname("128.6.4.102") #ilab2
                        sock.connect((HOST,PORT))
                    except Exception:
                        try:
                            HOST = "128.6.4.103" #ilab3
                            sock.connect((HOST, PORT))
                        except Exception:
                            try:
                                HOST = "128.6.4.28" #ilab4
                                sock.connect((HOST, PORT))
                            except Exception:
                                print("There is no server running on ilab, please start it before trying to run the speedtest")
                                self.errorMessage.text=" There is no server running on ilab,\n please start it before trying to run the speedtest"
                                return
                self.downloadResult.text = "Calculating...please wait"
                #self.uploadResult.text = "Coming in a future update"
                packetSize = 1460
                totalPackets = 0
                packet = "";
                
                # Here 100 different packet sizes are received in trains of five packet pairs 
                for runs in range(100):
                    packetSize = (1460) * (runs+1)
                    print("Run number: " + str(runs))
                    print("Expected packet size: " + str(packetSize))
                    measuredPacketLength = 0
                    for runAtThisSize in range(5):
                        for i in range(2):
                            totalPackets += packetSize
                            while(measuredPacketLength < packetSize):
                                packet = sock.recv(packetSize-measuredPacketLength)
                                measuredPacketLength += len(packet)
                                #   print("i: " + str(i) + " Measured Packet size: " + str(measuredPacketLength))
                                #   print("Checking received packet size: " + str(len(packet)))

                            if(i == 0):
                                initialTime = time.time()
                                print("Finished receiving first packet")
                                measuredPacketLength = 0
                                if(runAtThisSize == 0):
                                    trainStart = time.time()
                            else:
                                secondTime = time.time()
                                print("Finished receiving second packet")
                                measuredPacketLength = 0

                        dispersion = secondTime-initialTime
                        print("Time difference: " + str(dispersion))     
                        if(dispersion > 0):
                            speed = round((packetSize/125000)/dispersion)
                            print(str(speed) + " Mbps")
                            measurements.append(speed)
                        print() 
                    trainEnd = time.time()
                    trainDispersion = trainEnd-trainStart
                    cumulativePacketSize = packetSize*9
                    if(trainDispersion > 0):
                        ADRlist.append( round((cumulativePacketSize/125000)/trainDispersion))

                measurements.sort()
                currentNumber = 0
                mode = 0
                count = 0
                longestCount = 0
                total = 0
                for number in measurements:
                    total += number
                mean = math.floor(total / len(measurements))
                total = 0
                
                adrCount = 0
                adrMode = 0
                ADRlist.sort()
                adrCurrent = 0
                
                # This loop sums up the train dispersion rates and finds the mode of them
                for number in ADRlist:
                    if(number != adrCurrent):
                        print(str(adrCount) + " " + str(adrCurrent))
                        if(adrCount > longestCount):
                            adrMode = adrCurrent
                            longestCount = adrCount
                        adrCurrent = number
                        adrCount = 0
                    total += number
                    adrCount += 1
                
                
                print("Train dispersion mode: " + str(adrMode))
                print("Mean of measurements: " + str(mean))
                print("ADR: " + str(total/len(ADRlist)))
                print()
                
                longestCount = 0
                
                # This loop finds the link capacity by finding the mode from the set of numbers greater than the mean of the packet pair bandwidth measurements
                for number in measurements:
                    if(number != currentNumber):
                        print(str(count) + " " + str(currentNumber))
                        if(count > 3 and count > longestCount and currentNumber >= mean):
                            mode = currentNumber
                            longestCount = count
                        currentNumber = number
                        count = 0
                    count += 1
                print("Mode of measurements: " + str(mode))
                self.downloadResult.text = "Your download speed is: " + str(mode) + "Mbps"


    def __init__(self, **kwargs):
        super(SpeedTest, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='Download Speed'))
        self.add_widget(self.downloadResult)
        self.add_widget(self.errorMessage)
     #   self.add_widget(Label(text='Upload Speed'))
     #   self.add_widget(self.uploadResult)
        button = Button(text='Run speedtest!')
        button.bind(on_press=self.runTest)
        self.add_widget(button)
        

class MyApp(App):

    def build(self):
        return SpeedTest()


if __name__ == '__main__':
    MyApp().run()