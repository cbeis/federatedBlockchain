#Skeleton code of the sensor nodes
from pickle import dumps
from random import random, randint
from river import datasets
import socket, time
from codification import encode


dataset = datasets.Phishing()
train_files = []

for text,label in dataset:
    train_files.append((text,label))

train_split = train_files[:len(train_files)//5]

count = 0
interval = random() #Select the time interval between communication.
while True:
    s = socket.socket()
    s.connect(('127.0.0.1', 8100))
    chunk_size = randint(10,20)
    if len(train_split)-1 <count+chunk_size:
        s.send(encode(train_split[count:len(train_split)-1]))
        s.close()
        break
    s.send(encode(train_split[count:(count+chunk_size)]))
    s.close()
    count = count +chunk_size
    time.sleep(interval)

