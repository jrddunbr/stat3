from time import sleep, clock
import simplejson as json
from easysnmp import snmp_get
import threading
import os
import datetime

DELAY = 1 # seconds

switches = {}

ifSpeed32 = "1.3.6.1.2.1.2.2.1.5"
inOctets32 = "1.3.6.1.2.1.2.2.1.10"
outOctets32 = "1.3.6.1.2.1.2.2.1.16"
ifSpeed64 = "1.3.6.1.2.1.31.1.1.1.15"
inOctets64 = "1.3.6.1.2.1.31.1.1.1.6"
outOctets64 = "1.3.6.1.2.1.31.1.1.1.10"

def getData(ip, port): # returns speed, in, out
    data = {}
    data["speed"] = int(snmp_get(ifSpeed64 + "." + port, hostname=ip, community='cacti', version=2).value)
    data["in"] = int(snmp_get(inOctets64 + "." + port, hostname=ip, community='cacti', version=2).value)
    data["out"] = int(snmp_get(outOctets64 + "." + port, hostname=ip, community='cacti', version=2).value)
    return data

def snmpthread(ip, pt, reverse): # Switch IP, port, reversed?
    while 1:
        time = 15 # seconds
        b = getData(ip, str(pt))
        sleep(time)
        e = getData(ip, str(pt))
        speed = b["speed"]
        if speed != 0:
            in2 = (e["in"] - b["in"]) / time * 8 / 1024 / 1024 # Mb/s
            out2 = (e["out"] - b["out"]) / time * 8 / 1024 / 1024 # Mb/s
        else:
            in2 = 0
            out2 = 0
        now = datetime.datetime.now()
        try:
            datafile = open("/opt/stat/data/high/{}-{}-{}:{}-{}".format(now.month, now.day, now.year, ip, pt), "a+")
            if reverse:
                datafile.write("{}:{}:{}-{}-{}-{}\n".format(now.hour, now.minute, now.second, out2, in2, speed))
            else:
                datafile.write("{}:{}:{}-{}-{}-{}\n".format(now.hour, now.minute, now.second, in2, out2, speed))
        except Exception as e:
            print("Error creating log files, {}".format(e))
#####

# main program code

try:
    if not os.path.exists(os.path.dirname("/opt/stat/data/")): # trailing slash is IMPORTANT
        os.makedirs(os.path.dirname("/opt/stat/data/"))
except Exception as e:
    print ("Error creating data logging directory for network statistics")
    exit(0)

try:
    if not os.path.exists(os.path.dirname("/opt/stat/data/high/")):
        os.makedirs(os.path.dirname("/opt/stat/data/high/"))
except:
    print ("Error creating high-resolution data logging directory for network statistics")
    exit(0)

try:
    file = open("switch.conf", 'r')
    i = 1
    for line in file:
        try:
            sub = line.split(":")
            i+=1
            data = {}
            name = sub[0] # name of switch
            data["ip"] = sub[1] # IP in IPv4 format
            data["ports"] = int(sub[2]) # Number of ports on switch
            data["rdir"] = sub[3] # ports on switch which are switch centric, seperated by commas
            switches[name] = data
            # Example:
            #  swm1:1.2.3.4:24:1
        except:
            print("Error on line {} in switch file".format(i))

except:
    print("Error, you need a switch configuration file")
    exit(0)

for switch in switches:
    for port in range(1,switches[switch]["ports"]+1):
        if str(port) in switches[switch]["rdir"].split(","):
            #print("Switch: {} Port: {} Reversed".format(switch, port))
            collect = threading.Thread(target=snmpthread, args=(switches[switch]["ip"], port, True))
            collect.start()
        else:
            #print("Switch: {} Port: {} Normal".format(switch, port))
            collect = threading.Thread(target=snmpthread, args=(switches[switch]["ip"], port, False))
            collect.start()
