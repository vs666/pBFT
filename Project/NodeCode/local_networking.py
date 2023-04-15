import json 


class Network:
	def __init__(self,nodeIdentity):
		self.identity = nodeIdentity
		self.networkingFilePath = '../GlobalFS/'

	def sendMessage(self,destination_identity:str,message:dict):
		lock = True
		lockFilePath = self.networkingFilePath + destination_identity + '_lock.json'
		while lock:
			if json.load(open(lockFilePath,'r'))["status"] == 0:
				lock = False
				break
		with open(lockFilePath,'w') as f:
			json.dumps({"status":1}, f)
		messageFilePath = self.networkingFilePath + destination_identity + '_messages.json'
		msgList =  json.load(open(messageFilePath,'r'))
		msgList['messages'].append(message)
		with open(messageFilePath,'w') as f:
			json.dumps(msgList,f)
		with open(lockFilePath,'w') as f:
			json.dumps({"status":0}, f)
	
	def recvMessage(self):
		lockFilePath = self.networkingFilePath + self.identity + '_lock.json'
		while lock:
			if json.load(open(lockFilePath,'r'))["status"] == 0:
				lock = False
				break
		with open(lockFilePath,'w') as f:
			json.dumps({"status":1}, f)
		messageFilePath = self.networkingFilePath + self.identity + '_messages.json'
		msgList =  json.load(open(messageFilePath,'r'))
		rmsg = msgList['messages'][-1]
		with open(messageFilePath,'w') as f:
			json.dumps({'messages':msgList['messages'][-1]},f)
		with open(lockFilePath,'w') as f:
			json.dumps({"status":0}, f)
		return rmsg 




		