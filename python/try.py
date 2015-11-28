import symbolPreprocessing as spp
import numpy as np
import Symbol


H=np.array([[[0,1],[0,3],[1,4],[3,5],[4,4],[5,3],[7,3],[8,0]],[[0,1],[0,3],[1,4],[3,5],[4,4],[5,3],[7,3],[7,3]]],np.float64)
H=spp.pointClustering(H)
print H
H=spp.smoothing(H)
print H
H=spp.dehooking(H)
print H
H=spp.polyAproximation(H)
print H
H=spp.arcLengthResampling(H,3)
print H
print 'o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o_o'
G=np.array([[[1,0],[0,1],[0,2],[0,3],[1,4],[2,3],[2,2],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1]],[[1,0],[1,1],[1,2],[2,3],[2,4],[2,5],[2,5],[2,5],[0,4],[3,4],[3,3],[3,3],[3,3],[3,3],[3,3],[3,3]]],np.float64)
Gb=np.array([[0,2,0,4],[0,3,0,5]],np.float64)
Gc=np.array([[1,2],[1.5,2.5]],np.float64)
print G
G,tipus=spp.strokeDirOrder(G,Gb)
print G
print spp.sizeNorm(G,Gb,Gc)
