from flask import Flask 
import json 

app = Flask(__name__)

def writeJson(new_data, filename):
	with open(filename,'r+') as file:
		file_data = json.load(file)
		file_data.append(new_data)
		file.seek(0)
		json.dump(file_data,file,indent=4)

@app.route('/sendMessage',methods=['POST','GET'])
def addToFile():
	dest = request.args.get('to')
	source = request.args.get('from')
	message = request.args.get('message')
	writeJson({'source':source,'destination':dest,'message':message},'./files/messages.json')

@app.route('/spreadMessage',methods=['POST','GET'])
def sendMessage():
	dest = request.args.get('to')
	source = request.args.get('from')
	message = request.args.get('message')
	filename = request.args.get('filename')
	writeJson({'source':source,'destination':dest,'message':message},'./nodes/'+filename)
