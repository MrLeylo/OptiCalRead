import takeDS as tds
from pprint import pprint
import matplotlib.pyplot as plt
import symbolPreprocessing as spp

sdB=tds.mountDS('elsbthey2.dat')
bo=9
pprint(vars(sdB[bo]))
plt.figure(1)
for i in range(sdB[bo].tE.shape[0]):
	if i==0:
		pe=-1
	else:
		pe=int(sdB[bo].tE[i-1])
	plt.plot(sdB[bo].Coord[range(pe+1,int(sdB[bo].tE[i])+1),0],sdB[bo].Coord[range(pe+1,int(sdB[bo].tE[i])+1),1],'-')
for i in range(len(sdB)):
	sdB[i].draw()
dataBase=spp.preprocessing(sdB)



	
	
pprint(vars(sdB[bo]))
plt.figure(2)
for i in range(dataBase[bo].tE.shape[0]):
	if i==0:
		pe=-1
	else:
		pe=int(dataBase[bo].tE[i-1])
	plt.plot(dataBase[bo].Coord[range(pe+1,int(dataBase[bo].tE[i])+1),0],dataBase[bo].Coord[range(pe+1,int(dataBase[bo].tE[i])+1),1],'-')
plt.show()
