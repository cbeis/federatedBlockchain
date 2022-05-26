#Skeleton code of the socket who receives the data of the sensor.
import codecs
from pickle import dumps, loads
import socket
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("Ganache/Geth Address"))

w3.eth.default_account = w3.eth.accounts[0]
contract_addr= w3.toChecksumAddress("Contract Address")
abi = "Abi of the contract"
PrototypeBuffer = w3.eth.contract(address = contract_addr, abi = abi)
s = socket.socket()
s.bind( ('Addr', Port) )
s.listen(10)

while True:
        con,addr = s.accept()
        res = con.recv(1024)

        #Aquí se produciría la decodificación.

        data_sensor = res.decode()

        #Obtención de los prototipos anteriores de la blockchain de todos los nodos.
        old_prototypes = PrototypeBuffer.functions._seeAll().call()
        loads(codecs.decode(old_prototypes.encode(),"base64"))

        #En esta parte, dependiendo del algoritmo escogido, comprobaremos los prototipos entre sí, obtendremos una nueva versión con ellos y 
        #con los datos del sensor, y actualizaremos "nuestra" versión del prototipo con los prototipos serializados.
        serialized_updated_prototype = codecs.encode(dumps('updated_prototype'),"base64").decode()
        PrototypeBuffer.functions._addPrototype(serialized_updated_prototype).transact()

        con.close()


