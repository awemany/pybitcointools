#!/usr/bin/env python
import bitcoin
import sys

if __name__=="__main__":
    addr = sys.argv[1]
    h_addr = bitcoin.b58check_to_hex(addr)
    print "BTG:", bitcoin.hex_to_b58check(h_addr, 38)
    print "BCH/BTC:", bitcoin.hex_to_b58check(h_addr, 0)
    print "testnet:", bitcoin.hex_to_b58check(h_addr, 111)
    print "hex:", h_addr
