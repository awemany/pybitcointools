#!/usr/bin/env python
# Script to manually create 1-input 1-output transactions
# for the Bitcoin Gold chain, to claim Bitcoin Gold outputs

import sys
import bitcoin


if __name__=="__main__":
    if len(sys.argv) == 1:
        print sys.argv[0], "privkey input_txhash input_number input_amount dest_address fee"
        exit(0)

    (privkey, input_txhash, input_number, input_amount,
     dest_address, fee) = sys.argv[1:]

    privkey = bitcoin.b58check_to_hex(privkey)
    input_number = int(input_number)
    input_amount = int(input_amount)
    fee = int(fee)

    print "Private key:", privkey
    print "Input address for private key:", bitcoin.privkey_to_address(privkey)
    print "Input transaction hash:", input_txhash
    print "Input transaction output number:", input_number
    print "Input amount (Satoshis): ", input_amount
    output_amount = input_amount-fee
    print "Output amount (Satoshis): ", output_amount
    print "Miner fee (Satoshis): ", fee
    print "Destination address: ", dest_address

    vin = [input_txhash, input_number, input_amount]

    tx = bitcoin.mktx(
                [
                    {
                        'output': '{}:{}'.format(vin[0], vin[1]),
                    }
                ],
                [
                    {
                        "value": output_amount,
                        "address": dest_address
                    }
                ],
             serialize=True)
    signed_tx = bitcoin.segwit_sign(
        tx, 0, privkey, vin[2], hashcode=bitcoin.SIGHASH_ALL | bitcoin.SIGHASH_FORKID, separator_index=None)


    print "Signed transaction:"
    print signed_tx
