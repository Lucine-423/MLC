from pymongo import MongoClient
import json
import os
import pprint
client = MongoClient('localhost',27017)
db = client.MLC
atc = db.atc

wdir = os.getcwd();

wdir += "/READ"

for root, dirs, files in os.walk(wdir):    
	print("WORKING")
	for mfile in files:
		print("OPEN : ",root+"/"+mfile)
		rf = open(root+"/"+mfile);


		line = rf.readline().replace("\r","")
		stc = []
		while  line:
			ptr = 0
			ktmp = line.find(".", ptr)
			tmp = 0;
			while tmp < len(line) and tmp >= 0:
				tmp = line.find(" ", ptr)
				stc.append(line[ptr:tmp].lower())
				ptr = tmp+1;


			stmp = 0;

			wlink = []
			for word in enumerate(stc):
				strword = str(word)
				if strword.find(".") == -1 and strword.find("?") == -1 and strword.find("!") == -1:
					dotmp = filter(str.isalpha, strword)
					wlink.append(dotmp)
					stmp += 1;
				else :
					dotmp = filter(str.isalpha, strword)
					wlink.append(dotmp)
					stmp = 0;
					wcount = 0;
					for cword in wlink:
						fwd = "";
						back = "";
						if wcount == 0:
							fwd = "";
						else:
							fwd = wlink[wcount-1];
						if wcount < (len(wlink)-1):
							back = wlink[wcount+1]
						else:
							back = "";
						wcount += 1;
						wposts = {"word":cword,"connect":wlink,"fwd":fwd,"back":back};
						result = atc.insert_one(wposts).inserted_id;
					wlink = []
			stc = []
			line = rf.readline().replace("\r","")
		rf.close()

client.close()
print("Done.")
