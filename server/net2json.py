from pysnmp.hlapi import *
from time import sleep
import simplejson as json

DELAY = 10

# Thanks for the accepted answer from http://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
# It works wonderfully in this scenario
class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

def getData(ip, port):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('cacti', mpModel=0),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity('IF-MIB', 'ifSpeed', port)),
               ObjectType(ObjectIdentity('IF-MIB', 'ifInOctets', port)),
               ObjectType(ObjectIdentity('IF-MIB', 'ifOutOctets', port)))
    )
    return varBinds

# Feed this an IP, the interface number, and the time to wait to collect data,
# and it will reutrn the upload percent utilization, download percent utilization,
# and also the link speed in bits per second.
def collectData(ip, interface, delay):
    up = -1
    down = -1
    while(up < 0 and down < 0):
        begin = getData(ip, interface)
        sleep(delay)
        end = getData(ip, interface)
        up = ((int(end[1][1]) - int(begin[1][1])) * 8 * 100) / (DELAY * int(begin[0][1]))
        down = ((int(end[2][1]) - int(begin[2][1])) * 8 * 100) / (DELAY * int(begin[0][1]))
    return up, down, int(begin[0][1])

up, down, speed = collectData('128.153.145.251', 1, 10)
print("Speed: " + str(speed) + "b/s")
print("Percent upload used: " + str(up) + "%")
print("Percent download used: " + str(down) + "%")

output = {}

interface = {}
interface["upload"] = up
interface["download"] = down
interface["speed"] = speed
output["oitlink"] = interface

outputOb = Object()
outputOb.data = output

print (outputOb.toJSON())
file = open("net.json", 'w')
file.write(outputOb.toJSON())
