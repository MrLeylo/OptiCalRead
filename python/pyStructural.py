import pytemplate as temp
import pyDom as dom
import copy

def expreBuilder(symbols,tag):
	auxL=zip(symbols,tag)
	zs=sorted(auxL,key=lambda x: x[0].bBox[0])
	symbols,tag=map(list,zip(*zs))
	#symbolTypeCatalog={'nonscripted':[['+','-','x','X','\\'+'times','/','=','\\'+'neq','\gt','\geq','\lt','\leq','\ldots','.','COMMA','!','\exists','\in','\\'+'forall','\\'+'rightarrow','(','[','\{','\infty']],'superscripted':[['\sin','\cos','\\'+'tan','\log','e','\pi'],['0','1','2','3','4','5','6','7','8','9']],'scripted':[['a','c','e','i','m','n','r','x','z','A','B','C','F','X','Y','\\'+'alpha','\\'+'beta','\gamma','\\'+'theta','\phi','\pm',')',']','\}','\\'+'times'],['b','d','f','k','t'],['g','j','p','y']],'sumlike':[['\sum','\pi','\\'+'int']],'limlike':[['\lim']],'rootlike':[['\sqrt']],'barlike':[['\div']]}
	symbolTypeCatalog={'nonscripted':[['+','-','\\'+'times','/','=','\\'+'neq','\gt','\geq','\lt','\leq','\ldots','.','COMMA','!','\exists','\in','\\'+'forall','\\'+'rightarrow','(','[','\{','\infty']],'superscripted':[['\sin','\cos','\\'+'tan','\log','e','\pi'],['0','1','2','3','4','5','6','7','8','9']],'scripted':[['a','c','e','i','m','n','r','x','z','A','B','C','F','X','Y','\\'+'alpha','\\'+'beta','\gamma','\\'+'theta','\phi','\pm',')',']','\}','\\'+'times'],['b','d','f','k','t'],['g','j','p','y']],'sumlike':[['\sum','\pi','\\'+'int']],'limlike':[['\lim']],'rootlike':[['\sqrt']],'barlike':[['\div']]}
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
		if symbol.tag=='-':
			symbol.bBox[2]=symbol.center-((symbol.bBox[1]-symbol.bBox[0])/2)
			symbol.bBox[3]=symbol.center+((symbol.bBox[1]-symbol.bBox[0])/2)
	dominations=[]
	print symbols[6].outbBox,',',symbols[6].bBox,',',symbols[6].tag,',',symbols[8].centroid
	for curSNum in range(len(symbols)):
		for candSNum in range(len(symbols)):
			if curSNum!=candSNum:
				if symbols[curSNum].kinds[0]=='blik':
					if symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].outbBox[0]:
						if symbols[candSNum].centroid[0]<symbols[curSNum].centroid[0]:
							dominations.append(dom.hardDomination('above',symbols[curSNum],symbols[candSNum]))
						else:
							dominations.append(dom.hardDomination('below',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='supsc':
					if symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and symbols[candSNum].centroid[1]>symbols[curSNum].outbBox[2] and ((symbols[curSNum].bBox[1]-symbols[curSNum].bBox[0])*(symbols[curSNum].bBox[3]-symbols[curSNum].bBox[2]))>((symbols[candSNum].bBox[1]-symbols[candSNum].bBox[0])*(symbols[candSNum].bBox[3]-symbols[candSNum].bBox[2])):
						dominations.append(dom.hardDomination('superscript',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='sc':
					if symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and symbols[candSNum].centroid[1]>symbols[curSNum].outbBox[2] and ((symbols[curSNum].bBox[1]-symbols[curSNum].bBox[0])*(symbols[curSNum].bBox[3]-symbols[curSNum].bBox[2]))>((symbols[candSNum].bBox[1]-symbols[candSNum].bBox[0])*(symbols[candSNum].bBox[3]-symbols[candSNum].bBox[2])):
						dominations.append(dom.hardDomination('superscript',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]>symbols[curSNum].subThresh and symbols[candSNum].centroid[1]<symbols[curSNum].outbBox[3] and ((symbols[curSNum].bBox[1]-symbols[curSNum].bBox[0])*(symbols[curSNum].bBox[3]-symbols[curSNum].bBox[2]))>((symbols[candSNum].bBox[1]-symbols[candSNum].bBox[0])*(symbols[candSNum].bBox[3]-symbols[candSNum].bBox[2])):
						dominations.append(dom.hardDomination('subscript',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='slik':
					if symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].outbBox[0] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh:
						dominations.append(dom.hardDomination('above',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].outbBox[0] and symbols[candSNum].centroid[1]>symbols[curSNum].subThresh:
						dominations.append(dom.hardDomination('below',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]>symbols[curSNum].bBox[0] and symbols[candSNum].centroid[0]<symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]>symbols[curSNum].superThresh and symbols[candSNum].centroid[1]<symbols[curSNum].subThresh:
						dominations.append(dom.hardDomination('inside',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='llik':
					if symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and ((symbols[curSNum].bBox[1]-symbols[curSNum].bBox[0])*(symbols[curSNum].bBox[3]-symbols[curSNum].bBox[2]))>((symbols[candSNum].bBox[1]-symbols[candSNum].bBox[0])*(symbols[candSNum].bBox[3]-symbols[candSNum].bBox[2])):
						dominations.append(dom.hardDomination('superscript',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].outbBox[0] and symbols[candSNum].centroid[1]>symbols[curSNum].subThresh:
						dominations.append(dom.hardDomination('below',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='rlik':
					if symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and symbols[candSNum].centroid[1]>symbols[curSNum].outbBox[2] and ((symbols[curSNum].bBox[1]-symbols[curSNum].bBox[0])*(symbols[curSNum].bBox[3]-symbols[curSNum].bBox[2]))>((symbols[candSNum].bBox[1]-symbols[candSNum].bBox[0])*(symbols[candSNum].bBox[3]-symbols[candSNum].bBox[2])):
						dominations.append(dom.hardDomination('superscript',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]>symbols[curSNum].outbBox[0] and symbols[candSNum].centroid[0]<symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and symbols[candSNum].centroid[1]>symbols[curSNum].outbBox[2]:
						dominations.append(dom.hardDomination('above',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]>symbols[curSNum].bBox[0] and symbols[candSNum].centroid[0]<symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]>symbols[curSNum].bBox[2] and symbols[candSNum].centroid[1]<symbols[curSNum].bBox[3]:
						dominations.append(dom.hardDomination('inside',symbols[curSNum],symbols[candSNum]))
	for curSNum in range(len(symbols)):
		noSoft=True
		canGoOn=True
		c=0
		if hasattr(symbols[curSNum],'superThresh'):
			limUp=symbols[curSNum].superThresh
		else:
			limUp=symbols[curSNum].bBox[2]
		while c<len(symbols) and noSoft and canGoOn:
			if c!=curSNum and symbols[c].centroid[1]>limUp and symbols[c].centroid[1]<symbols[curSNum].bBox[3] and symbols[c].centroid[0]>symbols[curSNum].bBox[1]:
				dominators=[]
				for dA in dominations:
					if dA.submissive.ref==symbols[c].ref:
						dominators.append(dA.dominant.ref)
				if len(dominators)==0:
					dominations.append(dom.softDomination('rightNeigh',symbols[curSNum],symbols[c]))
					noSoft=False
				else:
					canGoOn==False
				del dominators
			c+=1
	print [[do.dominant.tag[:-1],do.submissive.tag[:-1]] for do in dominations]
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
	print [[do.dominant.tag[:-1],do.submissive.tag[:-1]] for do in dominations]
	hardDomed=[]
	for domi in dominations:
		if isinstance(domi,dom.hardDomination):
			hardDomed.append(domi.submissive.ref)
	print hardDomed
	print softDomed
	dominantBaseline=[]
	for sNum in range(len(symbols)):
		if sNum not in hardDomed:
			dominantBaseline.append(sNum)
	print dominantBaseline
	for dBlSym in dominantBaseline:
		if dBlSym in softDomed:
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
	print fullSons
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
							if [symbols[dBlSym].ref,symbols[grandson].ref,dominations[hdomsList[[hdomsList[do][1] for do in range(len(hdomsList))].index(son)][2]].typedom] not in [[domina.dominant.ref,domina.submissive.ref,domina.typedom] for domina in dominations] and ((symbols[dBlSym].bBox[1]-symbols[dBlSym].bBox[0])*(symbols[dBlSym].bBox[3]-symbols[dBlSym].bBox[2]))>((symbols[grandson].bBox[1]-symbols[grandson].bBox[0])*(symbols[grandson].bBox[3]-symbols[grandson].bBox[2])):
								#print [symbols[dBlSym],symbols[grandson],dominations[hdomsList[[hdomsList[do][1] for do in range(len(hdomsList))].index(son)][2]].typedom]
								dominations.append(dom.hardDomination(dominations[hdomsList[[hdomsList[do][1] for do in range(len(hdomsList))].index(son)][2]].typedom,symbols[dBlSym],symbols[grandson]))
					parents=[]
					grandParents=[]
					for d in hdomsList:
						if d[1]==dBlSym:
							grandParents.append(d)
						elif d[1]==son:
							parents.append(d)
					for grandParent in grandParents:
						if grandParent in parents:
							del dominations[grandParent[2]]
							c+=1
				fullSons.extend(sons)
	print [[do.dominant.tag[:-1],do.submissive.tag[:-1]] for do in dominations]
	expression=dominations
	return expression
	
def dominates(father,doms,td):
	sons=[]
	if td=='hard':
		tip=dom.hardDomination
	elif td=='soft':
		tip=dom.softDomination
	for domin in doms:
		if domin.dominant.ref==father and isinstance(domin,tip):
			#print domin.dominant
			#print domin.submissive
			sons.append(domin.submissive.ref)
	return sons
