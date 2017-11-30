#!/usr/bin/env python3
# A very simple transaction injector
# Use like this:
# ./injector.py <BTG-host> <BTG-port> <transaction-as-hex>
#
import socket
import hashlib
import sys
import struct
import time
import codecs
import random


network_magic = b"\xe1\x47\x6d\x44"  # gold
#network_magic = b"\xf9\xbe\xb4\xd9" # mainnet
#network_magic = b"\xfa\xbf\xb5\xda" # regtest

node_services = struct.pack("<Q", 1)

MSG_TX = struct.pack("<I", 1)

def hexstr(b):
    return codecs.encode(b, "hex")

def asm_msg(cmd, payload):
    frame = network_magic
    frame += cmd+b"\0"*(12-len(cmd))
    frame += struct.pack("<I", len(payload))
    checksum = hashlib.sha256(
        hashlib.sha256(payload).digest()).digest()[:4]
    frame += checksum
    frame += payload
    return frame

def send_msg(cmd, payload):
    frame = asm_msg(cmd, payload)
    print("<", len(frame), hexstr(frame))
    sock.send(frame)

def wait_msg(msg):
    data = b""
    sys.stdout.write(">")
    while True:
        b = sock.recv(1)
        if not len(b):
            sys.stderr.write("\nERROR NO MORE BYTES\n")
            return
        data += b
        sys.stdout.write("%02x" % ord(b))
        sys.stdout.flush()
        if msg in data:
            sys.stdout.write("\n%s found \n" % msg)
            sys.stdout.write("\n>> %s" % repr(data))
            return

def net_addr(host, port):
    # lacks time field (as used for version message)
    s = node_services
    s += ((b"\0"*10)+
          (b"\xff" * 2)+
          bytearray(int(i) for i in host.split(".")))
    s += struct.pack(">H", port)
    return s

if __name__=="__main__" :
    host, port, transaction = sys.argv[1:]
    transaction = codecs.decode(transaction, "hex")

    port = int(port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    ver_payload =(
        struct.pack("<I", 70015)+ # version
        node_services+ # services
        struct.pack("<Q", int(time.time()))+ # timestamp
        net_addr(host, port)+
        net_addr("192.168.1.1", 8338)+
        struct.pack("<Q", int(random.random()*1000000)) +
        b"\x07Bitcoin" + # user agent
        struct.pack("<I", 100000) + # last block
        b"\0" # relay flag
    )

    time.sleep(.25)
    send_msg(b"version",
             ver_payload)

    wait_msg(b"verack")
    send_msg(b"verack", b"")
    time.sleep(.25)

    send_msg(b"tx", transaction)
    print("Done. You can exit with Ctrl-C now.")
    wait_msg(b"forever")
