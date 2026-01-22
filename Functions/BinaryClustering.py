import numpy as np
from EvaluateSimilarities import *
from UpdateCosineMat import *
def BinaryClustering(ClusterRow,CosineMat,MaxSimAdjacencyList):
    CosineVec = CosineMat[ClusterRow,:]
    maxSim = np.max(CosineVec)
    maxSimLoc = np.where(CosineVec == maxSim)[0][0]
    ZeroRow = int(maxSimLoc[0])
    merge,CosineMat,MaxSimAdjacencyList = EvaluateSimilarities(CosineMat = CosineMat,
                                                               MaxSimAdjacencyList = MaxSimAdjacencyList,
                                                               ClusterRow = ClusterRow,
                                                               ZeroRow = ZeroRow)
    if not merge:
        return [CosineMat,MaxSimAdjacencyList]
    CosineMat = UpdateCosineMat(CosineMat = CosineMat,
                                ZeroRow = ZeroRow,
                                ClusterRow = ClusterRow,
                                MaxSimAdjacencyList = MaxSimAdjacencyList)    
   #MaxSimAdjacencyList = FillMaxSimAdjacencyList(MaxSimAdjacencyList = MaxSimAdjacencyList,
   #                                              ZeroRow = ZeroRow,
   #                                              ClusterRow = ClusterRow,
   #                                              CosineMat = CosineMat)    
    return [CosineMat,MaxSimAdjacencyList]
