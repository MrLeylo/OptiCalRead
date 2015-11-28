import os

for cases in os.listdir('segmentedData'):
	if ',e' in open('segmentedData/'+cases+'/trainFile_GT.txt','r').read() :
		filesHere=sorted(os.listdir('segmentedData/'+cases))
		Gfile=open('segmentedData/'+cases+'/trainFile_GT.txt')
		linea='o'
		filco=0
		while linea!='':
			linea=Gfile.readline()
			if ',e' in linea:
				if open('segmentedData/'+cases+'/'+filesHere[filco],'r').read().count('<trace ')==2 or open('segmentedData/'+cases+'/'+filesHere[filco],'r').read().count('<trace>')==2:
					print cases,',',filesHere[filco]
			filco+=1
		Gfile.close()
