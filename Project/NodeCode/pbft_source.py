import heapq
import json
class pBFT:
	def __init__(self,identity:str,nodeList:list,networkObject,maxDelay:int):
		print("Initializing Node...",identity)
		self.identity = identity
		self.nodeList = nodeList
		self.networkingObject = networkObject
		self.round = 0
		self.viewChangeType1 = []
		self.currentMessage = {}
		self.votingPhase = {'recvIds':[],'rmsg':{}}
		self.preCommitPhase = {'recvIds':[],'rmsg':{}}
		self.requestQueue = []
		self.message = {}
		self.f = len(self.nodeList)//3
		self.n = len(self.nodeList)
		self.cPhase = 'propose'
		self.delay = maxDelay
		self.maxDelay = maxDelay
		self.heap = []
		self.discountFactor = 1.0
		for node in nodeList:
			heapq.heappush(self.heap , [0,node])

	def isleader(self):
		Leader = False
		top_ele = heapq.heappop(self.heap)
		if top_ele[1] == self.identity:
			Leader = True
		heapq.heappush(self.heap,top_ele)
		return Leader

	# def clientMessage(self,message):


	def resetClock(self):
		self.delay = self.maxDelay

	def broadCast(self,message:dict):
		# asyncLim = 100
		# while asyncLim > 0:
		# 	asyncLim -= 1
		print("Node ",self.identity,"broadcasting",message)
		for node in self.nodeList:
			self.networkingObject.sendMessage(node,message)

	def voting_phase(self,message):
		if self.cPhase != 'voting':
			return False
		if message['round'] != self.round or message['sender'] in self.votingPhase['recvIds']:
			return False
		else:
			self.votingPhase['recvIds'].append(message['sender'])
		if message['value'] not in self.votingPhase['rmsg'].keys():
			self.votingPhase['rmsg'][message['value']] = []
		self.votingPhase['rmsg'][message['value']].append(message['sender'])
		if len(self.votingPhase['rmsg'][message['value']]) >= self.n - self.f:
			self.cPhase = 'precommit'
			self.resetClock()
			self.votingPhase = {'recvIds':[],'rmsg':{}}
			return True 
		else:
			# duplicate message ignore this bitch 
			return False

	def proposal_phase(self,message):
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
		top_ele[0] = self.discountFactor * top_ele[0] - score
		heapq.heappush(self.heap , top_ele)
		print('changing leader for',self.identity)
		self.resetClock()
		self.preCommitPhase = {'recvIds':[],'rmsg':{}}
		self.votingPhase = {'recvIds':[],'rmsg':{}}
		self.message = {}
		self.cPhase = 'propose'

	def precommit_phase(self,message):
		if self.cPhase != 'precommit':
			return False , ""
		if message['round'] != self.round or message['sender'] in self.preCommitPhase['recvIds']:
			return False , ""
		else:
			self.preCommitPhase['recvIds'].append(message['sender'])
		if message['value'] not in self.preCommitPhase['rmsg'].keys():
			self.preCommitPhase['rmsg'][message['value']] = []
		self.preCommitPhase['rmsg'][message['value']].append(message['sender'])

		if len(self.preCommitPhase['rmsg'][message['value']]) >= self.n - self.f:
			self.cPhase = 'precommit'
			msg_to_send = self.preCommitPhase['rmsg']
			print(msg_to_send,"consensus value ===============")
			self.resetClock()
			self.changeLeader(1)
			self.preCommitPhase = {'recvIds':[],'rmsg':{}}
			return True , msg_to_send
		elif len(self.preCommitPhase['rmsg'][message['value']]) >= self.f + 1 and self.message['value'] != message['value']:
			self.viewChange(json.dumps({'single':self.message,'multiple':self.preCommitPhase['rmsg'][message['value']]}))
			return False , ""
		else:
			# duplicate message ignore this bitch 
			return False , ""

	def clientRequest(self,rmsg):
		self.requestQueue.append(rmsg['value'])
		# self.cPhase = 'propose'

	def viewChange(self,proof=None):
		if proof == None:
			self.broadCast({'type':"view-change",'round':self.round,"identity":self.identity,'proof':"None"})
		elif type(proof) == str:
			self.broadCast({'type':"view-change",'round':self.round,"identity":self.identity,'proof':proof})

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
		print(message)
		cleg = {}
		with open('./'+self.identity+'_ledger.json','r') as f:
			cleg = json.load(f)
		
		with open('./'+self.identity+'_ledger.json','a') as f:
			json.dumps(cleg['ledger'].append(message))

	def proposalValue(self):
		if(len(self.requestQueue) !=0):
			self.message = {'type':'propose','value':self.requestQueue[0],'identity':self.identity,'sender':self.identity,'round':self.round}
			self.broadCast(self.message)
			self.requestQueue.pop(0)
			self.cPhase = 'voting'
			self.resetClock()

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

			# if self.delay <= 0:
			# 	self.viewChange()

			rmsg = self.networkingObject.recvMessage()
			rv = False
			# print(self.identity , rmsg)
			if rmsg == None:
				continue
			print(rmsg)
			
			if rmsg['round'] != self.round:
    			# ideally, save this message (if from future round) to be processed later, but for now ignore the message 
				continue

			if rmsg['type'] == 'client-request':
    				self.clientRequest(rmsg)

			if self.cPhase == 'propose' and self.isleader():
				print("in propose phase" , len(self.requestQueue))
				self.proposalValue()

			elif rmsg['round'] != self.round:
				# ideally, save this message (if from future round) to be processed later, but for now ignore the message 
				pass

			elif rmsg['type'] == 'view-change':
				self.viewChangeRecv(rmsg)

			elif rmsg['type'] == 'propose' and self.proposal_phase(rmsg):
				rmsg['type'] = 'vote'
				rmsg['sender'] = self.identity
				# signature shit here 
				self.broadCast(rmsg)

			elif rmsg['type'] == 'vote' and self.voting_phase(rmsg):
				rmsg['type'] = 'precommit'
				rmsg['sender'] = self.identity
				# signature shit here 
				self.broadCast(rmsg)

			# elif rmsg['type'] == 'precommit' and self.precommit_phase(rmsg):
				# add to file or something
				# print("in final consensus----------------------------")
				# print(self.message)
				# self.addToFile(self.message)

			elif rmsg['type'] == 'precommit' :
				flag , val  = self.precommit_phase(rmsg)
				print(flag)
				if flag:
					# add to file or something
					print("in final consensus----------------------------")
					print(val)
					self.addToFile(val)

