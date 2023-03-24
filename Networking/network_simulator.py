import time 
import numpy as np 
import requests
import sys

class NetworkSimulator:
	def __init__(self,messages_file,drop_probability,delay_params:dict,server_url:str,adv_manipulation=None):
		self.messages_file = messages_file
		self.message_queue = []
		self.probability_dropping = drop_probability
		self.delay_params = delay_params
		self.server_url = server_url
		self.adv_manipulation = adv_manipulation

	def readFile(self):
		dat = None
		with open(self.messages_file,'w') as file:
			dat = json.load(file)
		return dat

	def simulateDelay(self):
		'''
			can try different sampling techniques:
				- normal distribution ('gauss')
				- exponential distribution ('expo')
				- sampling from a vector with a given probability vector ('vecvec')
		'''
		if self.delay_params['mode'] == 'gauss':
			time.sleep(np.random.normal(self.delay_params['mean'],self.delay_params['sd']))
		elif self.delay_params['mode'] == 'expo':
			time.sleep(np.random.exponential(self.delay_params['lambda']))
		elif self.delay_params['mode'] == 'vecvec':
			# too lazy to google sampling command, will implement later.
			pass

	def runSimulator(self):
		while True:
			while len(self.message_queue) == 0:
				self.message_queue = self.readFile()
			if self.adv_manipulation != None:
				self.message_queue = self.adv_manipulation(self.message_queue) # assuming that if function is implemented, it has internally access to the identities files
			msg = self.message_queue[0] 
			# check if the below line is correct...
			requests.post(self.server_url,msg)


if __name__ == '__main__':
	# get all the args from command line ...
	# argument format 
	# [*.py, messages_filename, drop_probability, delay_params (dict), server url 
	# need to import as module if we wanna pass adversarial functions

	msg_fn = sys.argv[1]
	dp = float(sys.argv[2])
	delay_params = dict(sys.argv[3])
	server_url = sys.argv[4]
	ns = NetworkSimulator(msg_fn,dp, delay_params,server_url)  
	ns.runSimulator()
