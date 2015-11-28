#!/usr/bin/env python

import sys
import ink2Traces
import drawTraces
import fileSeg
import drawRegions
import matplotlib.pyplot as plt
import numpy as np
import symbolPreprocessing as spp
import repS
import SClass
from pprint import pprint
import elasticMatching as eM
import pytemplate as temp
import featurePonderation as fp



filenom=sys.argv[1]		#Llegir el nom del fitxer InkML de la consola
Coord=ink2Traces.i2t(filenom)		#Extreure les coordenades donades pel fitxer
img,byAxis,difs=drawTraces.draw(Coord)		#Mostrar resultat obtingut i montar imatge
Symb,groupedStrokes=fileSeg.segment(Coord,byAxis,difs)		#Agrupar traces en simbols
Symb=drawRegions.drawS(Symb)
#bBoxes,centers=drawRegions.draw(Symb)		#Busca la bounding box i el centre de cada simbol
symbols=spp.preprocessing(Symb)#,bBoxes,centers)
#repS.repr([symbols[3]])
for i in range(len(symbols)):
	symbols[i].computeFeatures()
	#pprint(vars(symbols[i]))
symboldB,tagClassification,averages=temp.readTemplate()
genTags={}
for character in tagClassification:
	if character[:-1] not in genTags:
		genTags[character[:-1]]=[]
	genTags[character[:-1]].append([character,len(tagClassification[character])])
for onlySym in genTags:
	for i in range(len(genTags[onlySym])):
		if genTags[onlySym][i][1]<0.05*sum([genTags[onlySym][caseID][1] for caseID in range(len(genTags[onlySym]))]):
			del tagClassification[genTags[onlySym][i][0]]
			del averages[genTags[onlySym][i][0]]
#[averages[car].computeFeatures() for car in averages]
weights=fp.ponderateByConcentration()
for i in range(len(symbols)):
	decision=eM.elasticMatching(averages,symbols[i],weights)
	print decision
plt.figure(5)
for j in range(len(tagClassification[decision][0].tE)):
	if j==0:
		ini=-1
	else:
		ini=int(tagClassification[decision][0].tE[j-1])
	plt.plot(averages[decision].Coord[range(ini+1,int(tagClassification[decision][0].tE[j])+1),0],-averages[decision].Coord[range(ini+1,int(tagClassification[decision][0].tE[j])+1),1],'r')
plt.show()
