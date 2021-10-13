

status = True
type_of_transaction=0
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

print("You choose option #{}".format(type_of_transaction))
