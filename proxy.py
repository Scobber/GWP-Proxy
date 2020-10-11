import socket
import sys
import time
import ttn
import argparse


def writelog(gatewayeui, direction, ipaddress, message, packetlen, extended):
    print("{0} {1} {2: <15} {3: <9} {4} :: {5} ::".format(gatewayeui, direction, ipaddress, message, packetlen, extended))


def main(argv):
    parser = argparse.ArgumentParser(description='GWP Proxy, github/scobber AGPL-3.0.')
    parser.add_argument("--raddress", default="router.au.thethings.network", type=str, help="LoRaWAN Router address")
    parser.add_argument("--rport", default=1700, type=int, help="LoRaWAN Router Port")
    parser.add_argument("--listen", default="0.0.0.0", type=str, help="Listen address")
    parser.add_argument("--port", default=1700, type=int, help="Listen port")
    args = parser.parse_args()
    ttnrouter = args.raddress
    ttnport = args.rport
    UDP_IP = args.listen
    UDP_PORT = args.port
    gwsock = socket.socket(socket.AF_INET,  # Internet
                           socket.SOCK_DGRAM)  # UDP
    ttnsock = socket.socket(socket.AF_INET,  # Internet
                            socket.SOCK_DGRAM)  # UDP
    ttnsock.settimeout(10)
    gwsock.bind((UDP_IP, UDP_PORT))
    while True:
        try:
            gwdata, gwaddr = gwsock.recvfrom(100000)  # buffer size is 1024 bytes
            #gwdata = gwdata.replace(b"GMT", b"UTC") # demonstration of removing
            #gwdata = gwdata.replace(b",\"temp\":30.0", b"") # Used to prove the temp param

            gwdatalen=len(gwdata)
            version, identifier, ptype,  gatewayeui, gwjson = ttn.decodeGateway(gwdata)
            writelog(gatewayeui, "><", gwaddr[0], ptype, gwdatalen, gwjson)

            ttnsock.sendto(gwdata, (ttnrouter, ttnport))

            ttndata, ttnaddr = ttnsock.recvfrom(100000)
            ttndatalen=len(ttndata)
            ttnversion, ttnidentifier, ttntype,  gatewayeui, ttnjson = ttn.decodeTTN(ttndata)
            writelog(gatewayeui, "<>", ttnaddr[0], ttntype, ttndatalen, ttnjson)
            gwsock.sendto(ttndata, gwaddr)
        except socket.timeout as s:
            print("Socket Timeout", s)


if __name__ == "__main__":
    main(sys.argv[1:])
