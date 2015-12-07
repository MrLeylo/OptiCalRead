import pytemplate as temp
import pyDom as dom

def expreBuilder(symbols,tags):
	symbols=symbols.sorted(symbols,key=lambda s: s.bBox[0])
	symbolTypeCatalog={'nonscripted':[['+','-','x','X','\\'+'times','/','=','\\'+'neq','\gt','\geq','\lt','\leq','\ldots','.','COMMA','!','\exists','\in','\\'+'forall','\\'+'rightarrow','(','[','\{','\infty']],'superscripted':[['\sin','\cos','\\'+'tan','\log','e','\pi'],['0','1','2','3','4','5','6','7','8','9']],'scripted':[['a','c','e','i','m','n','r','x','z','A','B','C','F','X','Y','\\'+'alpha','\\'+'beta','\gamma','\\'+'theta','\phi','\pm',')',']','\}','\\'+'times'],['b','d','f','k','t'],['g','j','p','y']],'sumlike':[['\sum','\pi','\\'+'int']],'limlike':[['\lim']],'rootlike':[['\sqrt']],'barlike':[['\div']]}
	for sNum in range(len(symbols)):
		symbols[sNum].tagUntagged(tag[sNum],sNum)
		if tag[sNum][:-1] not in [v1 for vx in [v2 for vy in symbolTypeCatalog.values() for v2 in vy] for v1 in vx]:
			print s[:-1],'not in database'
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
	dominations=[]
	for curSNum in range(len(symbols)):
		for candSNum in range(len(symbols)):
			if curSNum!=candSNum:
				if symbols[curSNum].kinds[0]=='blik':
					if symbols[candSNum].centroid[0]<symbols[curSNum].outsidebBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].outsidebBox[0]:
						if symbols[candSNum].centroid[0]<symbols[curSNum].centroid[0]:
							dominations.append(dom.hardDomination('above',symbols[curSNum],symbols[candSNum]))
						else:
							dominations.append(dom.hardDomination('below',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='supsc':
					if symbols[candSNum].centroid[0]<symbols[curSNum].outsidebBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and symbols[candSNum].centroid[1]>symbols[curSNum].outsidebBox[2]:
						dominations.append(dom.hardDomination('superscript',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='sc':
					if symbols[candSNum].centroid[0]<symbols[curSNum].outsidebBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and symbols[candSNum].centroid[1]>symbols[curSNum].outsidebBox[2]:
						dominations.append(dom.hardDomination('superscript',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]<symbols[curSNum].outsidebBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]>symbols[curSNum].subThresh and symbols[candSNum].centroid[1]<symbols[curSNum].outsidebBox[3]:
						dominations.append(dom.hardDomination('subscript',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='slik':
					if symbols[candSNum].centroid[0]<symbols[curSNum].outsidebBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].outsidebBox[0] and symbols[candSNum].centroid[1]<symbols[candSNum].superThresh:
						dominations.append(dom.hardDomination('above',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]<symbols[curSNum].outsidebBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].outsidebBox[0] and symbols[candSNum].centroid[1]>symbols[candSNum].subThresh:
						dominations.append(dom.hardDomination('below',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]>symbols[curSNum].bBox[0] and symbols[candSNum].centroid[0]<symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]>symbols[curSNum].superThresh and symbols[candSNum].centroid[1]<symbols[curSNum].subThresh:
						dominations.append(dom.hardDomination('inside',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='llik':
					if symbols[candSNum].centroid[0]<symbols[curSNum].outsidebBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]<symbols[candSNum].superThresh:
						dominations.append(dom.hardDomination('superscript',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]<symbols[curSNum].outsidebBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].outsidebBox[0] and symbols[candSNum].centroid[1]>symbols[candSNum].subThresh:
						dominations.append(dom.hardDomination('below',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='rlik':
					if symbols[candSNum].centroid[0]<symbols[curSNum].outsidebBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and symbols[candSNum].centroid[1]>symbols[curSNum].outsidebBox[2]:
						dominations.append(dom.hardDomination('superscript',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]>symbols[curSNum].outsidebBox[0] and symbols[candSNum].centroid[0]<symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and symbols[candSNum].centroid[1]>symbols[curSNum].outsidebBox[2]:
						dominations.append(dom.hardDomination('above',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]>symbols[curSNum].bBox[0] and symbols[candSNum].centroid[0]<symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]>symbols[curSNum].bBox[2] and symbols[candSNum].centroid[1]<symbols[curSNum].bBox[3]:
						dominations.append(dom.hardDomination('inside',symbols[curSNum],symbols[candSNum]))
	for symbol in symbols:
		if symbol.tag='-':
			symbol.bBox[2]=symbol.center-((symbol.bBox[1]-symbol.bBox[0])/2)
			symbol.bBox[3]=symbol.center+((symbol.bBox[1]-symbol.bBox[0])/2)
	for curSNum in range(len(symbols)):
		noSoft=True
		canGoOn=True
		c=0
		while c<len(symbols) and noSoft and canGoOn:
			if c!=curSNum and symbols[c].centroid[1]>symbols[curSNum].bBox[2] and symbols[c].centroid[1]<symbols[curSNum].bBox[3] and symbols[c].centroid[0]>symbols[curSNum].bBox[1]:
				dominators=[]
				for dA in dominations:
					if dA.submissive.ref==symbols[c]:
						dominators.append(dA.dominant.ref)
				if len(dominators)==0:
					dominations.append(dom.softDomination('rightNeigh',symbols[curSNum],symbols[c]))
					noSoft=False
				else:
					canGoOn==False
				del dominators
			c+=1
	softDomed=[]
	wheresD=[]
	c=0
	for domi in dominations:
		if type(domi)==softDomination:
			softDomed.append(domi.submissive.ref)
			wheresD.append(c)
		c+=1
	c=0
	for sNum in range(len(symbols)):
		while softDomed.count(sNum)>1:
			del dominations[wheresD[softDomed.index(sNum)]-c]
			softDomed.remove(sNum)
			c+=1
	hardDomed=[]
	for domi in dominations:
		if type(domi)=='hardDomination':
			hardDomed.append(domi.submissive.ref)	
	dominantBaseline=[]
	for sNum in range(len(symbols)):
		if sNum not in hardDomed:
			dominantBaseline.append(sNum)
	for dBlSym in dominantBaseline:
		if dBlSym in softDomed:
			if dominations[wheresD[softDomed.index(dBlSym)]-c].dominant not in dominantBaseline:
				dominantBaseline.remove(dBlSym)
	for i in range(len(dominantBaseline)-1):
		if softDomination('rightNeigh',dominantBaseline[i],dominantBaseline[i+1]) not in dominations:
			dominations.append('rightNeigh',dominantBaseline[i],dominantBaseline[i+1])
	hdomsList=[]
	cd=0
	for d in dominations:
		if type(d)=='hardDomination':
			hdomsList.append([d.dominant,d.submissive,cd])
		cd+=1
	sdomsList=[]
	cd=0
	for d in dominations:
		if type(d)=='softDomination':
			sdomsList.append([d.dominant,d.submissive,cd])
		cd+=1
	fullSons=dominantBaseline #!!!!!!!!!!!!!!!!!
	c=0
	while len(fullSons)!=0:
		currentLine=fullSons  #!!!!!!!!!!!!!!!!!
		fullSons=[]
		for dBlSym in currentline:
			sons=dominates(dBlSym,dominations,'hard')
			for son in sons:
				if len(dominates(dBlSym,dominations,'soft'))!=0:
					grandsons=dominates(dBlSym,dominations,'soft')
					for grandson in grandsons:
						if dom.hardDomination(symbol[son],symbol[grandson],dominations[hdomsList[[hdomsList[do,1] for do in range(len(hdomsList))].index(son),2]].typedom) not in dominations
							dominations.append(dom.hardDomination(symbol[son],symbol[grandson],dominations[hdomsList[[hdomsList[do,1] for do in range(len(hdomsList))].index(son),2]].typedom))
			parents=[]
			grandParents=[]
			for d in hdomsList:
				if d[1]==dBlSym:
					grandParents.append(d)
				elif d[1]==son:
					parents.append(d)
			for grandParent in grandParents:
				if grandParent in parents:
					del dominations[grandParent[2]-c]
					c+=1
			fullSons.append(sons)
	return expression
	
def dominates(father,doms,td):
	sons=[]
	if td=='hard':
		tip='hardDomination'
	elif td=='soft':
		tip='softDomination'
	for dom in doms:
		if dom.dominant.ref==father and type(dom)==tip:
			sons.append(dom.submissive.ref)
	return sons
