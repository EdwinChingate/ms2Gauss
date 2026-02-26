import numpy as np
import pandas as pd
from UpdateUniqueModulesAfterClustering import *
from ConsensusSpectra  import *
from CosineOverlappingClustering import *
from UpdateIntramoduleSimilarityAfterClustering  import *
from Retrieve_and_Join_ms2_for_feature  import *
from AlignFragmentsEngine  import *
def SummarizeSampling(feature_clusterList,
                      All_FeaturesTable,
                      SamplesNames,
                      min_spectra = 3,
                      Intensity_to_explain = 0.9,
                      cos_tol = 0.9,
                      percentile = 10,
                      slice_id = 0,
                      sample_id_col = 16,
                      ms2_spec_id_col = 15,
                      percentile_mz = 5,
                      percentile_Int = 10,
                      ms2Folder = 'ms2_spectra',
                      ToAdd = 'mzML',
                      Norm2One = False):
    ModulesList = []
    FirstSpectra = True
    IntramoduleSimilarityList = []
    feature_id = 0
    BigFeature_Module = []
    for feature_cluster_data in feature_clusterList:
        Modules, Feature_Module, IntramoduleSimilarity, This_Module_FeaturesTable, AlignedFragmentsMat, AlignedFragments_mz_Mat = feature_cluster_data        
        for module_id in np.arange(len(Modules)):   
            module = Modules[module_id]
            IntramoduleSimilarityVec = IntramoduleSimilarity[module_id, :]
            consensus_spectraDF = ConsensusSpectra(module = module,
                                                   min_spectra = min_spectra,
                                                   AlignedFragmentsMat = AlignedFragmentsMat,
                                                   AlignedFragments_mz_Mat = AlignedFragments_mz_Mat,
                                                   percentile_mz = percentile_mz,
                                                   percentile_Int = percentile_Int,
                                                   reduceIQR_factor = 6,
                                                   Columns_to_return = np.array([ 0, 2, 3, 9, 10, 11, 17, 18, 19, 20]))             
            if len(consensus_spectraDF) > 0:
                consensus_spectraDF['feature_id'] = feature_id
                if FirstSpectra:
                    All_consensus_ms2 = consensus_spectraDF
                    FirstSpectra = False
                else:
                    All_consensus_ms2 = pd.concat([All_consensus_ms2, consensus_spectraDF],
                                                  ignore_index = True)            
                ModulesList.append(np.array(Feature_Module)[module].tolist())  
                IntramoduleSimilarityList.append(IntramoduleSimilarityVec)
                BigFeature_Module += Feature_Module
                feature_id += 1
    feature_cluster_data = CosineOverlappingClustering(All_ms2 = np.array(All_consensus_ms2),
                                                       SamplesNames = SamplesNames,
                                                       All_FeaturesTable = All_FeaturesTable,
                                                       Feature_module = np.arange(len(ModulesList)),
                                                       Spectra_idVec = np.arange(len(ModulesList)),
                                                       Intensity_to_explain = 1,
                                                       min_spectra = min_spectra,
                                                       cos_tol = cos_tol,
                                                       percentile = percentile,
                                                       slice_id = slice_id)   
    Modules, Feature_Module, IntramoduleSimilarity, This_Module_FeaturesTable, AlignedFragmentsMat, AlignedFragments_mz_Mat = feature_cluster_data
    IntramoduleSimilarityModulesMat = UpdateIntramoduleSimilarityAfterClustering(Modules = Modules,
                                                                                 IntramoduleSimilarityList = IntramoduleSimilarityList)
    Modules = UpdateUniqueModulesAfterClustering(New_Modules = Modules,
                                                 Modules = ModulesList)
    Feature_Module = list(set(BigFeature_Module))
    All_ms2, Spectra_idVec = Retrieve_and_Join_ms2_for_feature(All_FeaturesTable = All_FeaturesTable,
                                                               Feature_module = Feature_Module,
                                                               SamplesNames = SamplesNames,
                                                               sample_id_col = sample_id_col,
                                                               ms2_spec_id_col = ms2_spec_id_col,
                                                               ms2Folder = ms2Folder,
                                                               ToAdd = ToAdd,
                                                               Norm2One = Norm2One)
    AlignedFragmentsMat, AlignedFragments_mz_Mat, Explained_fractionInt, N_features = AlignFragmentsEngine(All_ms2 = All_ms2,
                                                                                                           Feature_module = Feature_Module,
                                                                                                           Intensity_to_explain = Intensity_to_explain,
                                                                                                           min_spectra = min_spectra)
    BigExplained_fractionIntVec = np.zeros(len(All_FeaturesTable)).reshape(-1, 1)
    BigExplained_fractionIntVec[Feature_Module] = Explained_fractionInt
    This_Module_FeaturesTable = All_FeaturesTable.copy()
    This_Module_FeaturesTable = np.hstack((This_Module_FeaturesTable,
                                           BigExplained_fractionIntVec))
    This_Module_FeaturesTable = np.hstack((This_Module_FeaturesTable,
                                           slice_id * np.ones(len(BigExplained_fractionIntVec)).reshape(-1, 1)))    
    
    BigAlignedFragmentsMat = np.zeros((AlignedFragmentsMat.shape[0],
                                       len(All_FeaturesTable) + 1))
    BigAlignedFragments_mz_Mat = np.zeros((AlignedFragmentsMat.shape[0],
                                           len(All_FeaturesTable) + 1))  
    BigAlignedFragmentsMat[:, 0] = AlignedFragmentsMat[:, 0]
    BigAlignedFragments_mz_Mat[:, 0] = AlignedFragments_mz_Mat[:, 0]
    column_count = 1
    for spectra_id in Feature_Module:
        BigAlignedFragmentsMat[ :, spectra_id + 1] = AlignedFragmentsMat[:, column_count]
        BigAlignedFragments_mz_Mat[ :, spectra_id + 1] = AlignedFragments_mz_Mat[:, column_count]
        column_count += 1
    feature_cluster_data = [Modules,
                            np.arange(len(All_FeaturesTable), dtype = 'int').tolist(),
                            IntramoduleSimilarityModulesMat,
                            This_Module_FeaturesTable,
                            BigAlignedFragmentsMat,
                            BigAlignedFragments_mz_Mat]
    return feature_cluster_data
