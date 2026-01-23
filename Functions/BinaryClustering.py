import numpy as np
#from EvaluateSimilarities import *
#from UpdateCosineMat import *
def BinaryClustering(ClusterRow,
                     CosineMat,
                     Cluster,
                     CosTolDif = 0.15):
    CosineVec = CosineMat[ClusterRow,:]
    maxSim = np.max(CosineVec)
    maxSimLoc = np.where(CosineVec == maxSim)[0][0]
    ZeroRow = int(maxSimLoc)
    print(ZeroRow)
    merge,CosineMat,Cluster = EvaluateSimilarities(CosineMat = CosineMat,
                                                   Cluster = Cluster,
                                                   ClusterRow = ClusterRow,
                                                   ZeroRow = ZeroRow,
                                                   CosTolDif = CosTolDif)
    print(merge)
    if not merge:
        return [CosineMat,Cluster]
    CosineMat = UpdateCosineMat(CosineMat = CosineMat,
                                ZeroRow = ZeroRow,
                                ClusterRow = ClusterRow,
                                Cluster = Cluster)      
    return [CosineMat,Cluster]
