import socket
import time
import ttn
UDP_IP = "0.0.0.0"
UDP_PORT = 1700
ttnrouter = "ttn.opennetworkinfrastructure.org"

gwsock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
ttnsock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
ttnsock.settimeout(10)                     
gwsock.bind((UDP_IP, UDP_PORT))
ttnport = 1700
def writeLog(gatewayeui, direction, ipaddress, message, packetlen, extended):
    print("{0} {1} {2: <15} {3: <9} {4} :: {5} ::".format(gatewayeui, direction, ipaddress, message, packetlen, extended))
while True:
    try:
        gwdata, gwaddr = gwsock.recvfrom(100000) # buffer size is 1024 bytes
        #gwdata = gwdata.replace(b"GMT", b"UTC")
        gwdata = gwdata.replace(b",\"temp\":30.0", b"")

        gwdatalen=len(gwdata)
        version, identifier, ptype,  gatewayeui, gwjson = ttn.decodeGateway(gwdata)
        writeLog(gatewayeui, "><", gwaddr[0], ptype, gwdatalen, gwjson)

        ttnsock.sendto(gwdata, (ttnrouter, ttnport))
        
        ttndata, ttnaddr = ttnsock.recvfrom(100000)
        ttndatalen=len(ttndata)
        ttnversion, ttnidentifier, ttntype,  gatewayeui, ttnjson = ttn.decodeTTN(ttndata)
        writeLog(gatewayeui, "<>", ttnaddr[0], ttntype, ttndatalen, ttnjson)
        gwsock.sendto(ttndata, gwaddr)
    except socket.timeout as s:
        print("Socket Timeout", s)
