from operator import mod
from algorithm.RiverILVQ.prototypes import XuILVQ
from pickle import dumps, loads
from river import datasets
from web3 import Web3
import codecs, os, json, socket, river, random
from codification import decode

s = socket.socket()
s.bind( ('127.0.0.1', 8100) )
s.listen(10)

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

w3.eth.default_account = w3.eth.accounts[1]
contract_addr= w3.toChecksumAddress("0x39Bf11e2D76a63D63534234b54295f5C551e7073")
with open(os.getcwd() + '/solidity/artifacts/PrototypeBuffer.json', 'r') as f:
    prototypeJson = json.load(f)
abi = prototypeJson['abi']
PrototypeBuffer = w3.eth.contract(address = contract_addr, abi = abi)


model= XuILVQ()
test_files = datasets.Phishing()
train_files = []
train_oracle_files = []

while True:
    con,addr = s.accept()
    print("Conexion Establecida")
    data = []
    while True:
        res = con.recv(4096)
        if not res: break
        data.append(res)
    sensor_data = decode(data)
    train_files = train_files + sensor_data
    con.close()

    updated = False
    while(updated == False):
        accuracy,prototype,oracleData = PrototypeBuffer.functions._seeAll().call()
        if prototype != "":
            model.buffer._prototypes  = loads(codecs.decode(prototype.encode(),"base64"))
            model.buffer.n_features = 9
            model.buffer.classes = {False, True}
        if oracleData != "":
            train_oracle_files = loads(codecs.decode(oracleData.encode(),"base64"))

        for text, label in train_files + train_oracle_files:
            try:
                model.learn_one(text,label)
            except:
                pass


        metric = river.metrics.Accuracy()

        for x, y in test_files:
            y_pred = model.predict_one(x)
            if type(y_pred) != bool:
                if y_pred[0] == 1:
                    y_pred = False
                else: y_pred = True
            metric.update(y, y_pred)


        if accuracy == "":
            if PrototypeBuffer.functions._checkAccuracy(accuracy).call():
                prototype = codecs.encode(dumps(model.buffer._prototypes),"base64").decode()
                try:
                    PrototypeBuffer.functions._addPrototype(prototype,str(metric.get())).transact()
                    updated = True
                    train_files = []
                    train_oracle_files = []
                except:
                    updated = True
        elif metric.get() > float(accuracy):
            if PrototypeBuffer.functions._checkAccuracy(accuracy).call():
                prototype = codecs.encode(dumps(model.buffer._prototypes),"base64").decode()
                try:
                    PrototypeBuffer.functions._addPrototype(prototype,str(metric.get())).transact()
                    train_files = []
                    train_oracle_files = []
                    updated = True
                except:
                    updated = True
        else:
            updated = True

