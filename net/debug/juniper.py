from easysnmp import snmp_get

DELAY = 1 # seconds

switches = {}

# Good for Juniper EX4500
ifName = "1.3.6.1.2.1.31.1.1.1.1"
ifDescr = "1.3.6.1.2.1.2.2.1.2"
ifHighSpeed = "1.3.6.1.2.1.31.1.1.1.15"
ifHCInOctets = "1.3.6.1.2.1.31.1.1.1.6"
ifHCOutOctets = "1.3.6.1.2.1.31.1.1.1.10"

# Good for TP links
ifSpeed32 = "1.3.6.1.2.1.2.2.1.5"
inOctets32 = "1.3.6.1.2.1.2.2.1.10"
outOctets32 = "1.3.6.1.2.1.2.2.1.16"
ifSpeed64 = "1.3.6.1.2.1.31.1.1.1.15"
inOctets64 = "1.3.6.1.2.1.31.1.1.1.6"
outOctets64 = "1.3.6.1.2.1.31.1.1.1.10"



def getNames(ip):
    ports = []
    for i in range(1, 999):
        res = str(snmp_get(ifDescr + "." + str(i), hostname=ip, community='cacti', version=2).value)
        if not "NOSUCHINSTANCE" in res:
            if "xe" in res or "ge" in res:
                #print ("ID: {} Data: {}".format(i,res))
                ports.append((i, res))
    return ports;

def getJuniperData(ip, pid):
    data = {}
    data["speed"] = int(snmp_get(ifHighSpeed + "." + str(pid), hostname=ip, community='cacti', version=2).value)
    data["in"] = int(snmp_get(ifHCInOctets + "." + str(pid), hostname=ip, community='cacti', version=2).value)
    data["out"] = int(snmp_get(ifHCOutOctets + "." + str(pid), hostname=ip, community='cacti', version=2).value)
    return data

def getTPData(ip, port): # returns speed, in, out
    data = {}
    data["speed"] = int(snmp_get(ifSpeed64 + "." + port, hostname=ip, community='cacti', version=2).value)
    data["in"] = int(snmp_get(inOctets64 + "." + port, hostname=ip, community='cacti', version=2).value)
    data["out"] = int(snmp_get(outOctets64 + "." + port, hostname=ip, community='cacti', version=2).value)
    return data

ports = getNames("128.153.145.20")

for port in ports:
    ifname = port[1]
    data = getJuniperData("128.153.145.20", port[0])
    sp1 = ifname.split("-")
    typ = "null"
    if "xe" in sp1[0]:
        typ = "fiber"
    elif "ge" in sp1[0]:
        typ = "ethernet"
    else:
        typ = "unknown"
    sp2 = sp1[1].split("/")
    if not ".0" in sp2[2]:
        portnum = sp2[2].split(".")[0]
        print("{} ({}): {}".format(portnum, typ, data))
