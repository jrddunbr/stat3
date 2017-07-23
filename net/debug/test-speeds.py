from pysnmp.hlapi import *
from time import sleep, clock

DELAY = 2 # seconds

def getData(ip, port): # returns speed, in, out
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
                CommunityData('cacti'),
                #CommunityData('cacti', mpModel=0),
                UdpTransportTarget((ip, 161)),
                ContextData(),
                ObjectType(ObjectIdentity('IF-MIB', 'ifSpeed', port)),
                ObjectType(ObjectIdentity('IF-MIB', 'ifHCInOctets', port)),
                ObjectType(ObjectIdentity('IF-MIB', 'ifHCOutOctets', port)))
                #ObjectType(ObjectIdentity('IF-MIB', 'ifInOctets', port)),
                #ObjectType(ObjectIdentity('IF-MIB', 'ifOutOctets', port)))
        )
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        pass
    data = {}
    data["speed"] = int(varBinds[0][1])
    data["in"] = int(varBinds[1][1])
    data["out"] = int(varBinds[2][1])
    return data

def calcSpeed(first, second, speed, delay):
    ret = 0
    try:
        ret = ((int(second) - int(first)) * 8 * 100) / (delay * speed)
    except ZeroDivisionError:
        ret = 0
    return ret

in_table = []
out_table = []
calcd_table = []

first = clock();
for i in range(1,4):
    print("SWM{}".format(i), end="", flush=True)
    sw_table = []
    for j in range(1,25):
        print(".", end="", flush=True)
        sw_table.append(getData("128.153.145.25{}".format(i), j))
    in_table.append(sw_table)
    print()
second = clock();

sleep(DELAY)

for i in range(1,4):
    print("SWM{}".format(i), end="", flush=True)
    sw_table = []
    for j in range(1,25):
        print(".", end="", flush=True)
        sw_table.append(getData("128.153.145.25{}".format(i), j))
    out_table.append(sw_table)
    print()

if True:
    for i in range(1,4):
        sw_table = []
        print ("For switch SWM{}:".format(i))
        for j in range(1,25):
            before = in_table[i-1][j-1]
            after = out_table[i-1][j-1]
            data = {}
            data["in"] = calcSpeed(before["in"], after["in"], before["speed"], DELAY+(second-first))
            data["out"] = calcSpeed(before["out"], after["out"], before["speed"], DELAY+(second-first))
            data["speed"] = before["speed"]
            title = "No Link"
            if(before["speed"] == 1000000000):
                title = "Gigabit"
            elif(before["speed"] == 100000000):
                title = "100mb/s"
            elif(before["speed"] == 10000000):
                title = "10mb/s"
            elif(before["speed"] == 0):
                title = "No Link"
            else:
                title = "ACK"
            print("Port {}: Ingress: {}% Egress: {}% Link Speed: {}".format(j, int(data["in"]), int(data["out"]), title))
            sw_table.append(data)
        calcd_table.append(sw_table)

if True: # Port Usage/Speed Table
    for i in range(1,4):
        sw_table = []
        print ("SWM{}: ".format(i), end="", flush=True)
        for j in range(1,25):
            speed = in_table[i-1][j-1]["speed"]
            title = "  "
            if(speed == 1000000000):
                title = "■ "
            elif(speed == 100000000):
                title = "◨ "
            elif(speed == 10000000):
                title = "◫ "
            elif(speed == 0):
                title = "□ "
            else:
                title = "▩ "
            print (title, end="", flush=True)
        print()
