

class Consensus:
	def __init__(self,pubKey, privKey,nbrFile:str,params):
		'''
		args:
			pubKey: public key of the node

			privKey: private key of the node

			nbrFile: file containing the list of nodes

			params: parameters of the consensus algorithm
		
		returns:
			None

		'''
		self.pkey = pubKey 
		self.skey = privKey
		self.cround = 0
		self.vote = {}
		self.commit = {}
		self.nodes = [] # set of known nodes
		self.state = 'None'
		self.params = params
		self.sniffNodes(nbrFile)

	def sniffNodes(self,fileName):
		pass 

	def recvVote(self,message):
		'''
			1. Verify Identity and Signature 
			2. Check for duplicacies (first message is accepted)
			3. Add to the list of messages 
			4. Return the state (waiting / completed)
		'''
		# Verify the identity and signature 
		self.verifyMessage(self,message) 		# to make this function 

		# Check for duplicates (done by itself)
		# Add to the list of messages 
		if message['value'] not in self.commit.keys():
			self.commit[message['value']] = []
		if message['signature'] not in self.commit[message['value']]:
			self.commit[message['value']].append(message['signature']) # signature is the tuple (sign, msg, pkey)

		if max([len(self.commit[key]) for key in self.commit.keys()]) > 2*self.params['n']//3: 
			return 'Completed'
		return 'Waiting'

	def sendVotes(self,pre_prepare):
		# code to send votes here 
		pass

	def recvPrepare(self,msg):
		# do something here.. 





