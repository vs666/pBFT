import time 
import numpy as np 
import requests
import sys
import random
import json 

class NetworkSimulator:
	def __init__(self,nodeList,nfp='./',distribution='exponential',param=[1,0.4]):
		"""
		args:
			nodeList: list of node identities
			nfp: networking file path
			distribution: distribution of time delay
			param: parameters of distribution
		
		returns:
			None

		"""
		self.distribution = distribution
		self.nodeList = nodeList
		self.param = param
		self.networkingFilePath = nfp
		self.tdelay = []
		for nl in self.nodeList:
			self.tdelay.append(0)

	def mutateFile(self,nodeId):
		lock = True
		lockFilePath = self.networkingFilePath + nodeId + '_lock.json'
		while lock:
			try:
				if json.load(open(lockFilePath,'r'))["status"] == 0:
					lock = False
					break
			except:
				continue
		with open(lockFilePath,'w') as f:
			json.dump({"status":1}, f)
		
		rmessageFilePath = self.networkingFilePath + nodeId + '_pre_messages.json'
		msgList =  json.load(open(rmessageFilePath,'r'))
		if len(msgList["messages"]) == 0:
			with open(lockFilePath,'w') as f:
				json.dump({"status":0}, f)
			return None
		index = random.randint(0,len(msgList["messages"])-1)
		rmsg = msgList["messages"][index]
		nmsg = []
		for ind in range(len(msgList["messages"])):
			if ind != index:
				nmsg.append(msgList["messages"][ind])
		msgList["messages"] = nmsg
		with open(rmessageFilePath,'w') as f:
			json.dump(msgList,f)
		# print("Transferring message for",nodeId,rmsg)
		messageFilePath = self.networkingFilePath + nodeId + '_messages.json'
		msgList = json.load(open(messageFilePath,'r'))
		msgList["messages"].append(rmsg)
		with open(messageFilePath,'w') as f:
			json.dump(msgList,f)
		with open(lockFilePath,'w') as f:
			json.dump({"status":0}, f)
	
	def simulate(self):
		while True:
			index = 0
			for i in self.nodeList:
				if self.tdelay <= 0:
					self.mutateFile(i)
					self.tdelay[index] = np.random.exponential(self.param[0])
				else:
					self.tdelay -= 0.0001
