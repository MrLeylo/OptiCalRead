import pytemplate as temp


def expreBuilder(symbols,tags):
	symbols=symbols.sorted(symbols,key=lambda s: s.bBox[0])
	symbolTypeCatalog={'nonscripted':[['+','-','x','X','\\'+'times','/','=','\\'+'neq','\gt','\geq','\lt','\leq','\ldots','.','COMMA','!','\exists','\in','\\'+'forall','\\'+'rightarrow','(','[','\{','\infty']],'superscripted':[['\sin','\cos','\\'+'tan','\log','e','\pi'],['0','1','2','3','4','5','6','7','8','9']],'scripted':[['a','c','e','i','m','n','r','x','z','A','B','C','F','X','Y','\\'+'alpha','\\'+'beta','\gamma','\\'+'theta','\phi','\pm',')',']','\}','\\'+'times'],['b','d','f','k','t'],['g','j','p','y']],'sumlike':[['\sum','\pi','\\'+'int']],'limlike':[['\lim']],'rootlike':[['\sqrt']],'barlike':[['\div']]}
	for sNum in range(len(symbols)):
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
			
