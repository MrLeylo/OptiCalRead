import numpy as np
import statistics
import operator
import math
import copy
import os
import pickle

def findConcentration(tagClassification):
	#featList=[feat for feat in dir(tagClassification['a1'][0]) if not feat.startswith('__') and not callable(getattr(tagClassification['a1'][0],feat))]
	featList=vars(tagClassification['a1'][0])
	del featList['tE']
	del featList['tag']
	del featList['bBox']
	del featList['center']
	feats2Rec=copy.deepcopy(featList)
	del feats2Rec['Coord']
	del feats2Rec['Style']
	del feats2Rec['coG']
	l1=[symbol for symbol in tagClassification if symbol[-1]=='1']
	l2=[symbol for symbol in tagClassification if symbol[-1]=='2']
	l3=[symbol for symbol in tagClassification if symbol[-1]=='3']
	standevs={}
	for fe in feats2Rec:
		for llet in tagClassification:
			for i in range(len(tagClassification[llet])):
				new=True
				for j in range(len(vars(tagClassification[llet][i])[fe])):
					if math.isnan(vars(tagClassification[llet][i])[fe][j]) and new:
						tagClassification[llet][i].computeFeatures()
						new=False
	for symbol in tagClassification:
		for i in range(len(tagClassification[symbol])):
			if tagClassification[symbol][i].Style=='diagonal':
				tagClassification[symbol][i].Style=[[1,1]]
			elif tagClassification[symbol][i].Style=='horizontal':
				tagClassification[symbol][i].Style=[[1,2]]
			elif tagClassification[symbol][i].Style=='vertical':
				tagClassification[symbol][i].Style=[[2,1]]
			elif tagClassification[symbol][i].Style=='closed':
				tagClassification[symbol][i].Style=[[2,2]]
	for feature in featList:
		print feature
		if feature=='Coord' or feature=='Style' or feature=='coG':
			standevs[feature]=[math.sqrt((((float(float(np.nansum([statistics.pstdev([vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]])/np.mean([vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]]) for i in range(len(vars(tagClassification[symbol][0])[feature]))]))/len(vars(tagClassification[symbol][0])[feature])))/(float((np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][j][0] for mostra in tagClassification[altSymbol]] for altSymbol in l1]))/np.mean(reduce(operator.add,[[vars(mostra)[feature][j][0] for mostra in tagClassification[altSymbol]] for altSymbol in l1])) for j in range(len(vars(tagClassification['a1'][0])[feature]))])/len(vars(tagClassification[symbol][0])[feature]))+(np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][j][0] for mostra in tagClassification[altSymbol]] for altSymbol in l2]))/np.mean(reduce(operator.add,[[vars(mostra)[feature][j][0] for mostra in tagClassification[altSymbol]] for altSymbol in l2])) for j in range(len(vars(tagClassification['+2'][0])[feature]))])/len(vars(tagClassification[symbol][0])[feature]))+(np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][j][0] for mostra in tagClassification[altSymbol]] for altSymbol in l3]))/np.mean(reduce(operator.add,[[vars(mostra)[feature][j][0] for mostra in tagClassification[altSymbol]] for altSymbol in l3])) for j in range(len(vars(tagClassification['A3'][0])[feature]))])/len(vars(tagClassification[symbol][0])[feature])))/3))**2)+(((float(float(np.nansum([statistics.pstdev([vars(mostra)[feature][i][1] for mostra in tagClassification[symbol]])/np.mean([vars(mostra)[feature][i][1] for mostra in tagClassification[symbol]]) for i in range(len(vars(tagClassification[symbol][0])[feature]))]))/len(vars(tagClassification[symbol][0])[feature])))/(float((np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][j][1] for mostra in tagClassification[altSymbol]] for altSymbol in l1]))/np.mean(reduce(operator.add,[[vars(mostra)[feature][j][1] for mostra in tagClassification[altSymbol]] for altSymbol in l1])) for j in range(len(vars(tagClassification['a1'][0])[feature]))])/len(vars(tagClassification[symbol][0])[feature]))+(np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][j][1] for mostra in tagClassification[altSymbol]] for altSymbol in l2]))/np.mean(reduce(operator.add,[[vars(mostra)[feature][j][1] for mostra in tagClassification[altSymbol]] for altSymbol in l2])) for j in range(len(vars(tagClassification['+2'][0])[feature]))])/len(vars(tagClassification[symbol][0])[feature]))+(np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][j][1] for mostra in tagClassification[altSymbol]] for altSymbol in l3]))/np.mean(reduce(operator.add,[[vars(mostra)[feature][j][1] for mostra in tagClassification[altSymbol]] for altSymbol in l3])) for j in range(len(vars(tagClassification['A3'][0])[feature]))])/len(vars(tagClassification[symbol][0])[feature])))/3))**2)) for symbol in tagClassification]
		else:
			standevs[feature]=[((float(float(np.nansum([statistics.pstdev([vars(mostra)[feature][i] for mostra in tagClassification[symbol]])/np.mean([vars(mostra)[feature][i] for mostra in tagClassification[symbol]]) for i in range(len(vars(tagClassification[symbol][0])[feature]))]))/len(vars(tagClassification[symbol][0])[feature])))/(float((np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][j] for mostra in tagClassification[altSymbol]] for altSymbol in l1]))/np.mean(reduce(operator.add,[[vars(mostra)[feature][j] for mostra in tagClassification[altSymbol]] for altSymbol in l1])) for j in range(len(vars(tagClassification['a1'][0])[feature]))])/len(vars(tagClassification[symbol][0])[feature]))+(np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][j] for mostra in tagClassification[altSymbol]] for altSymbol in l2]))/np.mean(reduce(operator.add,[[vars(mostra)[feature][j] for mostra in tagClassification[altSymbol]] for altSymbol in l2])) for j in range(len(vars(tagClassification['+2'][0])[feature]))])/len(vars(tagClassification[symbol][0])[feature]))+(np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][j] for mostra in tagClassification[altSymbol]] for altSymbol in l3]))/np.mean(reduce(operator.add,[[vars(mostra)[feature][j] for mostra in tagClassification[altSymbol]] for altSymbol in l3])) for j in range(len(vars(tagClassification['A3'][0])[feature]))])/len(vars(tagClassification[symbol][0])[feature])))/3))	for symbol in tagClassification]
	print standevs
	if os.path.isfile('varStandarDevs.txt'):
		os.remove('varStandarDevs.txt')
	f = open('varStandarDevs.txt','wb')
	pickle.dump(standevs,f)
	f.close()
	
