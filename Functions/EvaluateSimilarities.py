import numpy as np
def EvaluateSimilarities(CosineMat,
                         Cluster,
                         ClusterRow,
                         ZeroRow,
                         CosTolDif = 0.15):    
    ClusterMembers = Cluster[0] 
    ClusterCoherence = Cluster[1]
    ClusterExternalAffinity = Cluster[2]
    NewMemberCosineVec = CosineMat[ZeroRow,:]    
    NodesSet = set(np.arange(len(NewMemberCosineVec),dtype='int').tolist())
    NewClusterCoherence = float(min(NewMemberCosineVec[ClusterMembers].tolist()))
    print(NewClusterCoherence)
    NewClusterCoherence = min([NewClusterCoherence,ClusterCoherence])
    print(NewClusterCoherence)
    NoNeighborsSet = NodesSet - set(ClusterMembers)
    ClusterExternalAffinity = np.max(CosineMat[np.ix_(ClusterMembers,list(NoNeighborsSet))])
    NewClusterExternalAffinity = float(max(NewMemberCosineVec[list(NoNeighborsSet)]))
    print(NewClusterExternalAffinity)
    NewClusterExternalAffinity = max([NewClusterExternalAffinity,ClusterExternalAffinity])
    print(NewClusterExternalAffinity)
    print(np.where(NewMemberCosineVec==float(max(NewMemberCosineVec[list(NoNeighborsSet)]))))
    Contrast = NewClusterCoherence-NewClusterExternalAffinity+CosTolDif
    print(Contrast,NewClusterCoherence,NewClusterExternalAffinity)
    merge = Contrast>=0
    if merge:
        Cluster[0] = ClusterMembers + [ZeroRow]
        Cluster[1] = NewClusterCoherence
        Cluster[2] = NewClusterExternalAffinity
    else:
        CosineMat[ClusterRow,ZeroRow] = 0
        CosineMat[ZeroRow,ClusterRow] = 0
    return [merge,CosineMat,Cluster]
    
