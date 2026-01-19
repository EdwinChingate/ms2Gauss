import numpy as np
from FlatMatrix_woDiag import *
def IntramoduleAverageCosineSimmilarity(moduleCosineMat):
    n = moduleCosineMat.shape[0]
    if n == 1:
        return [1,0]
    CosineArray = FlatMatrix_woDiag(matrix = moduleCosineMat,
                                    n = n)
    meanCosSim_off_diag = np.mean(CosineArray)
    stdCosSim_off_diag = np.std(CosineArray)
    return [meanCosSim_off_diag,stdCosSim_off_diag]
