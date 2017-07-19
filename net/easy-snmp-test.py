from easysnmp import snmp_get

ifSpeed32 = "1.3.6.1.2.1.2.2.1.5"
inOctets32 = "1.3.6.1.2.1.2.2.1.10"
outOctets32 = "1.3.6.1.2.1.2.2.1.16"
ifSpeed64 = "1.3.6.1.2.1.31.1.1.1.15"
inOctets64 = "1.3.6.1.2.1.31.1.1.1.6"
outOctets64 = "1.3.6.1.2.1.31.1.1.1.10"

def getData(ip, port): # returns speed, in, out
    data = {}
    data["speed"] = snmp_get(ifSpeed64 + "." + port, hostname=ip, community='cacti', version=2).value
    data["in"] = snmp_get(inOctets64 + "." + port, hostname=ip, community='cacti', version=2).value
    data["out"] = snmp_get(outOctets64 + "." + port, hostname=ip, community='cacti', version=2).value
    return data

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

# Grab a single piece of information using an SNMP GET
#print(snmp_get('1.3.6.1.2.1.2.2.1.5.1', hostname='128.153.145.251', community='cacti', version=2))
#print(snmp_get('1.3.6.1.2.1.2.2.1.10.1', hostname='128.153.145.251', community='cacti', version=2))
#print(snmp_get('1.3.6.1.2.1.2.2.1.16.1', hostname='128.153.145.251', community='cacti', version=2))
print(snmp_get('1.3.6.1.2.1.31.1.1.1.15.10', hostname='128.153.145.252', community='cacti', version=2))
print(snmp_get('1.3.6.1.2.1.31.1.1.1.15.10', hostname='128.153.145.252', community='cacti', version=2).value)
print(snmp_get('1.3.6.1.2.1.31.1.1.1.10.10', hostname='128.153.145.252', community='cacti', version=2))
print(snmp_get('1.3.6.1.2.1.31.1.1.1.6.10', hostname='128.153.145.252', community='cacti', version=2))
