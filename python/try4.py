import SClass as nsi
import symbolPreprocessing as spp
import numpy as np
from pprint import pprint

s=[nsi.Symbol(np.array([[1,0],[1,4],[1,8],[1,12],[2,0],[2,6],[2,12],[2,18],[2,24]],np.float64),np.array([3,8],np.float64))]
s2=[nsi.Symbol(np.array([[24,24],[1,0],[1,4],[1,8],[1,12],[2,0],[2,6],[2,12],[2,18],[2,24]],np.float64),np.array([0,4,9],np.float64))]
e=np.array([4,8],np.float64)
s[0].draw()
n=spp.polyAproximation(s)
pprint(vars(n[0]))
