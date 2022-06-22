from asyncore import poll
from web3 import Web3
import json,os

def handle_oracle_event(event):
    receipt= w3.eth.wait_for_transaction_receipt(event['transactionHash'])
    result = newOracleAddressEvent.processReceipt(receipt)

def set_oracle_address(event_filter,poll_interval):
    PrototypeBuffer.functions.setOracleInstanceAddress("Contract Address").transact()
    oracle_assigned = False;
    while not oracle_assigned:
        for event in event_filter.get_new_entries():
            handle_oracle_event(event)
            oracle_assigned = True;


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

w3.eth.default_account = w3.eth.accounts[0]
rpath = '/solidity/artifacts/PrototypeBuffer.json'
path = os.getcwd()+rpath
with open(path, 'r') as f:
    oracleJson = json.load(f)
abi = oracleJson['abi']

contract_addr= w3.toChecksumAddress("0x9Ff01078Ccf83052a74598BE68E2926092251142")
PrototypeBuffer = w3.eth.contract(address = contract_addr, abi = abi)

newOracleAddressEvent = PrototypeBuffer.events.newOracleAddressEvent()

block_filter = w3.eth.filter({'fromBlock':'latest', 'address':contract_addr})
set_oracle_address(block_filter, 2)
