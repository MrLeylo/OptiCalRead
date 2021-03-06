import numpy as np
import re


#search4Trace: indica si a la linea de text indicada hi ha un inici de trace o un final depenent del que es demani en whichTrace (='in' inici,='out' final)

def search4Trace(linea,whichTrace, condition):
	if whichTrace=='in':
		if condition=='single':
			if '<trace>' in linea or '<trace ' in linea:
				return True
			else:
				return False
		elif condition=='group':
			if '<traceGroup' in linea:
				return True
			else:
				return False
	elif whichTrace=='out':
		if condition=='single':
			if '</trace>' in linea or '</trace ' in linea:
				return True
			else:
				return False
		if condition=='group':
			if '</traceGroup' in linea:
				return True
			else:
				return False
	return

#Llegeix el fitxer d'entrenament indicat per filenom i torna les coordenades extretes (matriu de tres dimensions, equivalent a trace, punt, i eix de coordenades (x i y))
	
def i2t(filenom):
	linea="o"
	file=open(filenom,"r")
	print filenom
	coordinates=np.array([[[]]], np.float64)
	contador=0
	# Llegeix les linies del fitxer fins que acaben
	while linea!="":
		linea=file.readline()
		isTraceIn=search4Trace(linea,"in",'single')
		isTraceGroupIn=search4Trace(linea,"in",'group')
		# Si s'inicia una trace nova incrementa el comptador de traces i busca el final de la trace
		if isTraceIn:
			contador=contador+1
			isTraceOut=search4Trace(linea,"out")
			#Si a la mateixa linea s'acaba es guarda la linea fins on detecta el final
			if isTraceOut:
				lastV=linea.index('</trace>')
				newTraceW=linea[0:lastV+1]
			#Si no s'acaba a la mateixa linea va guardant les linies que troba dins de la mateixa trace
			else:
				lineaTrace=linea
				while lineaTrace!="":
					lineaTrace=lineaTrace+file.readline()
					isTraceOut=search4Trace(lineaTrace,"out")
					#Quan troba el final de la trace guarda el que ha acumulat de les diferents linies
					if isTraceOut:
						newTraceW=lineaTrace[0:len(lineaTrace)]
						lineaTrace=''
			#Neteja les linies per quedar-se nomes amb la part d'interes
			newTraceW.rstrip('\n')
			fiXML=newTraceW.index('>',0)
			fiTrace=newTraceW.index('<',3)
			onlyTrace=newTraceW[fiXML+1:fiTrace]
			#Separa les coordenades de la linea en una llista
			precoordinateLines=onlyTrace.split(' ')
			for lines in range(len(precoordinateLines)):
				word=precoordinateLines[lines].rstrip(',')
				precoordinateLines[lines]=word
			#Passa les coordenades de text a format numeric
			coordinatesAr=[]
			for i in range(len(precoordinateLines)):
				coordinatesAr.append(float(precoordinateLines[i]))
			#Ajusta la matriu de coordenades segons la longitud que va trobant en les traces (expandeix si la nova trace es mes llarga que les anteriors)
			if ((len(coordinatesAr)+1)/2)>coordinates.shape[1]:
				difer=((len(coordinatesAr)+1)/2)-coordinates.shape[1]
			else:
				difer=0
			if contador==1:
				expansio=0
			else:
				expansio=1
			coordinates=np.lib.pad(coordinates,((0,expansio),(0,difer),(0,2-coordinates.shape[2])),'constant')
			#Omple la matriu de coordenades
			c=0
			for i in range((len(coordinatesAr)+1)/2):
				for j in range(2):
					coordinates[coordinates.shape[0]-1,i,j]=coordinatesAr[c]
					c=c+1
		#Reparteix les coordenades en traces depenent del que digui l'arxiu
		ident=0
		elif isTraceGroupIn:
			if linea.count('<traceGroup')>1:
				ident+=linea.count('<traceGroup')-1
			isTraceGroupOut=search4Trace(linea,"out",'group')
			if isTraceGroupOut:
				if ident>0:
					ident-=linea.count('</traceGroup')
					if ident<0:
						lastV=linea.index('</traceGroup>')
						newTraceW=linea[0:lastV+1]
			else:
				lineaTrace=linea
				while lineaTrace!="":
					lineaTrace=lineaTrace+file.readline()
					isTraceGroupOut=search4Trace(linea,"out",'group')
					if isTraceGroupOut:
						if ident>0:
							ident-=linea.count('</traceGroup')
							if ident<0:
								newTraceW=lineaTrace[0:len(lineaTrace)]
								lineaTrace=''
						else:
							newTraceW=lineaTrace[0:len(lineaTrace)]
							lineaTrace=''
			newTraceW.rstrip('\n')
			fiXML=newTraceW.index('>',0)
			fiTrace=len(newTraceW)-newTraceW[::-1].index('<',0)-1
			onlyTrace=newTraceW[fiXML+1:fiTrace]
		if isMathMLin:
			if isMathMLout:
			else:
	file.close()
	return coordinates
