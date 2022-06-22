from web3 import Web3
from web3.logs import DISCARD
from river import datasets
from random import randint
import json,os,time

def handle_file():
    chunk_size = randint(1,20)
    if len(train_split)-1 < count:
        return ""
    elif len(train_split)-1 <count+chunk_size:
        send_data = train_split[count:len(train_split)-1]
    else:
        send_data = train_split[count:(count+chunk_size)]
    count = count +chunk_size
    return send_data

def handle_event(event):
    receipt= w3.eth.wait_for_transaction_receipt(event['transactionHash'])
    result = getLatestDataEvent.processReceipt(receipt, errors=DISCARD)
    try:
        caller_address = result[0]['args']['callerAddress']
        send_data = handle_file()
        if send_data != "":
            DataOracle.functions.setLatestData( send_data, caller_address).transact()
        else:
            pass
    except:
        pass

def log_loop(event_filter,poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
            time.sleep(poll_interval)

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
w3.eth.default_account = w3.eth.accounts[5]

with open(os.getcwd() + '/solidity/artifacts/DataOracle.json', 'r') as f:
    oracleJson = json.load(f)

abi = oracleJson['abi']
contract_addr= w3.toChecksumAddress("0xfd2904078c28b7e5c90A9655fbe3196f60f3C817")

dataset = datasets.Phishing()
train_files = []
count= 0

for text,label in dataset:
    train_files.append((text,label))

train_split = train_files[4*len(train_files)//5:]


DataOracle = w3.eth.contract(address = contract_addr, abi = abi)
getLatestDataEvent = DataOracle.events.GetLatestDataEvent()

block_filter = w3.eth.filter({'fromBlock':'latest', 'address':contract_addr})
log_loop(block_filter, 10)

