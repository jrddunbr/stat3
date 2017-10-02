#!/usr/bin/python3
#
# This is the main server application. This is run and then opens some threads
# so that it may run some server tasks in parallel

# Debugging Constants
DEBUG_NET = True # print network data packet and source IP

# Program Constants - these configure operation of the server
# TCP PORTS
TCP_SERVER_PORT = 2204
TCP_SENSOR_PORT = 2206
# UDP PORTS
UDP_SERVER_PORT = 2204
UDP_BATTERY_PORT = 2205
UDP_SENSOR_PORT = 2206
UDP_NETWORK_PORT = 2207
# PATHS
WEB_PATH = "/srv/http" # location of webserver directory (NO trailing slash)
# FLAGS
ENABLE_TCP = True # For compatibility with TCP only connections on certain devices
ENABLE_UDP = True # NOT recommended to set to false
ENABLE_REST = True # Enables ro REST api at $WEB_PATH/api

# imports in no particular order
import threading
import socket
import time
import os
import shutil
import datetime
from enum import Enum
import simplejson as json

#global variables
whoistable = {} # Stores whois information for servers
whitesense = {} # Stores sensor node whitelist
whitebatt = {} # Stores battery node whitelist
whitenet = {} # Stores network node whitelist

servers = {} # Stores ServerItems
batteries = {} # Stores BatteryItems
sensors = {} # Stores SensorItems
networks = {} # Stores NetworkItems
maintainers = {} # Stores Maintainer Items

class SensorType(Enum):
    RAW = 1; # RAW data (direct display plus special character removal)
    THERMAL = 2; # Thermal information from a 10K thermal resistor, as raw ADC from 0 to 1023
    BOOLEAN = 3; # Boolean information

class ServerItem:
    def __init__(self, name):
        self.name = name
        self.keys = {}
    def addKey(self, key, value):
        self.keys[key] = value;
    def getKey(self, keyname):
        if keyname in self.keys:
            return self.keys[keyname]
        else:
            return ""
    def getName(self):
        return self.name

class BatteryItem:
    def __init__(self, name, percent, timeleft):
        self.name = name
        self.percent = percent
        self.timeleft = timeleft

    def getName(self):
        return self.name
    def getPercent(self):
        return self.percent
    def getTimeLeft(self):
        return self.timeleft

class SensorItem:
    def __init__(self, name, sensortype, value):
        self.name = name
        self.type = sensortype
        self.value = value
        self.kelvin = -1.0
    def getName(self):
        return self.name
    def getType(self):
        return self.sensortype
    def getValue(self):
        return self.value
    def getKelvin(self):
        if self.sensortype == SensorType.THERMAL:
            if self.kelvin == -1.0:
                raw = self.value
                temp = math.log(10000 * ((1024.0 / raw) - 1))
                self.kelvin = 1 / (0.001129148 + (0.000234125 * temp) + (0.0000000876741 * temp * temp * temp));
                return self.kelvin
            else:
                return self.kelvin
        else:
            return -1

class NetworkInterface:
    def __init__(self, switch, port):
        self.name = name
        self.switch = switch
        self.port = port
        self.up = 0
        self.down = 0
    def setUp(self, speed):
        self.up = speed
    def setDown(self, speed):
        self.down = speed
    def getSwitch(self):
        return self.switch
    def getPort(self):
        return self.port
    def getUp(self):
        return self.up
    def getDown(self):
        return self.down

# Thanks for the accepted answer from http://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
# It works wonderfully in this scenario
class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

# Cleans all the shit that people put into this application.. *cough*Grissess*cough*
def sanitize(input):
    return input.replace('\\', '').replace('/', '').replace('<', '').replace('>', '').replace('?', '').replace('.py', '').replace('\n','').replace('\r','')

def udp_server():
    print ("starting server server on UDP port " + str(UDP_SERVER_PORT))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", UDP_SERVER_PORT))
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            # get rid of all path or HTML injections
            message = sanitize(data.decode("utf-8"))
            if DEBUG_NET: print ("recieved server message: " + message + " from " + str(addr[0]))
            try:
                name = whoistable[addr[0]]
            except:
                name = "grm plz stahp"
            if name not in servers:
                s = ServerItem(name)
            try:
                serverkey = message.split("|")
                s.addKey(serverkey[0], serverkey[1])
                servers[name] = s
            except:
                print("Malformed packet recieved from " + addr[0] + " on udp servers server, containing the string " + message)
        except:
            pass # well dang GRM

