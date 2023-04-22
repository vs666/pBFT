import json 
import os
from tsc import Locker

class Network:
	def __init__(self,nodeIdentity,nfp=None):
		self.identity = nodeIdentity
		self.networkingFilePath = './'
		if nfp != None:
			self.networkingFilePath = nfp

	def checkLock(self):
		lpath = self.networkingFilePath + self.identity + '.lock'
		return os.path.exists('./glock.lock') and os.path.exists(lpath)

	def lockFile(self):
		# print(f"{self.identity} is locking for {self.identity}")
		with open('./glock.lock','w') as fp:
			pass
		lpath = self.networkingFilePath + self.identity + '.lock'
		while self.checkLock():
			pass

		with open(lpath,'w') as fp:
			pass

	def releaseLock(self):
		# print(f"{self.identity} is releasing for {self.identity}")
		os.remove('./glock.lock')
		lpath = self.networkingFilePath + self.identity + '.lock'
		os.remove(lpath)

	def sendMessage(self,destination_identity:str,m2:dict):
		# print("Hello World")
		# lock = True
		# lockFilePath = self.networkingFilePath + destination_identity + '_lock.json'
		
		# while lock:
		# 	try:
		# 		if json.load(open(lockFilePath,'r'))["status"] == 0:
		# 			lock = False
		# 			break
		# 	except Exception:
		# 		continue

		# while self.checkLock():
		# 	pass
		# self.lockFile()
		messageFilePath = self.networkingFilePath + destination_identity + '_pre_messages.json'
		msgFp = open(messageFilePath,'r+')
		with Locker(msgFp,messageFilePath):
			msgList = None
			while True:
				try:
					msgList = json.load(msgFp)
					break
				except Exception:
					pass
			# print(f"{msgList = }, {m2 = } {self.identity = }")
			msgList["messages"].append(m2)
			msgFp.seek(0)
			msgFp.truncate(0)
			json.dump(msgList,msgFp)
			# with open(lockFilePath,'w') as f:
			# 	json.dump({"status":0},f)
		# self.releaseLock()
	
	def recvMessage(self):
		lockFilePath = self.networkingFilePath + self.identity + '_lock.json'
		lock = True
		# while lock:
		# 	try:
		# 		if json.load(open(lockFilePath,'r'))["status"] == 0:
		# 			lock = False
		# 			break
		# 	except:
		# 		pass
		# with open(lockFilePath,'w') as f:
		# 	json.dump({"status":1}, f)
		
		# while self.checkLock():
		# 	pass
		# self.lockFile()

		messageFilePath = self.networkingFilePath + self.identity + '_pre_messages.json'
		msgFp = open(messageFilePath,'r+')
		with Locker(msgFp,messageFilePath):
			while True:
				try:
					msgList =  json.load(msgFp)
					break
				except:
					pass	
			if len(msgList["messages"]) == 0:
				# with open(lockFilePath,'w') as f:
				# 	json.dump({"status":0}, f)
				# self.releaseLock()
				return None
			msgFp.seek(0)
			msgFp.truncate(0)
			rmsg = msgList["messages"][0]
			json.dump({"messages":msgList["messages"][1:]},msgFp)
			# with open(lockFilePath,'w') as f:
			# 	json.dump({"status":0}, f)
			# self.releaseLock()
		return rmsg 

		