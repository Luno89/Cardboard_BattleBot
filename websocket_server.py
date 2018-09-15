from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from pyA20.gpio import gpio
from pyA20.gpio import port
import json
import time

leftPort = port.PG7
rightPort = port.PG6

@staticmethod
def setMotorsClockWise():
    global leftPort
    global rightPort
    gpio.output(leftPort, gpio.LOW)
    gpio.output(rightPort, gpio.HIGH)

@staticmethod
def setMotorsCounterClockWise():
    global leftPort
    global rightPort
    gpio.output(leftPort, gpio.HIGH)
    gpio.output(rightPort, gpio.LOW)

@staticmethod
def stopMotors():
    global leftPort
    global rightPort
    gpio.output(leftPort, gpio.LOW)
    gpio.output(rightPort, gpio.LOW)

class SimpleEcho(WebSocket):

    def handleMessage(self):
        print("I am in the handle method")
        self.sendMessage(self.data)
        print("I sent the message")
        try:
            controller_json = json.loads(self.data)
            print("I am loading json")
            speed = controller_json['speed']
            direction = controller_json['direction']
            if (speed == 0 & direction == 0):
                gpio.output(leftPort, gpio.LOW)
    	        #gpio.output(rightPort, gpio.LOW)
            elif (speed == 0 & direction < 0):
                gpio.output(leftPort, gpio.HIGH)
                #setMotorsClockWise()
            elif (speed == 0 & direction > 0):
                gpio.output(leftPort, gpio.HIGH)
                #gpio.output(rightPort, gpio.LOW)
        except :
            print("something bad happened : " + sys.exc_info()[0])
        # echo message back to client
        #self.sendMessage(self.data)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


server = SimpleWebSocketServer('', 8000, SimpleEcho)
gpio.init()
gpio.setcfg(leftPort, gpio.OUTPUT)
gpio.setcfg(rightPort, gpio.OUTPUT)

#blink
#for x in range(0, 4):
#    gpio.output(leftPort, gpio.HIGH)
#    time.sleep(2)
#    gpio.output(leftPort, gpio.LOW)
#    time.sleep(1)
#gpio.output(rightPort, gpio.LOW)

server.serveforever()
