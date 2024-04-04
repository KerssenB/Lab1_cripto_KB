import os
import sys
import time
from scapy.all import IP, ICMP, send

message = sys.argv[1]
id_c = 1
seq_c = 1

def paquete_ICMP(letra, id_c, seq_c):
    time_utc= int(time.time())
    
    # Pasar tiempo de UTC a HEX y Bytes para que Wireshark reconozca el Timestamp
    time_hex = hex(time_utc)[2:]
    timestamp = bytes.fromhex(time_hex.rjust(16, '0'))
    timestamp = timestamp[::-1]
    
    data = timestamp
    
    # 3 bytes coherentes
    data += bytes(letra, 'utf-8')
    data += b'\x01\x02'
    
    # 5 bytes 0x00
    data += b'\x00\x00\x00\x00\x00'
    
    # bytes desde 0x10 a 0x37
    data += bytes(range(0x10, 0x38))
    
    paquete_final = IP(dst='127.0.0.1') / ICMP(id=id_c, seq=seq_c) / data
    
    return paquete_final

for i in message:
    paquete = paquete_ICMP(i, id_c, seq_c)
    send(paquete)
    
    id_c += 1
    seq_c += 1
    
    time.sleep(1)
