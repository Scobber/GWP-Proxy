def decodeGateway(packet):
    #packet = packet.decode('utf-8')
    version = packet[:1]
    identifier = packet[1:3]
    packval = packet[3:4]
    json = {}
    if(packval.hex() == "00"):
        ptype= "PUSH    "
    elif(packval.hex() == "02"):
        ptype= "PULL    "
    elif(packval.hex() == "05"):
        ptype= "TX_ACK  "
    else:
        ptype = "UNCL {0}".format(packval.hex())
    gatewayeui = ''.join('{:02x}'.format(x) for x in packet[4:12])
    
    json=packet[12:].decode('utf-8')
    return version, identifier, ptype,  gatewayeui, json

def decodeTTN(packet):
    #packet = packet.decode('utf-8')
    version = packet[:1]
    identifier = packet[1:3]
    packval = packet[3:4].hex()
    gatewayeui = "thethingsnetwork"
    json = "{}"
    if(packval == "01"):
        ptype= "PUSH_ACK"
    elif(packval == "03"):
        ptype= "PULL_RESP"
    elif(packval == "04"):
        ptype= "PULL_ACK"
    else:
        ptype = "UNCLASS", packval
    #gatewayeui = ''.join('{:02x}'.format(x) for x in packet[4:12])
    
    #json=packet[12:].decode('utf-8')
    return version, identifier, ptype,  gatewayeui, json
