from pysnmp.hlapi import *
from time import sleep, clock
import simplejson as json

DELAY = 2 # seconds

class Switch:
    def __init__(self, name, ip, ports=24):
        self.name = name
        self.ip = ip
        self.ports = ports

class Port:
    # Centric is true if the port is switch centric
    def __init__(self, centric=False):
        self.centric = centric

def getData(ip, port): # returns speed, in, out
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('cacti', mpModel=0),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity('IF-MIB', 'ifSpeed', port)),
               ObjectType(ObjectIdentity('IF-MIB', 'ifInOctets', port)),
               ObjectType(ObjectIdentity('IF-MIB', 'ifOutOctets', port)))
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

def fetch_data(switches): # dict of switches (as class Switch) as arguemt

    in_table = []
    out_table = []
    calcd_table = []
    swdata = {}
    swtable = []

    first = clock();
    for s in switches:
        #print(switches[s].name, end="", flush=True)
        sw_table = []
        for j in range(1,switches[s].ports+1):
            #print(".", end="", flush=True)
            sw_table.append(getData(switches[s].ip, j))
        in_table.append(sw_table)
        #print()
    second = clock();

    sleep(DELAY)

    for s in switches:
        #print(switches[s].name, end="", flush=True)
        sw_table = []
        for j in range(1,switches[s].ports+1):
            #print(".", end="", flush=True)
            sw_table.append(getData(switches[s].ip, j))
        out_table.append(sw_table)
        #print()

    if True:
        i = 0
        for s in switches:
            sw_table = []
            for j in range(1,switches[s].ports+1):
                centric = False
                before = in_table[i][j-1]
                after = out_table[i][j-1]
                data = {}
                data["name"] = switches[s].name + "_" + str(j)
                for entry in names:
                    #print(data["name"] + " =?= " + entry)
                    if data["name"] == entry:
                        data["name"] = names[entry].name
                        #print(names[entry].name + ": " + str(names[entry].centric))
                        centric = names[entry].centric
                        break
                up = calcSpeed(before["in"], after["in"], before["speed"], DELAY+(second-first))
                down = calcSpeed(before["out"], after["out"], before["speed"], DELAY+(second-first))
                if centric: # if we are switch centric, swap the values
                    data["upload"] = down
                    data["download"] = up
                else: # if we are host centric, leave it be
                    data["upload"] = up
                    data["download"] = down
                data["speed"] = before["speed"]
                #swdata[data["name"]] = data
                if data["speed"] > 0:
                    swtable.append(data)
                #sw_table.append(data)
            #calcd_table.append(sw_table)
            i = i+1
    return swtable#swdata#calcd_table

def fetch_switches(switches):
    pass

# Thanks for the accepted answer from http://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
# It works wonderfully in this scenario
class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=2)

def write_json(data):
    thing = {}
    thing["network"] = data
    output = Object()
    output.data = thing
    percentfile = open("../web/net.json", 'w')
    percentfile.write(output.toJSON())
    percentfile.close()

############ MAIN PART #####

switches = {}
names = {}

whoisfilename = "net-whois.txt"

wfile = open(whoisfilename, "r")

for line in wfile:
    entries = line.split("|")
    size = len(entries)
    port = Port()
    if size == 2:
        port.name = entries[1]
        names[entries[0]] = port
    elif size == 3:
        port.name = entries[1]
        port.centric = entries[2].find("SC") != -1
        names[entries[0]] = port
    elif size == 5:
        port.name = entries[1]
        port.centric = entries[2].find("SC") != -1
        names[entries[0]] = port

swm1 = Switch("swm1", "128.153.145.251")
swm2 = Switch("swm2", "128.153.145.252")
swm3 = Switch("swm3", "128.153.145.253")

switches[swm1.name] = swm1
switches[swm2.name] = swm2
switches[swm3.name] = swm3

while True:
    data = fetch_data(switches)
    write_json(data)
    data = {}
