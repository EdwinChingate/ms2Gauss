import numpy as np
def CommunityBlocks(AdjacencyList_Features):
    NeighborhoodSizeVec = np.array([len(x) for x in AdjacencyList_Features])
    Modules = []
    AssignedNodes = []
    for node_id in NeighborhoodSizeVec.argsort():
        AdjacencyList = AdjacencyList_Features[node_id]
        Module = list(set(AdjacencyList) - set(AssignedNodes))
        if len(Module) > 0:
            Modules.append(Module)
        AssignedNodes += Module    
    return Modules
