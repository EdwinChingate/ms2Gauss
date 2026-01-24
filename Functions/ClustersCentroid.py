def ClustersCentroid(CosineMat,
                     Cluster):
    N_membersCluster = len(Cluster[0])        
    Centroid = sum(CosineMat[Cluster[0],:])/N_membersCluster
    Centroid[Cluster[0]] = 0
    return Centroid
