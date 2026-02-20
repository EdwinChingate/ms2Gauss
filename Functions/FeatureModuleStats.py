import numpy as np
from ttest import *
def FeatureModuleStats(All_FeaturesTable,
                       module,
                       SamplesNames,
                       IntramoduleCosineStatsVec,
                       feature_id,
                       percentile_mz = 5,
                       percentile_RT = 5):
    FeatureTable = All_FeaturesTable[module, :]
    N_samples = len(SamplesNames)
    AlignedSamplesVec = np.zeros((N_samples + 17))
    Samples_ids = np.array(FeatureTable[:, 6],
                           dtype = 'int')
    Samples_ids = set(list(Samples_ids))
    Samples_ids = np.array(list(Samples_ids))
    AlignedSamplesVec_loc = Samples_ids + 17
    AlignedSamplesVec[AlignedSamplesVec_loc] = 1    
    mz = np.median(FeatureTable[:, 1])
    AlignedSamplesVec[0] = mz
    AlignedSamplesVec[1] = np.percentile(FeatureTable[:, 1],
                                         percentile_mz)
    AlignedSamplesVec[2] = np.percentile(FeatureTable[:, 1],
                                         100 - percentile_mz)
    Q1_mz = np.percentile(FeatureTable[:, 1],
                          25)
    Q3_mz = np.percentile(FeatureTable[:, 1],
                          75)     
    IQR_mz = Q3_mz - Q1_mz    
    AlignedSamplesVec[3] = IQR_mz / mz * 1e6
    AlignedSamplesVec[4] = len(Samples_ids)
    AlignedSamplesVec[5] = len(module)
    AlignedSamplesVec[6: 11] = IntramoduleCosineStatsVec
    AlignedSamplesVec[11] = np.median(FeatureTable[:, 2])
    AlignedSamplesVec[12] = np.percentile(FeatureTable[:, 2],
                                          25)
    AlignedSamplesVec[13] = np.percentile(FeatureTable[:, 2],
                                          75)  
    AlignedSamplesVec[14] = np.percentile(FeatureTable[:, 2],
                                          percentile_RT)
    AlignedSamplesVec[15] = np.percentile(FeatureTable[:, 2],
                                          100 - percentile_RT)    
    AlignedSamplesVec[16] =int(feature_id)    
    return AlignedSamplesVec
