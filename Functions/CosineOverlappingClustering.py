import numpy as np
from Retrieve_and_Join_ms2_for_feature import *
from AlignFragmentsEngine import *
from CosineMatrix import *
from AdjacencyList_from_matrix import *
from CommunityBlocks import *
from OverlappingClustering import *
def CosineOverlappingClustering(Feature_module,
                                All_FeaturesTable,
                                SamplesNames,
                                Intensity_to_explain = 0.9,
                                Spectra_idVec = [],
                                All_ms2 = [],
                                sample_id_col = 16,
                                ms2_spec_id_col = 15,
                                min_spectra = 3,
                                cos_tol = 0.9,
                                percentile = 10,
                                slice_id = 0,
                                ms2Folder = 'ms2_spectra',
                                ToAdd = 'mzML',
                                Norm2One = False):   
    if len(Spectra_idVec) == 0:
        All_ms2, Spectra_idVec = Retrieve_and_Join_ms2_for_feature(All_FeaturesTable = All_FeaturesTable,
                                                                   Feature_module = Feature_module,
                                                                   SamplesNames = SamplesNames,
                                                                   sample_id_col = sample_id_col,
                                                                   ms2_spec_id_col = ms2_spec_id_col,
                                                                   ms2Folder = ms2Folder,
                                                                   ToAdd = ToAdd,
                                                                   Norm2One = Norm2One)
    if len(All_ms2) == 0:
        return []
    Feature_module = np.array(Feature_module)[Spectra_idVec].tolist()
    AlignedFragmentsMat, AlignedFragments_mz_Mat, Explained_fractionInt, N_features = AlignFragmentsEngine(All_ms2 = All_ms2,
                                                                                                           Feature_module = Feature_module,
                                                                                                           Intensity_to_explain = Intensity_to_explain,
                                                                                                           min_spectra = min_spectra)
    CosineMat = CosineMatrix(AlignedFragmentsMat = AlignedFragmentsMat,
                             N_features = N_features)
    AdjacencyList_Features, features_ids = AdjacencyList_from_matrix(CosineMat = CosineMat,
                                                                     N_ms2_spectra = N_features,
                                                                     cos_tol = cos_tol)
    Feature_Modules = CommunityBlocks(AdjacencyList_Features = AdjacencyList_Features)
    
    
    Modules, IntramoduleSimilarity = OverlappingClustering(Feature_Modules = Feature_Modules,
                                                           CosineMat = CosineMat.copy(),
                                                           percentile = percentile)   

    
    This_Module_FeaturesTable = All_FeaturesTable[Feature_module, :].copy()
    This_Module_FeaturesTable = np.hstack((This_Module_FeaturesTable,
                                           Explained_fractionInt))
    This_Module_FeaturesTable = np.hstack((This_Module_FeaturesTable,
                                           slice_id * np.ones(len(Explained_fractionInt)).reshape(-1, 1)))    
    feature_cluster_data = [Modules,
                            Feature_module,
                            IntramoduleSimilarity,
                            This_Module_FeaturesTable,
                            AlignedFragmentsMat,
                            AlignedFragments_mz_Mat]
    return feature_cluster_data
