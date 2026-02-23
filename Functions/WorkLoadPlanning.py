import numpy as np
def WorkLoadPlanning(All_SummMS2Table,
                     slices = 50,
                     mz_Tol = 2e-3):
    Low_mzVec = All_SummMS2Table[: -1, 1]
    High_mzVec = All_SummMS2Table[1: , 1]
    max_mz = High_mzVec[ -1]
    DifVec = High_mzVec - Low_mzVec
    ValleyLoc = np.where(DifVec > mz_Tol)[0]
    N_valleys = len(ValleyLoc)
    split_mzVec = np.linspace(0, N_valleys, slices, dtype = 'int')[1: -1]
    mz_ValleyVec = High_mzVec[ValleyLoc]
    contrast = Low_mzVec[ValleyLoc]
    EdgesMat = np.hstack((np.append([0], ValleyLoc[split_mzVec]).reshape(-1, 1),
                          np.append(ValleyLoc[split_mzVec], [len(High_mzVec) + 1]).reshape(-1, 1)))
    EdgesMat = np.hstack((EdgesMat,
                          np.arange(len(EdgesMat[:,0])).reshape(-1, 1)))
    return EdgesMat
