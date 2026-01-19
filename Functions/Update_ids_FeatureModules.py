import numpy as np
from IntramoduleAverageCosineSimmilarity import *
def Update_ids_FeatureModules(Feature_module,
                              Feature_Modules,
                              CosineMat):    
    npFeature_module = np.array(Feature_module, dtype = 'int')
    Modules=[]
    for module in Feature_Modules:
        feature_module = list(npFeature_module[module])
        moduleCosineMat = CosineMat[np.ix_(module,module)]
        meanCosSim_off_diag = IntramoduleAverageCosineSimmilarity(moduleCosineMat)
        Modules.append([feature_module,meanCosSim_off_diag])
    return Modules
