import numpy as np
from FlatMatrix_woDiag import *
def IntramoduleCosineStats(moduleCosineMat,
                           percentile = 10):
    n = moduleCosineMat.shape[0]
    if n == 1:
        return [1,1,1,1]
    CosineArray = FlatMatrix_woDiag(matrix = moduleCosineMat,
                                    n = n)
    medianCosSim_off_diag = np.median(CosineArray)
    if len(CosineArray) > 1:        
        low_percentile_CosSim_off_diag = np.percentile(CosineArray,percentile)
        high_percentile_CosSim_off_diag = np.percentile(CosineArray,100-percentile)
    else:
        low_percentile_CosSim_off_diag = medianCosSim_off_diag
        high_percentile_CosSim_off_diag = medianCosSim_off_diag
    return [n,low_percentile_CosSim_off_diag,medianCosSim_off_diag,high_percentile_CosSim_off_diag]
