from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from pyA20.gpio import gpio
from pyA20.gpio import port
import json

leftPort = port.PG7
rightPort = port.PG8

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
        controller_json = json.loads(self.data)
        speed = controller_json['speed']
        direction = controller_json['direction']

        if (speed == 0 & direction == 0):
            stopMotors()
        elif (speed == 0 & direction < 0):
            setMotorsClockWise()
        elif (speed == 0 & direction > 0):
            setMotorsCounterClockWise()

        # echo message back to client
        self.sendMessage(self.data)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


gpio.init()
gpio.setcfg(leftPort, gpio.OUTPUT)
gpio.setcfg(rightPort, gpio.OUTPUT)

server = SimpleWebSocketServer('', 8000, SimpleEcho)
server.serveforever()