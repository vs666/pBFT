import time 
import numpy as np 
import requests
import sys
import random
import json 
import os
from tsc import Locker

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

	def checkLock(self,id):
		lpath = self.networkingFilePath + id + '.lock'
		return os.path.exists('./glock.lock') and os.path.exists(lpath)

	def lockFile(self,id):
		# print(f"simulator is locking for {id}")
		with open('./glock.lock','w') as fp:
			pass
		lpath = self.networkingFilePath + id + '.lock'
		with open(lpath,'w') as fp:
			pass

	def releaseLock(self,id):
		# print(f"simulator is releasing for {id}")
		os.remove('./glock.lock')
		lpath = self.networkingFilePath + id + '.lock'
		os.remove(lpath)


	def mutateFile(self,nodeId):
		# lock = True
		# lockFilePath = self.networkingFilePath + nodeId + '_lock.json'
		# while lock:
		# 	try:
		# 		if json.load(open(lockFilePath,'r'))["status"] == 0:
		# 			lock = False
		# 			break
		# 	except:
		# 		continue
		# with open(lockFilePath,'w') as f:
		# 	json.dump({"status":1}, f)
		# while self.checkLock(nodeId):
		# 	pass
		# self.lockFile(nodeId)

		rmessageFilePath = self.networkingFilePath + nodeId + '_pre_messages.json'
		rmsgFp = open(rmessageFilePath,'r+')
		with Locker(rmsgFp,rmessageFilePath):
			while True:
				try:
					msgList =  json.load(rmsgFp)
					rmsgFp.seek(0)
					break
				except:
					pass

			if len(msgList["messages"]) == 0:
				# with open(lockFilePath,'w') as f:
				# 	json.dump({"status":0}, f)
				# self.releaseLock(nodeId)
				return None
			index = random.randint(0,len(msgList["messages"])-1)
			rmsg = msgList["messages"][index]
			nmsg = []
			for ind in range(len(msgList["messages"])):
				if ind != index:
					nmsg.append(msgList["messages"][ind])
			msgList["messages"] = nmsg
			json.dump(msgList,rmsgFp)

		# print("Transferring message for",nodeId,rmsg)
		messageFilePath = self.networkingFilePath + nodeId + '_messages.json'
		msgFp = open(messageFilePath,'r+')
		with Locker(msgFp,messageFilePath):
			while True:
				try:
					msgList = json.load(open(messageFilePath,'r'))
					break
				except:
					pass

			msgList["messages"].append(rmsg)
			json.dump(msgList,msgFp)


	def simulate(self):
		while True:
			index = 0
			for i in self.nodeList:
				if self.tdelay[index] <= 0:
					self.mutateFile(i)
					if self.distribution == 'exponential':
						self.tdelay[index] = np.random.exponential(self.param[0])
					elif self.distribution == 'sync':
						self.tdelay[index] = 0
				else:
					self.tdelay[index] -= 0.0001
