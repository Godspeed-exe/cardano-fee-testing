

from typing import Protocol

from pathlib import Path
import json


status = True
type_of_transaction=0
protocol_parameters_path="protocol_parameters.json"

if Path(protocol_parameters_path).is_file():
    with open(protocol_parameters_path) as jsonFile:
        protocol_parameters = json.load(jsonFile)
        jsonFile.close()
else:
    print("ERROR: Your protocol parameter file was not found!")
    exit()


print('Welcome to the Cardano fee calculation simulation.')
print('Please select the type of transaction you want to simulate:')
print('1. Normal Cardano transaction - only ADA')
print('2. Cardano transaction with Native Asset - ADA plus NFT')
print('3. Execute a smart contract')

while status:
    type_of_transaction = input('Which option do you want to simulate?')
    if type_of_transaction.strip().isdigit():
        type_of_transaction = int(type_of_transaction)
        if type_of_transaction in range(1,3):
            status = False



a = protocol_parameters['txFeePerByte']
b = protocol_parameters['executionUnitPrices']['priceSteps']
c = protocol_parameters['executionUnitPrices']['priceMemory']
d = protocol_parameters['txFeeFixed']
T = 0
C = 0
M = 0




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