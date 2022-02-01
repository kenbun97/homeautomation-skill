from mycroft import MycroftSkill, intent_file_handler
from xml.etree import ElementTree as ET
import socket
from time import sleep

PORT = 5001
BUFFER_SIZE = 1024
CONFIG_FILE = '/home/pi/HomeAuto/tcp_drivers/Config_HomeAuto.xml'
DEVICE_NAME = 'name'
DEVICE_CHANNEL = 'channel'
DEVICE_IP = 'ip'

class HomeAuto:
#{#
    def __init__(self):
    #{#
        self.G_config = self.readConfig(CONFIG_FILE)
    #}#

    def readConfig(self, fileName):
    #{#
        xml = ET.parse(fileName)
        root_element = xml.getroot()
        config = {}

        for child in root_element:
        #{#
            config[child.attrib[DEVICE_NAME]] = {}
            for var in child:
            #{#
                config[child.attrib[DEVICE_NAME]][var.tag] = var.text
            #}#
        #}#
        return config
    #}#

    def sendCommands(self, cIpAddress, message, length):
    #{#
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((cIpAddress, PORT))
        s.send(message)
        data = s.recv(BUFFER_SIZE)
        s.close()
        return data
    #}#

    def buildCommand(self, deviceName, iState):
    #{#
        try:
        #{#
            self.readConfig(CONFIG_FILE)
            if(deviceName in self.G_config):
            #{#
                message = chr((int(self.G_config[deviceName][DEVICE_CHANNEL]) << 1) + iState).encode('ascii')
                self.sendCommands(self.G_config[deviceName][DEVICE_IP], message, 1)
            #}#
            else:
            #{#
                pass
            #}#
        #}#
        except Exception as err:
        #{#
            print(type(err))
            print(err.args)
            print(err)
        #}#
    #}#

    def determineDevice(self, message):
    #{#
        messageString = str(message.data.get('utterances')[0])
        potentialDevices = messageString.split(' ')
        devices = self.G_config.keys()
        for device in devices:
        #{#
            if(device in potentialDevices):
            #{#
                return device
            #}#
        #}#
        return None
    #}#

    def determineState(self, message):
    #{#
        messageString = str(message.data.get('utterances')[0])
        potentialStates = messageString.split(' ')
        states = {'on':1, 'off':0, 'power':1}
        for state in list(states.keys()):
        #{#
            if(state in potentialStates):
            #{#
                return states[state]
            #}#
        #}#
        return None
    #}#
#}#

class Homeautomation(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.home = HomeAuto()

    @intent_file_handler('powerdevice.intent')
    def handle_homeautomation(self, message):
        device = self.home.determineDevice(message)
        state = self.home.determineState(message)
        self.home.buildCommand(device,state)
        self.speak_dialog('homeautomation')
        #sleep(1)
        #self.home.buildCommands('lamp',0)


def create_skill():
    return Homeautomation()



