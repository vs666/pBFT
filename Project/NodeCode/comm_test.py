from local_networking import Network
from network_simulator import NetworkSimulator
import sys
import os 
import json 
import random
import time 


def makeFile(fileName,content):
	with open(fileName,'w') as fp:
		json.dump(content,fp)

def add_elt(fileName,content):
	d = {}
	with open(fileName,'r') as fp:
		d = json.load(fp)
	d["messages"].append(content)
	with open(fileName,'w') as fp:
		json.dump(d,fp)

for fn in ['f1','f2','f3','f4','f5']:
	makeFile(fn+'_pre_messages.json',{"messages":[]})
	makeFile(fn+'_messages.json',{"messages":[]})
	makeFile(fn+'_lock.json',{"status":0})


time.sleep(2)
# for fn in ['f1','f2','f3','f4','f5']:
# 	add_elt(fn+'.json',{"hello":1,"world":-1})


networkList = []
for fn in ['f1','f2','f3','f4','f5']:
	networkList.append(Network(fn,'./'))

for i in range(10):
	a = random.randint(1,5)
	b = random.randint(1,5) 
	while a == b:
		b = random.randint(1,5)
	networkList[a-1].sendMessage('f'+str(b),{"msg":"Hello from f"+str(a)})
	for z in range(5):
		if random.randint(0,1) == 1:
			print("message recv for f",z+1,networkList[z].recvMessage())
