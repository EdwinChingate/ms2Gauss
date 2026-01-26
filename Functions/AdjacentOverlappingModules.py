import numpy as np
def AdjacentOverlappingModules(Modules,
                               IntramoduleSimilarity,
                               CompactCosineTen):
    N_modules = len(Modules)
    AdjacencyList = []
    module_ids = []
    for module_id in np.arange(N_modules):    
        module = Modules[module_id]
        LowIntramoduleSimmilarity = IntramoduleSimilarity[module_id,1]
        maxSimNeighborsVec = CompactCosineTen[module_id,:,2]
        Neigbours = np.where(maxSimNeighborsVec > LowIntramoduleSimmilarity)[0].tolist() + [int(module_id)]
        module_ids.append(int(module_id))
        AdjacencyList.append(Neigbours)
    module_ids = set(module_ids)        
    return [AdjacencyList,module_ids]
