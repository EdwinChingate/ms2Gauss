def UpdateCosineMat(CosineMat,
                    ZeroRow,
                    ClusterRow,
                    Cluster):
    N_membersCluster = len(Cluster[0])    
    ZeroVec = CosineMat[ZeroRow,:]
    ClusterVec = CosineMat[ClusterRow,:]
    Centroid = (ZeroVec+N_membersCluster*ClusterVec)/(N_membersCluster+1)
    sum(CosineMat[Cluster[0],:])/N_membersCluster
    Centroid[Cluster[0]] = 0
    CosineMat[ClusterRow,:] = Centroid
    CosineMat[:,ClusterRow] = Centroid
    return CosineMat
