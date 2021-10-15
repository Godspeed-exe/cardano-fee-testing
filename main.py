from pathlib import Path
import json


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
            main_inputs.append(exploded)
        
        txinnerbody = {0: main_inputs,1: recipients}

        T = 0
        C = 0
        M = 0
    case _:
        T = 0
        C = 0
        M = 0
        
print(txinnerbody)
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