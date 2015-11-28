import math
import numpy as np
import symbolPreprocessing as spp
import featurePonderation as fP


def elasticMatching(charTemplates,symbolToRec,weights):
	costCoord=[]
	costLP=[]
	costtAngle=[]
	costtAD=[]
	costliS=[]
	costaA=[]
	costqE=[]
	costrSL=[]
	costcog=[]
	coststyle=[]
	reference=[]
	cost=[]
	for character in charTemplates:
		costCoord.append(sum([math.sqrt(((charTemplates[character].Coord[i,0]-symbolToRec.Coord[i,0])**2)+((charTemplates[character].Coord[i,1]-symbolToRec.Coord[i,1])**2)) for i in range(symbolToRec.Coord.shape[0])]))
		costLP.append(sum([abs(charTemplates[character].LP[i]-symbolToRec.LP[i]) for i in range(symbolToRec.LP.shape[0])]))
		costtAngle.append(sum([abs(charTemplates[character].turningAngle[i]-symbolToRec.turningAngle[i]) for i in range(symbolToRec.turningAngle.shape[0])]))
		costtAD.append(sum([abs(charTemplates[character].turningAngleDifference[i]-symbolToRec.turningAngleDifference[i]) for i in range(symbolToRec.turningAngleDifference.shape[0])]))
		if symbolToRec.liS.shape[0]!=len(charTemplates[character].liS):
			costliS.append(spp.lcomp(symbolToRec.Coord,symbolToRec.Coord.shape[0]))
		else:
			costliS.append(sum([abs(charTemplates[character].liS[i]-symbolToRec.liS[i]) for i in range(symbolToRec.liS.shape[0])]))
		if symbolToRec.accAngle.shape[0]!=len(charTemplates[character].accAngle):
			costaA.append(symbolToRec.tE.shape[0]*2*math.pi)
		else:	
			costaA.append(sum([abs(charTemplates[character].accAngle[i]-symbolToRec.accAngle[i]) for i in range(symbolToRec.accAngle.shape[0])]))
		if symbolToRec.quadraticError.shape[0]!=len(charTemplates[character].quadraticError):
			costqE.append(math.sqrt(8)*symbolToRec.tE.shape[0])
		else:
			costqE.append(sum([abs(charTemplates[character].quadraticError[i]-symbolToRec.quadraticError[i]) for i in range(symbolToRec.quadraticError.shape[0])]))
		if symbolToRec.relStrokeLength.shape[0]!=len(charTemplates[character].relStrokeLength):
			costrSL.append(1)
		else:
			costrSL.append(sum([abs(charTemplates[character].relStrokeLength[i]-symbolToRec.relStrokeLength[i]) for i in range(symbolToRec.relStrokeLength.shape[0])]))	
		if symbolToRec.coG.shape[0]!=len(charTemplates[character].coG):
			costcog.append(symbolToRec.tE.shape[0]*math.sqrt(8))
		else:
			costcog.append(sum([math.sqrt(((charTemplates[character].coG[i][0]-symbolToRec.coG[i][0])**2)+((charTemplates[character].coG[i][1]-symbolToRec.coG[i][1])**2)) for i in range(symbolToRec.coG.shape[0])]))
		if charTemplates[character].Style==symbolToRec.Style:
			coststyle.append(0)
		else:
			coststyle.append(1)
		reference.append(character)
		cost.append(0)
	#print [((0.5*(costCoord[i]/50))+(0.05*(costLP[i]/max(costLP)))+(0.05*(costtAngle[i]/max(costtAngle)))+(0.05*costtAD[i]/(50*2*math.pi))+(0.05*costliS[i]/max(costliS))+(0.05*costaA[i]/(symbolToRec.tE.shape[0]*2*math.pi))+(0.025*costqE[i]/max(costqE))+(0.025*costrSL[i]/max(costrSL))+(0.1*costcog[i]/symbolToRec.tE.shape[0])+(0.1*coststyle[i]))*100 for i in range(len(cost))]
	#print [math.sqrt(len(tagClassification[reference[i]])) for i in range(len(cost))]
	
	
	#cost=[((0.5*(costCoord[i]/50))+(0.05*(costLP[i]/max(costLP)))+(0.05*(costtAngle[i]/max(costtAngle)))+(0.05*costtAD[i]/(50*2*math.pi))+(0.05*costliS[i]/max(costliS))+(0.05*costaA[i]/(symbolToRec.tE.shape[0]*2*math.pi))+(0.025*costqE[i]/max(costqE))+(0.025*costrSL[i]/max(costrSL))+(0.1*costcog[i]/symbolToRec.tE.shape[0])+(0.1*coststyle[i])) for i in range(len(cost))]
	cost=[((weights['Coord']*(costCoord[i]/50))+(weights['LP']*(costLP[i]/max(costLP)))+(weights['turningAngle']*(costtAngle[i]/max(costtAngle)))+(weights['turningAngleDifference']*costtAD[i]/(50*2*math.pi))+(weights['liS']*costliS[i]/max(costliS))+(weights['accumulatedAngle']*costaA[i]/(symbolToRec.tE.shape[0]*2*math.pi))+(weights['quadraticError']*costqE[i]/max(costqE))+(weights['relStrokeLength']*costrSL[i]/max(costrSL))+(weights['coG']*costcog[i]/symbolToRec.tE.shape[0])+(weights['Style']*coststyle[i])) for i in range(len(cost))]
	
	
	
	#print '----------------------------------------'
	#print cost
	#print '(',reference.index('x1'),')'
	#cost=[costCoord[i]/50 for i in range(len(cost))]
	while charTemplates[reference[np.argmin(cost)]].tE.shape[0]!=symbolToRec.tE.shape[0]:
		del reference[np.argmin(cost)]
		del cost[np.argmin(cost)]
	etiqBelongs=reference[np.argmin(cost)]
	return etiqBelongs
