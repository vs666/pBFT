from local_networking import Network
from meta import NL,DELAY
import time
import random

round = 0
while True:
	node = random.choice(NL)
	ob = Network(node,"./")
	num = random.randint(1,1000)
	print("sending message" , num ,node)
	ob.sendMessage(node,{"type":"client-request" , 'value':"consensus_start"+str(num) , 'round':round})
	# round+=1
	time.sleep(3)

