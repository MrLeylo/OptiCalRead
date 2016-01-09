def findConcentrationSecond(tagClassification):
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
		fdata=open(getFileName(feature)[0],'w')
		if type(getFileName(feature)[1]) is str:
			fvars=open(getFileName(feature)[1],'w')
		elif type(getFileName(feature)[1]) is list:
			fvars=[]
			for nam in getFileName(feature)[1]:
				fvars.append(open(nam,'w'))
		print feature
		if feature=='Style':
			standevs[feature]=[]
			outStdVar=math.sqrt(((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][0][0] for mostra in tagClassification[symbol]] for symbol in tagClassification])))**2)+((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][0][1] for mostra in tagClassification[symbol]] for symbol in tagClassification])))**2))
			for symbol in tagClassification:
				fdata.write(symbol+':\n')
				for m in tagClassification[symbol]:
					fdata.write(str(vars(m)[feature][0][0])+','+str(vars(m)[feature][0][1])+'\n'
				fdata.write('------------------------------------------------------------------------------\n')
				inStdVar=math.sqrt(((statistics.pstdev([vars(mostra)[feature][0][0] for mostra in tagClassification[symbol]]))**2)+((statistics.pstdev([vars(mostra)[feature][0][1] for mostra in tagClassification[symbol]]))**2))
				fvars.write(symbol+':'+str(inStdVar)+'\n')
				standevs[feature].append(inStdVar/float(outStdVar))
			fvars.write('OUT:'+str(outStdVar)+'\n')
			fdata.close()
			fvars.close()
		if feature=='turningAngle' or feature=='turningAngleDifference' or feature=='LP':
			L=50
			standevs[feature]=[]
			outStdVar=[]
			for i in range(L):
				outStdVar.append(statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i] for mostra in tagClassification[symbol]] for symbol in tagClassification])))
			textLocal=[]
			notYet=True
			for symbol in tagClassification:
				fdata.write(symbol+':\n')
				for m in tagClassification[symbol]:
					for i in range(50):
						fdata.write(str(vars(m)[feature][i])+',')
					fdata.write('\n')
				fdata.write('------------------------------------------------------------------------------\n')
				localStdv=[]
				for i in range(L):
					if notYet:
						textLocal.append('')
					inStdVar=statistics.pstdev([vars(mostra)[feature][i] for mostra in tagClassification[symbol]])
					localStdv.append(inStdVar/float(outStdVar[i]))
					textLocal[i]+='('+str(i)+')'+symbol+':'+str(localStdv)+'\n'
				standevs[feature].append(np.nansum(localStdv)/float(L))
				notYet=False
			for i in range(L):
				fvars.write(textLocal[i])
				fvars.write('OUT:'+str(outStdVar[i]))
			fdata.close()
			fvars.close()
		if feature=='Coord':
			L=50
			standevs[feature]=[]
			outStdVar=[]
			for i in range(L):
				outStdVar.append(math.sqrt(((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]] for symbol in tagClassification])))**2)+((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][1] for mostra in tagClassification[symbol]] for symbol in tagClassification])))**2))))
			for symbol in tagClassification:
				fdata.write(symbol+':\n')
				for m in tagClassification[symbol]:
					for i in range(50):
						fdata.write('['+str(vars(m)[feature][i][0])+','+str(vars(m)[feature][i][1])+'],')
					fdata.write('\n')
				fdata.write('------------------------------------------------------------------------------\n')
				localStdv=[]
				for i in range(L):
					if notYet:
						textLocal.append('')
					inStdVar=math.sqrt(((statistics.pstdev([vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]]))**2)+((statistics.pstdev([vars(mostra)[feature][1] for mostra in tagClassification[symbol]]))**2))
					localStdv.append(inStdVar/float(outStdVar[i]))
					textLocal[i]+='('+str(i)+')'+symbol+':'+str(localStdv)+'\n'
				standevs[feature].append(np.nansum(localStdv)/L)
				notYet=False
			for i in range(L):
				fvars.write(textLocal[i])
				fvars.write('OUT:'+str(outStdVar[i]))
			fdata.close()
			fvars.close()
		if feature=='liS' or feature=='relStrokeLength' or feature=='accAngle' or feature=='quadraticError':
			standevs[feature]=[]
			oneOut=np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]] for symbol in l1])) for i in range(1)])/1.0
			twoOut=np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]] for symbol in l2])) for i in range(2)])/2.0
			threeOut=np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]] for symbol in l3])) for i in range(3)])/3.0
			outStdVar=((oneOut*len(l1))+(twoOut*len(l2))+(threeOut*len(l3)))/float(len(l1)+len(l2)+len(l3))
			text1=''
			text2=''
			text3=''
			for symbol in tagClassification:
				for m in tagClassification[symbol]:
					for i in range(symbol.tE.shape[0]):
						fdata.write(str(vars(m)[feature][i])+',')
					fdata.write('\n')
				fdata.write('------------------------------------------------------------------------------\n')
				inStdVar=np.nansum([statistics.pstdev([vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]]) for i in range(symbol.tE.shape[0])])/float(symbol.tE.shape[0])
				if symbol in l1:
					text1+=symbol+':'+str(inStdVar)+'\n'
				elif symbol in l2:
					text2+=symbol+':'+str(inStdVar)+'\n'
				elif symbol in l3:
					text3+=symbol+':'+str(inStdVar)+'\n'
				standevs[feature].append(inStdVar/float(outStdVar))
			fvars[0].write(text1)
			fvars[1].write(text2)
			fvars[2].write(text3)
			fdata.close()
			fvars.close()
		if feature=='coG':
			standevs[feature]=[]
			oneOut=np.nansum([math.sqrt(((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]] for symbol in l1])))**2)+((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i][1] for mostra in tagClassification[symbol]] for symbol in l1])))**2)) for i in range(1)])/1.0
			twoOut=np.nansum([math.sqrt(((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]] for symbol in l2])))**2)+((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i][1] for mostra in tagClassification[symbol]] for symbol in l2])))**2)) for i in range(2)])/2.0
			threeOut=np.nansum([math.sqrt(((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]] for symbol in l3])))**2)+((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i][1] for mostra in tagClassification[symbol]] for symbol in l3])))**2)) for i in range(3)])/3.0
			outStdVar=((oneOut*len(l1))+(twoOut*len(l2))+(threeOut*len(l3)))/float(len(l1)+len(l2)+len(l3))
			text1=''
			text2=''
			text3=''
			for symbol in tagClassification:
				for m in tagClassification[symbol]:
					for i in range(symbol.tE.shape[0]):
						fdata.write(str(vars(m)[feature][i][0])+','+str(vars(m)[feature][i][1]),']',',')
					fdata.write('\n')
				fdata.write('------------------------------------------------------------------------------\n')
				inStdVar=np.nansum([math.sqrt(((statistics.pstdev([vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]]))**2)+((statistics.pstdev([vars(mostra)[feature][i][1] for mostra in tagClassification[symbol]]))**2)) for i in range(symbol.tE.shape[0])])/float(symbol.tE.shape[0])
				if symbol in l1:
					text1+=symbol+':'+str(inStdVar)+'\n'
				elif symbol in l2:
					text2+=symbol+':'+str(inStdVar)+'\n'
				elif symbol in l3:
					text3+=symbol+':'+str(inStdVar)+'\n'
				standevs[feature].append(inStdVar/float(outStdVar))
			text1+='OUT:'+str(oneOut)+'\n'
			text2+='OUT:'+str(twoOut)+'\n'
			text3+='OUT:'+str(threeOut)+'\n'
			fvars[0].write(text1)
			fvars[1].write(text2)
			fvars[2].write(text3)
			fdata.close()
			fvars.close()
	print standevs
	if os.path.isfile('varStandarDevs.txt'):
		os.remove('varStandarDevs.txt')
	f = open('varStandarDevs.txt','wb')
	pickle.dump(standevs,f)
	f.close()
	
	def getFileName(feature):
		nomData='fAn_'+feature+'.txt'
		if os.path.isfile(nomData):
			os.remove(nomData)
		nomVars='vAn_'+feature+'.txt'
		if os.path.isfile(nomVars):
			os.remove(nomVars)
		if feature=='liS' or feature=='relStrokeLength' or feature=='accAngle' or feature=='quadraticError' or feature=='coG':
			 nomVars=['vAn_'+feature+'01.txt','vAn_'+feature+'02.txt','vAn_'+feature+'03.txt']
			 for n in nomVars:
				 if os.path.isfile(n):
					os.remove(n)
		else:
			nomVars='vAn_'+feature+'.txt'
			if os.path.isfile(nomVars):
				os.remove(nomVars)
		return [nomData,nomVars]
