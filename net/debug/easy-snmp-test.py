from easysnmp import snmp_get
from time import sleep
import threading

ifSpeed32 = "1.3.6.1.2.1.2.2.1.5"
inOctets32 = "1.3.6.1.2.1.2.2.1.10"
outOctets32 = "1.3.6.1.2.1.2.2.1.16"
ifSpeed64 = "1.3.6.1.2.1.31.1.1.1.15"
inOctets64 = "1.3.6.1.2.1.31.1.1.1.6"
outOctets64 = "1.3.6.1.2.1.31.1.1.1.10"

#switches = {}

def getData(ip, port): # returns speed, in, out
    data = {}
    data["speed"] = int(snmp_get(ifSpeed64 + "." + port, hostname=ip, community='cacti', version=2).value)
    data["in"] = int(snmp_get(inOctets64 + "." + port, hostname=ip, community='cacti', version=2).value)
    data["out"] = int(snmp_get(outOctets64 + "." + port, hostname=ip, community='cacti', version=2).value)
    return data

def snmpthread(sw, pt):
    while 1:
        time = 1 # seconds
        b = getData("128.153.145.25" + str(sw), str(pt))
        sleep(time)
        e = getData("128.153.145.25" + str(sw), str(pt))
        speed = b["speed"]
        if speed != 0:
            in2 = (e["in"] - b["in"]) / time * 8 / 1024 / 1024 # Mb/s
            out2 = (e["out"] - b["out"]) / time * 8 / 1024 / 1024 # Mb/s
        else:
            in2 = 0
            out2 = 0

        curdata = {}
        curdata["speed"] = speed
        curdata["in"] = in2
        curdata["out"] = out2
        #switches[str(sw) + ":" + str(pt)] = curdata

for sw in range(1, 4):
    for pt in range(1,25):
        collect = threading.Thread(target=snmpthread, args=(sw, pt))
        collect.start()

# For deubgging purposes see below, and uncomment any line with the switches variable.

# sleep(1)
# while 1:
#     empty = 0
#     sleep(1)
#     for i in range(1,50):
#         print()
#     for sw in range(1, 4):
#         for pt in range(1,25):
#             data = switches[str(sw) + ":" + str(pt)]
#             if data["speed"] != 0:
#                 print ("SWM{} Port {}:\tSpeed: {}Mb/s\tUpload: {} Mb/s\tDownload: {} Mb/s".format(sw, pt, data["speed"], round(data["in"],2), round(data["out"],2)))
#             else:
#                 empty += 1
#     print("There are {} ports disconnected.".format(empty))

# sleep(1)
# while 1:
#     sleep(1)
#     print ("------------")
#     sw = 3
#     pt = 1
#     data = switches[str(sw) + ":" + str(pt)]
#     if data["speed"] != 0:
#         print ("SWM{} Port {}:\tSpeed: {}Mb/s\tUpload: {} Mb/s\tDownload: {} Mb/s".format(sw, pt, data["speed"], round(data["in"],2), round(data["out"],2)))
