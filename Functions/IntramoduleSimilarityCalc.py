import numpy as np
from IntramoduleCosineStats import *
def IntramoduleSimilarityCalc(Modules,
                              CosineMat,
                              percentile = 10):
    N_modules = len(Modules)
    IntramoduleSimilarity = np.zeros((N_modules,5))
    for module_id in np.arange(N_modules):    
        module = Modules[module_id]
        moduleCosineMat = CosineMat[np.ix_(module,module)]
        IntramoduleSimilarity[module_id,:-1] = IntramoduleCosineStats(moduleCosineMat = moduleCosineMat,
                                                                      percentile = percentile)
        IntramoduleSimilarity[module_id,-1] = module_id
    return IntramoduleSimilarity
