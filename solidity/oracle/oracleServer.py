#Oracle service, responsible of receiving requests and obtaining data from the sensor not connected to the blockchain, which only updates data of the sensor directly.

from asyncore import read
from web3 import Web3
import json
import os
import time

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
w3.eth.default_account = w3.eth.accounts[0]

with open(os.getcwd() + '/solidity/artifacts/DataOracle.json', 'r') as f:
    oracleJson = json.load(f)

abi = oracleJson['abi']
contract_addr= w3.toChecksumAddress("0x9d7e1c43F0845BBB83c4Ab03bA7b3E7a28EE7A9b")

DataOracle = w3.eth.contract(address = contract_addr, abi = abi)
getLatestDataEvent = DataOracle.events.GetLatestDataEvent()


def handle_event(event):
    receipt= w3.eth.wait_for_transaction_receipt(event['transactionHash'])
    result = getLatestDataEvent.processReceipt(receipt)
    caller_address = result[0]['args']['callerAddress']
    with open(os.getcwd() + '/sensorData.txt', 'r') as f:
        sensorData = f.read()
    os.remove("sensorData.txt")
    DataOracle.functions.setLatestData( sensorData, caller_address)

def log_loop(event_filter,poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
            time.sleep(poll_interval)

block_filter = w3.eth.filter({'fromBlock':'latest', 'address':contract_addr})
log_loop(block_filter, 2)