def ponderateByConcentration():
	sdFile = open('varStandarDevs.txt','rb')
	standevs=pickle.load(sdFile)
	sdFile.close()
	totDevs={}
	for feature in standevs:
		totDevs[feature]=sum(standevs[feature])/len(standevs[feature])
	print totDevs
	localF=['turningAngle','turningAngleDifference','Coord','LP']
	globalF=['accAngle','coG','relStrokeLength','liS','quadraticError']
	weights={}
	norm=sum([(totDevs[feature]+max([totDevs[fe] for fe in localF])-(2*min([totDevs[fe] for fe in localF])))**(-1) for feature in localF])
	for feature in localF:
		weights[feature]=0.5*((totDevs[feature]+max([totDevs[fe] for fe in localF])-(2*min([totDevs[fe] for fe in localF])))**(-1))/norm
	norm=sum([(totDevs[feature]+max([totDevs[fe] for fe in globalF])-(2*min([totDevs[fe] for fe in globalF])))**(-1) for feature in globalF])
	for feature in globalF:
		weights[feature]=0.4*((totDevs[feature]+max([totDevs[fe] for fe in globalF])-(2*min([totDevs[fe] for fe in globalF])))**(-1))/norm
	weights['Style']=0.1
	print weights
	return weights
	
		
	
