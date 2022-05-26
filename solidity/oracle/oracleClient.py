#Establishment of the oracle and periodic requests for its update

from asyncore import poll
from web3 import Web3
import json
import os
import time

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

w3.eth.default_account = w3.eth.accounts[0]
with open(os.getcwd()+ '/solidity/artifacts/PrototypeBuffer.json', 'r') as f:
    oracleJson = json.load(f)
abi = oracleJson['abi']
contract_addr= w3.toChecksumAddress("0x7C2b0bDA0aBCC6f2bf1df5001876FdEA954fa5cD")
PrototypeBuffer = w3.eth.contract(address = contract_addr, abi = abi)

newOracleAddressEvent = PrototypeBuffer.events.newOracleAddressEvent()
dataUpdatedEvent = PrototypeBuffer.events.DataUpdatedEvent()

def handle_oracle_event(event):
    receipt= w3.eth.wait_for_transaction_receipt(event['transactionHash'])
    result = newOracleAddressEvent.processReceipt(receipt)
    print("Oracle Address has been assigned.")

def log_oracle_loop(event_filter,poll_interval):
    PrototypeBuffer.functions.setOracleInstanceAddress("0x9d7e1c43F0845BBB83c4Ab03bA7b3E7a28EE7A9b").transact()
    oracle_assigned = False;
    while not oracle_assigned:
        for event in event_filter.get_new_entries():
            handle_oracle_event(event)
            oracle_assigned = True;

def handle_data_event(event):
    receipt= w3.eth.wait_for_transaction_receipt(event['transactionHash'])
    result = dataUpdatedEvent.processReceipt(receipt)
    print("Data has been updated")

def log_data_loop(event_filter,poll_interval):
    while True:
        PrototypeBuffer.functions.updateData().call()
        received_data = false
        while not received_data:
            for event in event_filter.get_new_entries():
                handle_data_event(event)
                received_data = True;
                time.sleep(poll_interval)
        time.sleep(3600)

block_filter = w3.eth.filter({'fromBlock':'latest', 'address':contract_addr})
log_oracle_loop(block_filter, 2)

log_data_loop(block_filter, 2)