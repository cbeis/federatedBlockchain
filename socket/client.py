#Skeleton code of the sensor nodes

import socket
from asyncore import read
import time
import os

s = socket.socket()
s.connect((Address, Port)

while True:
    #Recogemos las muestras de un archivo, asumiendo que el sensor las deposita ahí.
    with open(os.getcwd() + 'sensorData.txt', 'r') as f:
        sensorData = f.read()

    #Aquí se realizaría la codificación de datos, pero tendrá su fichero propio.

    s.send(sensorData.encode())
    #Una vez realizada la conexión, enviaremos datos cada hora.
    #Esto es fácilmente modificable a número de muestras almacenadas o cualquier variable que prefiramos.
    time.sleep(3600)

s.close()
