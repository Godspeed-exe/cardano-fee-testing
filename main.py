from pathlib import Path
import json
import bech32
import sys


def convert_to_hex(address):
    recipient = address.split("+")
    dec_recipient = bech32.bech32_decode(recipient[0])
    index_recipient = recipient[1]
    recipient_hexlist = bech32.convertbits(dec_recipient[1], 5, 16)
    hex_recipient = ''.join([f'{c:04x}' for c in recipient_hexlist])[0:-2].upper()

    return [hex_recipient, int(index_recipient)]

status = True
type_of_transaction=0
protocol_parameters_path="protocol_parameters.json"

options = {
    1: 'Cardano transaction - only ADA',
    2: 'Cardano transaction with Native Asset - ADA plus NFT',
    3: 'Cardano transaction with metadata',
    4: 'Execute a smart contract',
}

if Path(protocol_parameters_path).is_file():
    with open(protocol_parameters_path) as jsonFile:
        protocol_parameters = json.load(jsonFile)
        jsonFile.close()
else:
    print("ERROR: Your protocol parameter file was not found!")
    exit()


print('Welcome to the Cardano fee calculation simulation.')
print('Please select the type of transaction you want to simulate:')

for opt in options:
    print('{}. {}'.format(opt, options[opt]))

while status:
    type_of_transaction = input('Which option do you want to simulate?')
    if type_of_transaction.strip().isdigit():
        type_of_transaction = int(type_of_transaction)
        if type_of_transaction in range(1,len(options)+1):
            status = False

match type_of_transaction:
    case 1:
        txbody = []
        num_inputs = input("How many inputs will your transaction have?")
        inputs = []
        while num_inputs==0 or not num_inputs.isdigit():
            num_inputs = input("How many inputs will your transaction have?")
        num_inputs = int(num_inputs)

        for counter_inputs in range (1, num_inputs+1): 
            new_input = input('Insert hash #{} of your input, example: 3474b8031017af508e873244b8ac5bfd4e35cee06a5d1695bbd5fd52aebde0c5#1: '.format(counter_inputs))
            inputs.append(new_input) 
        
        main_inputs = []
        recipients = []

        for el in inputs:
            exploded = el.upper().split('#')
            exploded[1] = int(exploded[1])
            main_inputs.append(exploded)
        
        recipient = input("To which address do you want to send these funds? example: addr1qye5yk4hev8y4ts7kjg9vej80jvr3jcny90kvvsfutr4vy70cnldrp0e0l8zkk0cdar60k5m5gnev2tk22q89ffz0ucsjv3a34+0")
        change = input("To which address should the change be sent? example: addr1qygq56zcjm30nd7stemhxt0spgv8pv2gjzvxct86nksm7zr3thmphsj959ukugkm8rlh0phhkxh0h566ehagqy98nzhslwlep0+0")
        

        recipients.append(convert_to_hex(recipient))
        recipients.append(convert_to_hex(change))

        txbody = []
        txinnerbody = {0: main_inputs,1: recipients, 2: 0, 3: 0}
        txbody.append(txinnerbody)
        txbody.append([])
        txbody.append(None)

        size = sys.getsizeof(txbody)
        print("size: {}".format(size))
        T = size
        C = 0
        M = 0
    case _:
        T = 0
        C = 0
        M = 0
        
print(txbody)
a = protocol_parameters['txFeePerByte']
b = protocol_parameters['executionUnitPrices']['priceSteps']
c = protocol_parameters['executionUnitPrices']['priceMemory']
d = protocol_parameters['txFeeFixed']


#needed: T * C * M 
#formula: a * T + b * C + c * M + d
# T is the Tx size
# C is the CPU steps
# M is the Memory units
# (C and M would be zero in the case of a tx without a smart contract).
# Current settings are:
# a = 44, b = 7.21E-05, c = 0.0577, d = 155381
# a, b, c, d are protocol parameters that determine the transaction fee in terms of
# a - transaction size, per byte
# b - cpu steps, per step
# c - memory units, per byte allocated
# d - a fixed fee per transaction

print("You choose option #{}".format(type_of_transaction))

result = (a * T + b * C + c * M + d) / 1000000

print("Total fee: {:.6f} ADA".format(result))