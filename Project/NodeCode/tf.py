import json 

fp = open('t.json','r+')
d = json.load(fp)
d["akshett"] = "jindal"
fp.seek(0)
fp.truncate(0)
json.dump(d,fp)
