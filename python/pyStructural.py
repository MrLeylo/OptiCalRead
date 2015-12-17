import pytemplate as temp
import pyDom as dom
import copy
import SClass as nsi

def expreBuilder(symbols,tag):
	auxL=zip(symbols,tag)
	zs=sorted(auxL,key=lambda x: x[0].bBox[0])
	symbols,tag=map(list,zip(*zs))
	#symbolTypeCatalog={'nonscripted':[['+','-','x','X','\\'+'times','/','=','\\'+'neq','\gt','\geq','\lt','\leq','\ldots','.','COMMA','!','\exists','\in','\\'+'forall','\\'+'rightarrow','(','[','\{','\infty']],'superscripted':[['\sin','\cos','\\'+'tan','\log','e','\pi'],['0','1','2','3','4','5','6','7','8','9']],'scripted':[['a','c','e','i','m','n','r','x','z','A','B','C','F','X','Y','\\'+'alpha','\\'+'beta','\gamma','\\'+'theta','\phi','\pm',')',']','\}','\\'+'times'],['b','d','f','k','t'],['g','j','p','y']],'sumlike':[['\sum','\pi','\\'+'int']],'limlike':[['\lim']],'rootlike':[['\sqrt']],'barlike':[['\div']]}
	symbolTypeCatalog={'nonscripted':[['+','-','\\'+'times','/','=','\\'+'neq','\gt','\geq','\lt','\leq','\ldots','.','COMMA','!','\exists','\in','\\'+'forall','\\'+'rightarrow','(','[','\{','\infty']],'superscripted':[['\sin','\cos','\\'+'tan','\log','e','\pi'],['0','1','2','3','4','5','6','7','8','9']],'scripted':[['a','c','e','i','m','n','r','x','z','A','B','C','F','X','Y','\\'+'alpha','\\'+'beta','\gamma','\\'+'theta','\phi','\pm',')',']','\}'],['b','d','f','k','t','\\'+'int'],['g','j','p','y']],'sumlike':[['\sum','\pi']],'limlike':[['\lim']],'rootlike':[['\sqrt']],'barlike':[['\div']]}
	for sNum in range(len(symbols)):
		symbols[sNum].tagUntagged(tag[sNum],sNum)
		if tag[sNum][:-1] not in [v1 for vx in [v2 for vy in symbolTypeCatalog.values() for v2 in vy] for v1 in vx]:
			print tag[sNum][:-1],'not in database'
		else:
			if tag[sNum][:-1] in [v2 for vy in symbolTypeCatalog['nonscripted'] for v2 in vy]:
				symbols[sNum].setRegions('nosc','cent')
			elif tag[sNum][:-1] in [v2 for vy in symbolTypeCatalog['superscripted'] for v2 in vy]:
				if tag[sNum][:-1] in symbolTypeCatalog['superscripted'][0]:
					symbols[sNum].setRegions('supsc','cent')
				elif tag[sNum][:-1] in symbolTypeCatalog['superscripted'][1]:
					symbols[sNum].setRegions('supsc','asc')
			elif tag[sNum][:-1] in [v2 for vy in symbolTypeCatalog['scripted'] for v2 in vy]:
				if tag[sNum][:-1] in symbolTypeCatalog['scripted'][0]:
					symbols[sNum].setRegions('sc','cent')
				elif tag[sNum][:-1] in symbolTypeCatalog['scripted'][1]:
					symbols[sNum].setRegions('sc','asc')
				elif tag[sNum][:-1] in symbolTypeCatalog['scripted'][2]:
					symbols[sNum].setRegions('sc','desc')
			elif tag[sNum][:-1] in [v2 for vy in symbolTypeCatalog['sumlike'] for v2 in vy]:
				symbols[sNum].setRegions('slik','cent')
			elif tag[sNum][:-1] in [v2 for vy in symbolTypeCatalog['limlike'] for v2 in vy]:
				symbols[sNum].setRegions('llik','cent')
			elif tag[sNum][:-1] in [v2 for vy in symbolTypeCatalog['rootlike'] for v2 in vy]:
				symbols[sNum].setRegions('rlik','cent')
			elif tag[sNum][:-1] in [v2 for vy in symbolTypeCatalog['barlike'] for v2 in vy]:
				symbols[sNum].setRegions('blik','cent')
			print symbols[sNum].kinds
	for symbol in symbols:
		if symbol.tag[:-1]=='-':
			symbol.bBox[2]=symbol.center[1]-((symbol.bBox[1]-symbol.bBox[0])/2)
			symbol.bBox[3]=symbol.center[1]+((symbol.bBox[1]-symbol.bBox[0])/2)
	dominations=[]
	for curSNum in range(len(symbols)):
		for candSNum in range(len(symbols)):
			if curSNum!=candSNum:
				if symbols[curSNum].kinds[0]=='blik':
					if symbols[candSNum].centroid[0]<symbols[curSNum].bBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[0]:
						if symbols[candSNum].centroid[1]<symbols[curSNum].centroid[1]:
							dominations.append(dom.hardDomination('above',symbols[curSNum],symbols[candSNum]))
						else:
							dominations.append(dom.hardDomination('below',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='supsc':
					if symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[0] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and symbols[candSNum].centroid[1]>symbols[curSNum].outbBox[2] and symbols[candSNum].bBox[3]<symbols[curSNum].bBox[3]:
						dominations.append(dom.hardDomination('superscript',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='sc':
					auxMarker=symbols[curSNum].bBox[0]
					if symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>auxMarker and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and symbols[candSNum].centroid[1]>symbols[curSNum].outbBox[2] and symbols[candSNum].bBox[3]<symbols[curSNum].bBox[3]:
						dominations.append(dom.hardDomination('superscript',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[0] and symbols[candSNum].centroid[1]>symbols[curSNum].subThresh and symbols[candSNum].centroid[1]<symbols[curSNum].outbBox[3] and symbols[candSNum].bBox[2]>symbols[curSNum].bBox[2]:
						dominations.append(dom.hardDomination('subscript',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='slik':
					if symbols[candSNum].centroid[0]<symbols[curSNum].bBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[0] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh:
						dominations.append(dom.hardDomination('above',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]<symbols[curSNum].bBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[0] and symbols[candSNum].centroid[1]>symbols[curSNum].subThresh:
						dominations.append(dom.hardDomination('below',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]>symbols[curSNum].bBox[0] and symbols[candSNum].centroid[0]<symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]>symbols[curSNum].superThresh and symbols[candSNum].centroid[1]<symbols[curSNum].subThresh:
						dominations.append(dom.hardDomination('inside',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='llik':
					if symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and symbols[candSNum].bBox[3]<symbols[curSNum].bBox[3]:
						dominations.append(dom.hardDomination('superscript',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbos[candSNum].centroid[0]>symbols[curSNum].outbBox[0] and symbols[candSNum].centroid[1]>symbols[curSNum].subThresh:
						dominations.append(dom.hardDomination('below',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='rlik':
					if symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and symbols[candSNum].centroid[1]>symbols[curSNum].outbBox[2] and symbols[candSNum].bBox[3]<symbols[curSNum].bBox[3]:
						dominations.append(dom.hardDomination('superscript',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]>symbols[curSNum].outbBox[0] and symbols[candSNum].centroid[0]<symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and symbols[candSNum].centroid[1]>symbols[curSNum].outbBox[2]:
						dominations.append(dom.hardDomination('above',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]>symbols[curSNum].bBox[0] and symbols[candSNum].centroid[0]<symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]>symbols[curSNum].bBox[2] and symbols[candSNum].centroid[1]<symbols[curSNum].bBox[3]:
						dominations.append(dom.hardDomination('inside',symbols[curSNum],symbols[candSNum]))
	print [[do.dominant.tag[:-1],do.dominant.ref,do.submissive.tag[:-1],do.submissive.ref,do.typedom] for do in dominations]
	print symbols[4].bBox[2],symbols[4].bBox[3],symbols[4].bBox[1],symbols[6].centroid
	for curSNum in range(len(symbols)):
		noSoft=True
		canGoOn=True
		c=0
		if hasattr(symbols[curSNum],'superThresh'):
			limUp=symbols[curSNum].superThresh
		else:
			limUp=symbols[curSNum].bBox[2]
		while c<len(symbols) and noSoft and canGoOn:
			if c!=curSNum and symbols[c].centroid[1]>limUp and symbols[c].centroid[1]<symbols[curSNum].bBox[3] and symbols[c].centroid[0]>symbols[curSNum].bBox[1] and symbols[curSNum].centroid[1]>symbols[c].bBox[2] and symbols[curSNum].centroid[1]<symbols[c].bBox[3]:      #!!!!!!!!!!!!!!!!!!!!!!!!!
				dominators=[]
				for dA in dominations:
					if dA.submissive.ref==symbols[c].ref and isinstance(dA,dom.hardDomination):
						dominators.append(dA.dominant.ref)
						print ':::::::::::::::::::::::::::::',symbols[c].ref,symbols[curSNum].ref,dA.dominant.ref,':::::::::::::::::::::::::::::'
				if len(dominators)==0:
					dominations.append(dom.softDomination('rightNeigh',symbols[curSNum],symbols[c]))
					noSoft=False
				else:
					if [dominators[0],symbols[curSNum].ref] in [[doi.dominant.ref,doi.submissive.ref] for doi in dominations]:
						#del dominations[[[doi.dominant.ref,doi.submissive.ref] for doi in dominations].index([symbols[curSNum].ref,dominators[0]])]
						dominations.append(dom.softDomination('rightNeigh',symbols[curSNum],symbols[c]))
						noSoft=False
					else:
						canGoOn=False
				del dominators
			c+=1
	print [[do.dominant.tag[:-1],do.dominant.ref,do.submissive.tag[:-1],do.submissive.ref] for do in dominations]
	softDomed=[]
	wheresD=[]
	c=0
	for domi in dominations:
		if isinstance(domi,dom.softDomination):
			softDomed.append(domi.submissive.ref)
			wheresD.append(c)
		c+=1
	for sNum in range(len(symbols)):
		while softDomed.count(sNum)>1:
			indecs=softDomed.index(sNum)
			del dominations[wheresD[indecs]]
			softDomed.remove(sNum)
			del wheresD[indecs]
			for i in range(indecs,len(wheresD)):
				wheresD[i]-=1
	print [[do.dominant.tag[:-1],do.dominant.ref,do.submissive.tag[:-1],do.submissive.ref,do.typedom] for do in dominations]
	hardDomed=[]
	whereH=[]
	c=0
	for domi in dominations:
		if isinstance(domi,dom.hardDomination):
			hardDomed.append(domi.submissive.ref)
			whereH.append(c)
		c+=1
	print hardDomed
	print softDomed
	for domn in dominations:
		if [domn.dominant.ref,domn.submissive.ref] in [[domt.submissive.ref,domt.dominant.ref] for domt in dominations]:
			del dominations[[[domt.submissive.ref,domt.dominant.ref] for domt in dominations].index([domn.dominant.ref,domn.submissive.ref])]
			for i in range(hardDomed.index(domn.dominant.ref),len(whereH)):
				whereH[i]-=1
			for i in range(len(wheresD)):
				wheresD[i]-=1
			del hardDomed[hardDomed.index(domn.dominant.ref)]
	print [[do.dominant.tag[:-1],do.dominant.ref,do.submissive.tag[:-1],do.submissive.ref,do.typedom] for do in dominations] 
	dominantBaseline=[]
	for sNum in range(len(symbols)):
		if sNum not in hardDomed:
			dominantBaseline.append(sNum)
	print dominantBaseline
	for dBlSym in dominantBaseline:
		if dBlSym in softDomed:
			print wheresD[softDomed.index(dBlSym)],',',len(dominations)
			if dominations[wheresD[softDomed.index(dBlSym)]].dominant.ref not in dominantBaseline:
				dominantBaseline.remove(dBlSym)
	for i in range(len(dominantBaseline)-1):
		if ['rightNeigh',symbols[dominantBaseline[i]].ref,symbols[dominantBaseline[i+1]].ref] not in [[domin.typedom,domin.dominant.ref,domin.submissive.ref] for domin in dominations]:
			dominations.append(dom.softDomination('rightNeigh',symbols[dominantBaseline[i]],symbols[dominantBaseline[i+1]]))
	print dominantBaseline
	hdomsList=[]
	print [[do.dominant.tag[:-1],do.submissive.tag[:-1]] for do in dominations]
	cd=0
	for d in dominations:
		if isinstance(d,dom.hardDomination):
			hdomsList.append([d.dominant.ref,d.submissive.ref,cd])
		cd+=1
	sdomsList=[]
	cd=0
	for d in dominations:
		if isinstance(d,dom.softDomination):
			sdomsList.append([d.dominant.ref,d.submissive.ref,cd])
		cd+=1
	print hdomsList
	print sdomsList
	fullSons=copy.deepcopy(dominantBaseline)
	c=0
	print [[do.dominant.tag[:-1],do.submissive.tag[:-1]] for do in dominations]
	while len(fullSons)!=0:
		currentLine=copy.deepcopy(fullSons)
		fullSons=[]
		for dBlSym in currentLine:
			sons=dominates(dBlSym,dominations,'hard')
			if len(sons)!=0:
				for son in sons:
					if len(dominates(dBlSym,dominations,'soft'))!=0:
						grandsons=dominates(son,dominations,'soft')
						for grandson in grandsons:
							if [symbols[dBlSym].ref,symbols[grandson].ref,dominations[hdomsList[[hdomsList[do][1] for do in range(len(hdomsList))].index(son)][2]].typedom] not in [[domina.dominant.ref,domina.submissive.ref,domina.typedom] for domina in dominations]:
								#print [symbols[dBlSym],symbols[grandson],dominations[hdomsList[[hdomsList[do][1] for do in range(len(hdomsList))].index(son)][2]].typedom]
								dominations.append(dom.hardDomination(dominations[hdomsList[[hdomsList[do][1] for do in range(len(hdomsList))].index(son)][2]].typedom,symbols[dBlSym],symbols[grandson]))
								hdomsList.append([symbols[dBlSym].ref,symbols[grandson].ref,len(dominations)-1])
					parents=[]
					grandParents=[]
					for d in hdomsList:
						if d[1]==dBlSym:
							grandParents.append(d)
						elif d[1]==son:
							parents.append(d)
					for parent in parents:
						if parent[0] in [g[0] for g in grandParents]:
							where=[h[2] for h in hdomsList].index(parent[2])
							del dominations[parent[2]]
							for i in range(where,len(hdomsList)):
								hdomsList[i][2]-=1
							c+=1
				fullSons.extend(sons)
	print [[do.dominant.tag[:-1],do.dominant.ref,do.submissive.tag[:-1],do.submissive.ref] for do in dominations]
	for sym in symbols:
		sons=dominates(sym.ref,dominations,'hard')
		sons=sorted(sons)
		domdic={}
		for son in sons:
			tip=dominations[[[doi.dominant.ref,doi.submissive.ref] for doi in dominations].index([sym.ref,son])].typedom
			if tip not in domdic:
				domdic[tip]=[]
			domdic[tip].append(son)
		gone=[]
		for tip in domdic:
			for ele in range(len(domdic[tip])-1):
				if symbols[domdic[tip][ele]].ref not in gone:
					if [domdic[tip][ele],domdic[tip][ele+1],'rightNeigh'] not in [[doi.dominant.ref,doi.submissive.ref,doi.typedom] for doi in dominations]:
						if symbols[domdic[tip][ele+1]].centroid[1]<symbols[domdic[tip][ele]].bBox[2] and symbols[domdic[tip][ele]].kinds[0]!='blik' and symbols[domdic[tip][ele]].kinds[0]!='nosc':							
							while symbols[domdic[tip][ele+1]].ref in [doim.submissive.ref for doim in dominations]:
								del dominations[[doim.submissive.ref for doim in dominations].index(symbols[domdic[tip][ele+1]].ref)]
							if symbols[domdic[tip][ele+1]].centroid[0]>symbols[domdic[tip][ele]].bBox[1]:
								if symbols[domdic[tip][ele]].kinds[0]=='slik':
									dominations.append(dom.hardDomination('above',symbols[domdic[tip][ele]],symbols[domdic[tip][ele+1]]))
								else:
									dominations.append(dom.hardDomination('superscript',symbols[domdic[tip][ele]],symbols[domdic[tip][ele+1]]))
							else:
								if symbols[domdic[tip][ele]].kinds[0]=='slik' or symbols[domdic[tip][ele]].kinds[0]=='rlik':
									dominations.append(dom.hardDomination('above',symbols[domdic[tip][ele]],symbols[domdic[tip][ele+1]]))
								else:
									dominations.append(dom.hardDomination('superscript',symbols[domdic[tip][ele]],symbols[domdic[tip][ele+1]]))
						elif symbols[domdic[tip][ele+1]].centroid[1]>symbols[domdic[tip][ele]].bBox[3] and (symbols[domdic[tip][ele]].kinds[0]=='sc' or symbols[domdic[tip][ele]].kinds[0]=='slik' or symbols[domdic[tip][ele]].kinds[0]=='llik'):
							while symbols[domdic[tip][ele+1]].ref in [doim.submissive.ref for doim in dominations]:
								del dominations[[doim.submissive.ref for doim in dominations].index(symbols[domdic[tip][ele+1]].ref)]
							if symbols[domdic[tip][ele]].kinds[0]=='sc':
								dominations.append(dom.hardDomination('subscript',symbols[domdic[tip][ele]],symbols[domdic[tip][ele+1]]))
							else:
								dominations.append(dom.hardDomination('below',symbols[domdic[tip][ele]],symbols[domdic[tip][ele+1]]))
						else:
							dominations.append(dom.softDomination('rightNeigh',symbols[domdic[tip][ele]],symbols[domdic[tip][ele+1]]))
						gone.append(symbols[domdic[tip][ele+1]].ref)
	print [[do.dominant.tag[:-1],do.dominant.ref,do.submissive.tag[:-1],do.submissive.ref,do.typedom] for do in dominations]
	######################################################
	print dominantBaseline
	hdomsList=[]
	print [[do.dominant.tag[:-1],do.submissive.tag[:-1]] for do in dominations]
	cd=0
	for d in dominations:
		if isinstance(d,dom.hardDomination):
			hdomsList.append([d.dominant.ref,d.submissive.ref,cd])
		cd+=1
	sdomsList=[]
	cd=0
	for d in dominations:
		if isinstance(d,dom.softDomination):
			sdomsList.append([d.dominant.ref,d.submissive.ref,cd])
		cd+=1
	print hdomsList
	print sdomsList
	fullSons=copy.deepcopy(dominantBaseline)
	c=0
	print [[do.dominant.tag[:-1],do.submissive.tag[:-1]] for do in dominations]
	while len(fullSons)!=0:
		currentLine=copy.deepcopy(fullSons)
		fullSons=[]
		for dBlSym in currentLine:
			sons=dominates(dBlSym,dominations,'hard')
			if len(sons)!=0:
				for son in sons:
					if len(dominates(dBlSym,dominations,'soft'))!=0:
						grandsons=dominates(son,dominations,'soft')
						for grandson in grandsons:
							if [symbols[dBlSym].ref,symbols[grandson].ref,dominations[hdomsList[[hdomsList[do][1] for do in range(len(hdomsList))].index(son)][2]].typedom] not in [[domina.dominant.ref,domina.submissive.ref,domina.typedom] for domina in dominations]:
								#print [symbols[dBlSym],symbols[grandson],dominations[hdomsList[[hdomsList[do][1] for do in range(len(hdomsList))].index(son)][2]].typedom]
								dominations.append(dom.hardDomination(dominations[hdomsList[[hdomsList[do][1] for do in range(len(hdomsList))].index(son)][2]].typedom,symbols[dBlSym],symbols[grandson]))
								hdomsList.append([symbols[dBlSym].ref,symbols[grandson].ref,len(dominations)-1])
					parents=[]
					grandParents=[]
					for d in hdomsList:
						if d[1]==dBlSym:
							grandParents.append(d)
						elif d[1]==son:
							parents.append(d)
					for parent in parents:
						if parent[0] in [g[0] for g in grandParents]:
							where=[h[2] for h in hdomsList].index(parent[2])
							del dominations[parent[2]]
							for i in range(where,len(hdomsList)):
								hdomsList[i][2]-=1
							c+=1
				fullSons.extend(sons)
	print [[do.dominant.tag[:-1],do.dominant.ref,do.submissive.tag[:-1],do.submissive.ref,do.typedom] for do in dominations]
	for sIn in range(len(symbols)):
		following=dominates(sIn,dominations,'soft')
		following=sorted(following)
		while len(following)>1:
			if [following[0],following[len(following)-1]] in [[dmn.dominant.ref,dmn.submissive.ref] for dmn in dominations]:
				del dominations[[[doim.dominant.ref,doim.submissive.ref] for doim in dominations].index([sIn,following[len(following)-1]])]
			del following[len(following)-1]
	print [[do.dominant.tag[:-1],do.dominant.ref,do.submissive.tag[:-1],do.submissive.ref,do.typedom] for do in dominations]	
	auxiliarSyms=[s.ref for s in symbols]
	print auxiliarSyms
	while len(auxiliarSyms)!=0:
		cs=0
		yetNotDone=True
		print 'De moment:'
		print auxiliarSyms
		while cs!=len(auxiliarSyms) and yetNotDone:
			sons=dominates(auxiliarSyms[cs],dominations,'hard')
			print sons
			if all(son not in auxiliarSyms for son in sons):
				print auxiliarSyms[cs]
				yetNotDone=False
				domines={}
				for son in sons:
					tip=dominations[[[doi.dominant.ref,doi.submissive.ref] for doi in dominations].index([auxiliarSyms[cs],son])].typedom
					if tip not in domines:
						domines[tip]=[]
					domines[tip].append(symbols[son])
				symbols[auxiliarSyms[cs]]=symbolFamily(symbols[auxiliarSyms[cs]],domines)
				del auxiliarSyms[cs]
			cs+=1
	expression=''
	for dblIn in dominantBaseline:
		expression+=getTex(symbols[dblIn])
	#while '\\' in expression:
	#	print expression
	#	print 'a'+expression
	#	print buea
	#	expression=expression[:expression.index('\\')+1]+expression[expression.index('\\')+2:]
	#	print 'to:'+expression
	#	print buea
	print [[doi.dominant.ref,doi.submissive.ref,doi.typedom] for doi in dominations]
	print expression
	return dominations,expression
	
def dominates(father,doms,td):
	sons=[]
	if td=='hard':
		tip=dom.hardDomination
	elif td=='soft':
		tip=dom.softDomination
	for domin in doms:
		if domin.dominant.ref==father and isinstance(domin,tip):
			sons.append(domin.submissive.ref)
	return sons
	
def symbolFamily(symbol,symbolDomines):
	if symbol.kinds[0]=='supsc':
		if 'superscript' in symbolDomines:
			symbol.addSupsc(symbolDomines['superscript'])
	elif symbol.kinds[0]=='sc':
		if 'superscript' in symbolDomines:
			symbol.addSupsc(symbolDomines['superscript'])
		if 'subscript' in symbolDomines:
			symbol.addSubsc(symbolDomines['subscript'])
	elif symbol.kinds[0]=='slik':
		if 'above' in symbolDomines:
			symbol.addAb(symbolDomines['above'])
		if 'below' in symbolDomines:
			symbol.addBe(symbolDomines['below'])
		if 'inside' in symbolDomines:
			symbol.addIns(symbolDomines['inside'])
	elif symbol.kinds[0]=='llik':
		if 'superscript' in symbolDomines:
			symbol.addSupsc(symbolDomines['superscript'])
		if 'below' in symbolDomines:
			symbol.addBe(symbolDomines['below'])
	elif symbol.kinds[0]=='rlik':
		if 'superscript' in symbolDomines:
			symbol.addSupsc(symbolDomines['superscript'])
		if 'below' in symbolDomines:
			symbol.addBe(symbolDomines['below'])
		if 'inside' in symbolDomines:
			symbol.addIns(symbolDomines['inside'])
	elif symbol.kinds[0]=='blik':
		if 'above' in symbolDomines:
			symbol.addAb(symbolDomines['above'])
		if 'below' in symbolDomines:
			symbol.addBe(symbolDomines['below'])
	return symbol
	
def getTex(symbol):
	symbol.reTag()
	texExpr=''
	if symbol.kinds[0]=='nosc':
		texExpr+=symbol.texTag+' '
	elif symbol.kinds[0]=='supsc':
		texExpr+=symbol.texTag+' '
		if hasattr(symbol,'superscripts'):
			texExpr+='^{'
			for member in symbol.superscripts:
				texExpr+=getTex(member)
			texExpr+='}'
	elif symbol.kinds[0]=='sc':
		texExpr+=symbol.texTag+' '
		if hasattr(symbol,'superscripts'):
			texExpr+='^{'
			for member in symbol.superscripts:
				texExpr+=getTex(member)
			texExpr+='}'
		if hasattr(symbol,'subscripts'):
			texExpr+='_{'
			for member in symbol.subscripts:
				texExpr+=getTex(member)
			texExpr+='}'
	elif symbol.kinds[0]=='slik':
		texExpr+=symbol.texTag+' '
		if hasattr(symbol,'aboves') or hasattr(symbol,'belows'):
			if hasattr(symbol,'belows'):
				texExpr+='_{'
				for member in symbol.belows:
					texExpr+=getTex(member)
				texExpr+='}'
			if hasattr(symbol,'aboves'):
				texExpr+='^{'
				for member in symbol.aboves:
					texExpr+=getTex(member)
				texExpr+='}'
		if hasattr(symbol,'containing'):
			for member in symbol.containing:
				texExpr+=getTex(member)
	elif symbol.kinds[0]=='llik':
		texExpr+=symbol.texTag+' '
		if hasattr(symbol,'belows'):
			texExpr+='_{'
			for member in symbol.belows:
				texExpr+=getTex(member)
			texExpr+='}'
		if hasattr(symbol,'superscripts'):
			texExpr+='^{'
			for member in symbol.superscripts:
				texExpr+=getTex(member)
			texExpr+='}'
	elif symbol.kinds[0]=='rlik':
		texExpr+=symbol.texTag+' '
		if hasattr(symbol,'aboves'):
			texExpr+='['
			for member in symbol.aboves:
				texExpr+=getTex(member)
			texExpr+=']'
		if hasattr(symbol,'containing'):
			texExpr+='{'
			for member in symbol.containing:
				texExpr+=getTex(member)
			texExpr+='}'
		if hasattr(symbol,'superscripts'):
			texExpr+='^{'
			for member in symbol.superscripts:
				texExpr+=getTex(member)
			texExpr+='}'
	elif symbol.kinds[0]=='blik':
		texExpr+=symbol.texTag+' '
		texExpr+='{'
		if hasattr(symbol,'aboves'):
			for member in symbol.aboves:
				texExpr+=getTex(member)
		texExpr+='}'
		texExpr+='{'
		if hasattr(symbol,'belows'):
			for member in symbol.belows:
				texExpr+=getTex(member)
		texExpr+='}'
	return texExpr
