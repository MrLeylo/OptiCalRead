import numpy as np

def c2s(Coord,gS):
	symbols=np.zeros([len(gS),(Coord.shape[1])*max(gS),2], np.float64)
	counter=0
	for i in range(len(gS)):
		for r in range(gS[i]):
			symbols[i]=Coord[counter]
			counter=counter+1
	return symbols