def tcp_server():
    print ("starting server server on TCP port " + str(TCP_SERVER_PORT))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", TCP_SERVER_PORT))
    sock.listen(1)
    while True:
        try:
            conn, addr = sock.accept()
            # get rid of all path or HTML injections
            data = conn.recv(1024)
            if data:
                # get rid of all path or HTML injections
                message = sanitize(data.decode("utf-8"))
                if DEBUG_NET: print ("recieved server message: " + message + " from " + str(addr[0]))
                try:
                    name = whoistable[addr[0]]
                except:
                    name = "grm plz stahp"
                if name not in servers:
                    s = ServerItem(name)
                try:
                    serverkey = message.split("|")
                    s.addKey(serverkey[0], serverkey[1])
                    servers[name] = s
                except:
                    print("Malformed packet recieved from " + addr[0] + " on tcp servers server, containing the string " + message)
        except Exception as e:
            print (e)
            pass # well dang GRM

def udp_battery():
    print ("starting battery server on UDP port " + str(UDP_BATTERY_PORT))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", UDP_BATTERY_PORT))
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = sanitize(data.decode("utf-8"))
            if DEBUG_NET: print ("recieved battery message: " + message + " from " + str(addr[0]))
            try:
                rec = message.split("|")
                name = rec[0]
                percent = rec[1]
                timeleft = rec[2]
                batteries[name] = BatteryItem(name, percent, timeleft)
            except:
                print("Malformed packet recieved from " + addr[0] + " on udp battery server, containing the string " + message)
        except:
            pass # again, well dang GRM

def udp_sensor():
    print ("starting sensor server on UDP port " + str(UDP_SENSOR_PORT))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", UDP_SENSOR_PORT))
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = sanitize(data.decode("utf-8"))
            if DEBUG_NET: print ("recieved sensor message: " + message + " from " + str(addr[0]))
            try:
                rec = message.split("|")
                name = rec[0]
                sensortype = rec[1]
                value = rec[2]
                stp = SensorType.RAW
                if sensortype == "THERMAL":
                    stp = SensorType.THERMAL
                if sensortype == "BOOLEAN":
                    stp = SensorType.BOOLEAN
                if sensortype == "IBOOLEAN":
                    stp = SensorType.IBOOLEAN
                sensors[name] = SensorItem(name, stp, value)
            except:
                print("Malformed packet recieved from " + addr[0] + " on udp sensor server, containing the string " + message)
        except:
            pass # again, well dang GRM

def udp_network():
    print ("starting sensor server on UDP port " + str(UDP_NETWORK_PORT))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", UDP_NETWORK_PORT))
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = sanitize(data.decode("utf-8"))
            if DEBUG_NET: print ("recieved sensor message: " + message + " from " + str(addr[0]))
            try:
                rec = message.split("|")
                switch = rec[0]
                port = rec[1]
                up = rec[2]
                down = rec[3]
                networks[switch][port] = NetworkInterface(switch, port)
                networks[switch][port].setUp(up)
                networks[switch][port].setDown(down)
            except:
                print("Malformed packet recieved from " + addr[0] + " on udp network server, containing the string " + message)
        except:
            pass # again, well dang GRM

def reporting():
    while(True):
        output = Object()
        output.data = servers
        report_file = open(WEB_PATH + '/manage.json', 'w')
        report_file.write(output.toJSON())
        report_file.close()
        time.sleep(5)

 ##################
# Main Exec Thread #
 ##################

try:
    # Read whitelist files and server whois so that we can get some data
    whoisfile = open('configs/server-whois.txt', 'r')
    for line in whoisfile:
        if '|' in line:
            spline = line.split("|")
            whoistable[spline[0]] = spline[1].strip()
    battfile = open('configs/battery-whitelist.txt', 'r')
    for line in whoisfile:
        if '|' in line:
            spline = line.split("|")
            whitebatt[spline[0]] = spline[1].strip()
    sensefile = open('configs/sensor-whitelist.txt', 'r')
    for line in whoisfile:
        if '|' in line:
            spline = line.split("|")
            whitesense[spline[0]] = spline[1].strip()
    netfile = open('configs/network-whitelist.txt', 'r')
    for line in whoisfile:
        if '|' in line:
            spline = line.split("|")
            whitenet[spline[0]] = spline[1].strip()
    maintainerfilecontents = ""
    maintainersfile = open('users/maintainers.json','r')
    for line in whoisfile:
        maintainerfilecontents += line
    try:
        maintainers = json.loads(maintainersfilecontents)
    except:
        pass
except Exception as e:
    # ACK!!! Dang users!
    print("Something happened wihile reading whitelists and maintainers")
    print(e)
    exit(0)

# Start all of the server threads
t1 = threading.Thread(target=udp_server)
t1.start()
t2 = threading.Thread(target=udp_battery)
t2.start()
t3 = threading.Thread(target=udp_sensor)
t3.start()
t4 = threading.Thread(target=udp_network)
t4.start()
t5 = threading.Thread(target=reporting)
t5.start()
if ENABLE_TCP:
    t6 = threading.Thread(target=tcp_server)
    t6.start()
    #t7 = threading.Thread(target=tcp_sensor)
    #t7.start()
    pass
