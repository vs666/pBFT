import json 


class Network:
	def __init__(self,nodeIdentity,nfp=None):
		self.identity = nodeIdentity
		self.networkingFilePath = '../GlobalFS/'
		if nfp != None:
			self.networkingFilePath = nfp

	def sendMessage(self,destination_identity:str,m2:dict):
		lock = True
		lockFilePath = self.networkingFilePath + destination_identity + '_lock.json'
		while lock:
			if json.load(open(lockFilePath,'r'))["status"] == 0:
				lock = False
				break
		with open(lockFilePath,'w') as f:
			json.dump({"status":1}, f)
		messageFilePath = self.networkingFilePath + destination_identity + '_pre_messages.json'
		msgList = json.load(open(messageFilePath,'r'))
		msgList["messages"].append(m2)
		with open(messageFilePath,'w') as f:
			json.dump(msgList,f)
		with open(lockFilePath,'w') as f:
			json.dump({"status":0}, f)
	
	def recvMessage(self):
		lockFilePath = self.networkingFilePath + self.identity + '_lock.json'
		lock = True
		while lock:
			if json.load(open(lockFilePath,'r'))["status"] == 0:
				lock = False
				break
		with open(lockFilePath,'w') as f:
			json.dump({"status":1}, f)
			print("Opened 1 mutex for ",self.identity)
			
		messageFilePath = self.networkingFilePath + self.identity + '_messages.json'
		msgList =  json.load(open(messageFilePath,'r'))
		if len(msgList["messages"]) == 0:
			with open(lockFilePath,'w') as f:
				json.dump({"status":0}, f)
			return None
		rmsg = msgList["messages"][0]
		with open(messageFilePath,'w') as f:
			json.dump({"messages":msgList["messages"][1:]},f)
		with open(lockFilePath,'w') as f:
			json.dump({"status":0}, f)
			
		return rmsg 




		