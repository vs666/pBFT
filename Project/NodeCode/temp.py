import heapq
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
		self.delay = 100
		self.heap = []
		for node in nodeList:
			self.heap.heappush(self.heap , (0,node))
	def boradCast(self,message:dict):
		for node in nodeList:
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
			self.cPhase = 'voting'
			return True

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

		if len(self.preCommitPhase['rmsg'][message['value']]) >= n - f:
			self.cPhase = 'precommit'
			top_ele = self.heappop(self.heap)
			# its a min heap so , 
			top_ele[0]-=1
			self.heap.heappush(self.heap , top_ele)
			self.preCommitPhase = {'recvIds':[],'rmsg':{}}
			return True 
		else:
			# duplicate message ignore this bitch 
			return False

	def start(self):
		self.delay = 100
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
			if(self.delay < 0):
				break
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
				a=2

			# else:
			#     top_ele = self.heappop(self.heap)
			#     # its a min heap so , 
			#     top_ele[0]+=1
			#     self.heap.heappush(self.heap , top_ele)

