#Establishment of the oracle and periodic requests for its update.


from asyncore import poll
from web3 import Web3
import json, os, time

def log_data_loop(event_filter,poll_interval):
    while True:
        print("UpdateData request sent.")
        PrototypeBuffer.functions.updateData().transact()
        time.sleep(300)

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
w3.eth.default_account = w3.eth.accounts[0]

rpath = '/solidity/artifacts/PrototypeBuffer.json'
path = os.getcwd()+rpath
with open(path, 'r') as f:
    oracleJson = json.load(f)
abi = oracleJson['abi']

contract_addr= w3.toChecksumAddress("0x586f08EE4C0472c25A9cEf404823024A0E87cFfd")
PrototypeBuffer = w3.eth.contract(address = contract_addr, abi = abi)

block_filter = w3.eth.filter({'fromBlock':'latest', 'address':contract_addr})
log_data_loop(block_filter, 2)