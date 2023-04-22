import heapq
class pBFT:
	def __init__(self,identity:str,nodeList:list,networkObject,maxDelay:int):
		print("Initializing Node...",identity)
		self.identity = identity
		self.nodeList = nodeList
		self.networkingObject = networkObject
		self.round = 0
		self.viewChangeType1 = []
		self.currentMessage = {}
		self.votingPhase = {}
		self.preCommitPhase = {}
		self.f = len(self.nodeList)//3
		self.n = len(self.nodeList)
		self.cPhase = 'propose'
		self.delay = maxDelay
		self.maxDelay = maxDelay
		self.heap = []
		for node in nodeList:
			heapq.heappush(self.heap , [0,node])

	def isleader(self):
		Leader = False
		top_ele = heapq.heappop(self.heap)
		if top_ele[2] == self.id:
			Leader = True
		heapq.heappush(self.heap,top_ele)
		return Leader

	# def clientMessage(self,message):


	def resetClock(self):
		self.delay = self.maxDelay

	def boradCast(self,message:dict):
		# asyncLim = 100
		# while asyncLim > 0:
		# 	asyncLim -= 1
		print("Node ",self.identity,"broadcasting",message)
		for node in self.nodeList:
			self.networkingObject.sendMessage(node,message)

	def votingPhase(self,message):
		if self.cPhase != 'voting':
			return False
		if message['round'] != self.round or message['sender'] in self.votingPhase['recvIds']:
			return False
		else:
			self.votingPhase['recvIds'].append(message['sender'])
		if message['value'] not in self.votingPhase['rmsg'].keys():
			self.votingPhase['rmsg'][message['value']] = []
		self.votingPhase['rmsg'][message['value']].append(message['sender'])
		if len(self.votingPhase['rmsg'][message['value']]) >= n - f:
			self.cPhase = 'precommit'
			self.resetClock()
			self.votingPhase = {'recvIds':[],'rmsg':{}}
			return True 
		else:
			# duplicate message ignore this bitch 
			return False

	def proposalPhase(self,message):
		if self.cPhase != 'propose':
			return False
		else:
			self.message = message
			self.resetClock()
			self.cPhase = 'voting'
			return True

	def changeLeader(self,score:int):
		top_ele = heapq.heappop(self.heap)
		# its a min heap so , 
		top_ele[0] -= score
		heapq.heappush(self.heap , top_ele)
		print('changing leader for',self.identity)
		self.resetClock()
		self.preCommitPhase = {'recvIds':[],'rmsg':{}}
		self.votingPhase = {'recvIds':[],'rmsg':{}}
		self.message = {}
		self.cPhase = 'propose'

	def preCommitPhase(self,message):
		if self.cPhase != 'precommit':
			return False
		if message['round'] != self.round or message['sender'] in self.preCommitPhase['recvIds']:
			return False
		else:
			self.preCommitPhase['recvIds'].append(message['sender'])
		if message['value'] not in self.preCommitPhase['rmsg'].keys():
			self.preCommitPhase['rmsg'][message['value']] = []
		self.preCommitPhase['rmsg'][message['value']].append(message['sender'])

		if len(self.preCommitPhase['rmsg'][message['value']]) >= self.n - self.f:
			self.cPhase = 'precommit'
			self.resetClock()
			self.changeLeader(1)
			self.preCommitPhase = {'recvIds':[],'rmsg':{}}
			return True 
		elif len(self.preCommitPhase['rmsg'][message['value']]) >= self.f + 1 and self.message['value'] != message['value']:
			self.viewChange(json.dumps({'single':self.message,'multiple':self.preCommitPhase['rmsg'][message['value']]}))
		else:
			# duplicate message ignore this bitch 
			return False

	def viewChange(self,proof=None):
		if proof == None:
			self.boradCast({'type':"view-change",'round':self.round,"identity":self.identity,'proof':"None"})
		elif type(proof) == str:
			self.boradCast({'type':"view-change",'round':self.round,"identity":self.identity,'proof':proof})

	def viewChangeRecv(self,message):
		if message['proof'] == "None" and message['identity'] not in self.viewChangeType1:
			self.viewChangeType1.append(self.identity)		# can append signed message digest instead
			if len(self.viewChangeType1) >= self.f + 1:
				self.changeLeader(-1)
			# commit to view change if len(self.viewChangeType1)
		else:
			proof_valid = True
			# check if proof is correct 
			if proof_valid:
				self.changeLeader(-1)
			pass

	def addToFile(self,message:dict):
		cleg = {}
		with open('./'+self.identity+'_ledger.json','r') as f:
			cleg = json.load(f)
		
		with open('./'+self.identity+'_ledger.json','w') as f:
			json.dumps(cleg['ledger'].append(message))


	def start(self):
		print("Starting node...",self.identity)
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

			self.delay-=1

			if self.delay <= 0:
				self.viewChange()

			rmsg = self.networkingObject.recvMessage()
			rv = False

			if rmsg == None:
				continue

			elif rmsg['round'] != self.round:
				# ideally, save this message (if from future round) to be processed later, but for now ignore the message 
				pass

			elif rmsg['type'] == 'view-change':
				self.viewChangeRecv(rmsg)

			elif rmsg['type'] == 'propose' and self.proposalPhase(rmsg):
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
				self.addToFile(self.message)

