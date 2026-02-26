import numpy as np
import pandas as pd
from UpdateUniqueModulesAfterClustering import *
from ReOrganizeSamplingResults  import *
from FormattingSummary import *
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

    All_consensus_ms2, ModulesList, IntramoduleSimilarityList, BigFeature_Module = ReOrganizeSamplingResults(feature_clusterList = feature_clusterList,
                                                                                                             min_spectra = min_spectra,
                                                                                                             percentile_mz = percentile_mz,
                                                                                                             percentile_Int = percentile_Int)
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
    feature_cluster_data = FormattingSummary(All_FeaturesTable = All_FeaturesTable,
                                             Modules = Modules,
                                             Feature_Module = Feature_Module,
                                             Explained_fractionInt = Explained_fractionInt,
                                             slice_id = slice_id,
                                             AlignedFragmentsMat = AlignedFragmentsMat,
                                             AlignedFragments_mz_Mat = AlignedFragments_mz_Mat)
    return feature_cluster_data
