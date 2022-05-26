# federatedBlockchain

El código subido es la generalización más abstracta posible del proyecto completo. Las partes particularizadas como la actualización que se llevaría a cabo dependiendo del algoritmo que utilicemos se profundizarán en la parte de pruebas de la documentación.

## geth

### data.sh

    Script de lanzamiento de un nodo individual de nuestra red blockchain.

## socket

### client.py

    Socket de envío de los datos del nodo sensor al nodo blockchain.

### server.py

    Socket de recepción de los datos, así como se procesan, actualizan y se suben a nuestra red de bloques.

## solidity

### Prototype.sol

    Código del contrato donde se produce el almacenamiento y actualización de los prototipos, así como las llamadas al oráculo.

## Oracle

### oracleClient.py

    Comunica al smart Contract la dirección en la que se encuentra alojado el oráculo, así como realiza peticiones periódicas al mismo para su actualización.

### oracleServer.py

    Responde las peticiones desde el Oracle smart contract con los datos del sensor pertenecientes al nodo aislado.

### DataOracle.py

    Smart Contract en el que se encuentran los métodos con las principales funcionalidades del oráculo.
