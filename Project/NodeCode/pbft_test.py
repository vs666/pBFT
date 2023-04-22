from pbft_source import pBFT
from local_networking import Network
from network_simulator import NetworkSimulator
import sys
import os 
import json 
import random
import time 
from threading import Thread
from meta import NL,DELAY

def makeFile(fileName,content):
	with open(fileName,'w') as fp:
		json.dump(content,fp)

for fn in NL:
	makeFile(fn+'_pre_messages.json',{"messages":[]})
	makeFile(fn+'_messages.json',{"messages":[]})
	makeFile(fn+'_lock.json',{"status":0})
	makeFile(fn+'_ledger.json',{"ledger":[]})
	
# time for simulator to start 
time.sleep(2)
# for fn in NL:
# 	add_elt(fn+'.json',{"hello":1,"world":-1})

def startNode(node):
	node.start()


nodeList = []
for fn in NL:
	nodeList.append(pBFT(fn,NL,Network(fn,'./'),DELAY))

threads = []

for fn in nodeList:
	thread = Thread(target=startNode,args=(fn,))
	thread.start()
	threads.append(thread)

for thread in threads:
	thread.join()

