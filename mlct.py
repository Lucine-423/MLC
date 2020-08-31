from pymongo import MongoClient
import numpy as np
import pdb
client = MongoClient('localhost',27017)
db = client.MLC
atc = db.atc
tnk = db.tnk

def list_sort_hw(result,wherefind):
	fword = []
	for item in result :
			fword.append(item[wherefind]);

	fwordset = set(fword)
	fwordtmp = {}
	fwordsort = []
	for item in fwordset:
		fwordtmp[item] = fword.count(item);
		fwordsort = sorted(fwordtmp.items(), key=lambda x:x[1],reverse=True)
	return fwordsort

def create_tclist(result):
	tclist = []
	for item in result :
			tclist.append(item["connect"])
	return tclist

def lstndx(tclist, cntw):
	lndx = []
	vndx = []
	for cnti in tclist:
		if set(cntw).issubset(set(cnti)) == True:
			#print(cnti)
			#pdb.set_trace()
			tndx = []
			fnum = cnti.count(cntw[0])
			tndx.append(cnti.index(cntw[0]))
			exist = 1;
			while exist:
				try:
					tndx.append(cnti.index(cntw[0],tndx[-1]+1))
				except :
					exist = 0;

			for i in range(fnum):
				for k in range(1,len(cntw)):
					nears = []
					ndx = cnti.index(cntw[k])
					lmndx = ndx
					if ndx - tndx[i] > 0:
							nears.append(ndx - tndx[i])
					exist = 1;
					while exist:
						try:
							ndx = cnti.index(cntw[k],lmndx+1)
							lmndx = ndx;
							if ndx - tndx[i] > 0:
								nears.append(ndx - tndx[i])
						except:
							exist = 0;
						
					if len(nears):
						mndx = min(nears)+tndx[i];
						lndx.append(mndx)
				vcndx = []
				if len(lndx):	
					lndx.append(tndx[i])	
					acndx = np.array(lndx)
					vcndx.append(np.std(acndx,axis=0))
			if len(vcndx):
				vndx.append(min(vcndx))
	if len(vndx):
		vrndx = np.array(vndx)
		rndx = np.mean(vrndx)
	else :
		rndx = -1;
	return rndx

def deeper(m_target,f_cntw,m_sentv,depth):
	tlist = atc.find({"word":m_target,"connect":{"$all":f_cntw}},{"connect":1,"back":1}).limit(100000)
	#pdb.set_trace()
	fsort = list_sort_hw(tlist,"back")
	if len(fsort):
		for alyw in fsort:
			m_cntw = list(f_cntw)
			if alyw[1] < sentv:
				break
			if alyw[0] != m_cntw[-1]:
				m_cntw.append(alyw[0])
				#i_target = alyw[0]
				rtclist = atc.find({"word":m_target},{"connect":1}).limit(1000)
				tclist = create_tclist(rtclist)
				dcvt = lstndx(tclist,m_cntw)
				#print(m_cntw)
				#print(dcvt)
				if dcvt < 10 and dcvt > 0:
					print(m_cntw)
					print(dcvt)
				#pdb.set_trace()
				if (depth > 1):
					deeper(m_target,m_cntw,m_sentv,depth-1)
				else:
					return 0;

target = "you"
sentv = 12
dptv = 2
#alist = atc.find({"word":target},{"connect":1,"back":1}).limit(10000)

fword = {}

#sortlist = list_sort_hw(alist,"back");


deeper(target,[target],sentv,dptv)

client.close();


