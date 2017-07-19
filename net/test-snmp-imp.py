PRINT = False

SEND_IP = "128.153.145.251"
SEND_PORT = 16

import os
import sys
import time
import socket

def send(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto("", (SEND_IP, SEND_PORT))

def createPacket(community, ip, query):
    pass

"""

TRANSMIT (to UDP/161)

30 49 02 01

00 version number

01

<char string for community name>

a0 3d

<3 byte request ID>

02 01

00 error status

02 01

00 error index

30 0e

2b 06 01 02 01 02 02 01 05 01 IP-MIB object iso.1.3.6.1.2.1.2.2.1.5.1

Repeat from 30 0e



RECIEVE (from 161)

30 56 02 01

00 version number

04 05

<char string for community name>

a2 4a

02 03

<3 byte request ID (same as query ID)

02 01

00 error status

02 01

00 error index

30 3d

30 12

06 0a

2b 06 01 02 01 02 02 01 05 01 IP-MIB

42 04

<unsigned 32 bit integer>

Repeat from 30 12

"""
