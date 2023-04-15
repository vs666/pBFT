class pBFT:
	def __init__(self,identity:str,nodeList:list,networkObject):
		self.identity = identity
		self.nodeList = nodeList
		self.networkingObject = networkObject
		self.round = 0
		self.currentMessage = {}
		self.votingPhase = {}
		self.preCommitPhase = {}
		self.f = len(self.nodeList)//3
		self.n = len(self.nodeList)
		self.cPhase = 'propose'
	def boradCast(self,message:dict):
		for node in nodeList:
			self.networkingObject.sendMessage(node,message)

	def votingPhase(self,message):
		if self.cPhase != 'voting':
			return False
		if message['sender'] in self.votingPhase['recvIds']:
			return False
		else:
			self.votingPhase['recvIds'].append(message['sender'])
		if message['digest'] not in self.votingPhase.keys():
			# new value 
			pass
		elif message['identity'] not in votingPhase[message['digest']].keys():
			# new entry 
			pass 
			if len(votingPhase[message['digest']].keys()) >= n - f:
				self.cPhase = 'precommit'
				votingPhase = {}
				return True 
		else:
			# duplicate message ignore this bitch 
			return False

	def proposalPhase(self,message):
		if self.cPhase != 'propose':
			return False
		else:
			self.message = message
			self.cPhase = 'voting'
			return True

	def preCommitPhase(self,message):
		if self.cPhase != 'precommit':
			return False
		if message['sender'] in self.preCommitPhase['recvIds']:
			return False
		else:
			self.preCommitPhase['recvIds'].append(message['sender'])
		if message['digest'] not in self.preCommitPhase.keys():
			# new value 
			pass
		elif message['identity'] not in preCommitPhase[message['digest']].keys():
			# new entry 
			pass 
			if len(preCommitPhase[message['digest']].keys()) >= n - f:
				preCommitPhase = {}
				self.cPhase = 'propose'
				self.round += 1
				return True 
		else:
			# duplicate message ignore this bitch 
			return False

	def start(self):
		while True:
			'''
				Step 1: Recv msg 
					Step 1.1: Process message 
					Step 1.2: Check if there is need to broadcast message (end of some phase)
						Step 1.2.1: Make the modified message 
						Step 1.2.2: Sign the message using your signature (optional to implement)
				Step 2: Check if agreement is reached then store the results locally
			'''
			# can check who is leader here...for view change and shit 

			rmsg = self.networkingObject.recvMessage()
			rv = False
			if rmsg == None:
				continue
			if rmsg['type'] == 'propose' and self.proposalPhase(rmsg):
				rmsg['type'] = 'vote'
				rmsg['sender'] = self.identity
				# signature shit here 
				self.boradCast(rmsg)
			elif rmsg['type'] == 'vote' and self.votingPhase(rmsg):
				rmsg['type'] = 'precommit'
				rmsg['sender'] = self.identity
				# signature shit here 
				self.boradCast(rmsg)
			elif rmsg['type'] == 'precommit' and self.preCommitPhase(rmsg):
				# add to file or something 

