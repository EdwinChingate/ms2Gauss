import numpy as np
def EvaluateSimilarities(CosineMat,
                         Cluster,
                         ZeroRow,
                         Centroid,
                         CosTolDif = 0.15):    
    ClusterMembers = Cluster[0] 
    ClusterCoherence = Cluster[1]
    ClusterExternalAffinity = Cluster[2]
    NewMemberCosineVec = CosineMat[ZeroRow,:]    
    NodesSet = set(np.arange(len(NewMemberCosineVec),dtype='int').tolist())
    NewClusterCoherence = float(min(NewMemberCosineVec[ClusterMembers].tolist()))
    NewClusterCoherence = min([NewClusterCoherence,ClusterCoherence])
    NoNeighborsSet = NodesSet - set(ClusterMembers)
    ClusterExternalAffinity = np.max(CosineMat[np.ix_(ClusterMembers,list(NoNeighborsSet))])
    r,c = np.where(CosineMat[np.ix_(ClusterMembers,list(NoNeighborsSet))] == ClusterExternalAffinity)
    print(ClusterMembers[r[0]],list(NoNeighborsSet)[c[0]])
    NewClusterExternalAffinity = float(max(NewMemberCosineVec[list(NoNeighborsSet)]))
    NewClusterExternalAffinity = max([NewClusterExternalAffinity,ClusterExternalAffinity])
    Contrast = NewClusterCoherence-NewClusterExternalAffinity+CosTolDif
    merge = Contrast>=0
    if merge:
        Cluster[0] = ClusterMembers + [ZeroRow]
        Cluster[1] = NewClusterCoherence
        Cluster[2] = NewClusterExternalAffinity
    else:
        Centroid[ZeroRow] = 0
    return [merge,Cluster,Centroid]
    
