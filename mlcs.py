from pymongo import MongoClient
import random

client = MongoClient('localhost',27017)
db = client.MLC
atc = db.atc
while 1:
	findword = ""
	usrcmd = str(raw_input("\nTHE FIRST WORD: "))
	findword = usrcmd;
	wherefind = "back"
	cntword = [usrcmd];
	exact = 4;
	tmpext = 0;
	while findword != "":
		fword = []
		if tmpext > exact:
			cntword = [usrcmd];
			tmpext = 0;
			print(""),
		cntword.append(findword)

		print(findword),
		result = atc.find({"word":findword,"connect":{"$all":cntword}},{wherefind:1}).limit(5000);
		for item in result :
			fword.append(item[wherefind]);

		fwordset = set(fword)
		fwordtmp = {}

		for item in fwordset:
			fwordtmp[item] = fword.count(item);

		fwordsort = sorted(fwordtmp.items(), key=lambda x:x[1],reverse=True)
		choose = random.randint(0, len(fwordsort)/5)
		findword = fwordsort[choose][0]
		tmpext += 1;


client.close();