import numpy as np
from EvaluateSimilarities import *
from UpdateCosineMat import *
def BinaryClustering(ClusterRow,
                     CosineMat,
                     Cluster,
                     Centroid,
                     iterations_since_addition,
                     CosTolDif = 0.15):
    maxSim = np.max(Centroid)
    maxSimLoc = np.where(Centroid == maxSim)[0][0]
    ZeroRow = int(maxSimLoc)
    merge,Cluster,Centroid = EvaluateSimilarities(CosineMat = CosineMat,
                                                  Cluster = Cluster,
                                                  Centroid = Centroid,
                                                  ZeroRow = ZeroRow,
                                                  CosTolDif = CosTolDif)
    if not merge:
        iterations_since_addition += 1
        return [CosineMat, Cluster, Centroid, iterations_since_addition]
    Centroid = ClustersCentroid(CosineMat = CosineMat,
                                Cluster = Cluster)  
    return [CosineMat, Cluster, Centroid, aiterations_since_addition]
