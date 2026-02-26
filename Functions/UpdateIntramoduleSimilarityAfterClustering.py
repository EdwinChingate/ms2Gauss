import numpy as np
def UpdateIntramoduleSimilarityAfterClustering(Modules,
                                               IntramoduleSimilarityList):
    IntramoduleSimilarityModulesList = []
    for module in Modules:
        FirstClust = True
        for module_id in module:
            IntramoduleSimilarityVec = IntramoduleSimilarityList[module_id].copy().reshape(-1, 1)
            if FirstClust:
                IntramoduleSimilarityVecMat = IntramoduleSimilarityVec
                FirstClust = False
            else:
                IntramoduleSimilarityVecMat = np.hstack((IntramoduleSimilarityVecMat,
                                                         IntramoduleSimilarityVec))
        MeanIntramoduleSimilarityVec = np.mean(IntramoduleSimilarityVecMat.T,
                                               axis = 0)
        IntramoduleSimilarityModulesList.append(MeanIntramoduleSimilarityVec)
    IntramoduleSimilarityModulesMat = np.array(IntramoduleSimilarityModulesList)
    return IntramoduleSimilarityModulesMat
