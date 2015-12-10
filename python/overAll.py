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

#Sistema sencer, llegeix nom del fitxer inkml a analitzar i retorna l'expressio (ex: overAll.py fitxerAClassificar.inkml)

filenom=sys.argv[1]		#Llegir el nom del fitxer InkML de la consola
Coord=ink2Traces.i2t(filenom)		#Extreure les coordenades donades pel fitxer
img,byAxis,difs=drawTraces.draw(Coord)		#Mostrar resultat obtingut i montar imatge
Symb,groupedStrokes=fileSeg.segment(Coord,byAxis,difs)		#Agrupar traces en simbols
Symb=drawRegions.drawS(Symb)		#Buscar la bounding box i el centre de cada simbol
Symb=spp.preprocessing(Symb)		#Preprocessar tots els simbols
#repS.repr([symbols[3]])
for i in range(len(Symb)):
	Symb[i].computeFeatures()		#Calcular les features de cada simbol
symboldB,tagClassification,averages=temp.readTemplate()		#Llegeix la base de dades per extreure tots els simbols etiquetats, totes les mostres ordenades per caracter(etiqueta) i el template de cada caracter
genTags={}		#Busca el significat independent de cada caracter i si la proporcio del caracter respecte el significat independent es molt baixa ho considera soroll i elimina el caracter
for character in tagClassification:
	if character[:-1] not in genTags:
		genTags[character[:-1]]=[]
	genTags[character[:-1]].append([character,len(tagClassification[character])])
for onlySym in genTags:
	for i in range(len(genTags[onlySym])):
		if genTags[onlySym][i][1]<0.05*sum([genTags[onlySym][caseID][1] for caseID in range(len(genTags[onlySym]))]):
			del tagClassification[genTags[onlySym][i][0]]
			del averages[genTags[onlySym][i][0]]
weights=fp.ponderateByConcentration()		#Aplica una ponderacio per concentracio a les features
for i in range(len(Symb)):		#Per cada simbol a analitzar li assigna un caracter
	decision=eM.elasticMatching(averages,Symb[i],weights)
	print decision
plt.show()
