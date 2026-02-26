import numpy as np
from CosineOverlappingClustering import *
from SummarizeSampling import *
def FeatureClusterData(Feature_module,
                       All_FeaturesTable,
                       SamplesNames,
                       Intensity_to_explain = 0.9,
                       min_spectra = 3,
                       cos_tol = 0.9,
                       percentile = 10,
                       percentile_mz = 5,
                       percentile_Int = 10,
                       slice_id = 0,
                       max_Nspectra_cluster = 170,
                       Nspectra_sampling = 54,
                       SamplingTimes = 10,
                       sample_id_col = 16,
                       ms2_spec_id_col = 15,
                       ms2Folder = 'ms2_spectra',
                       ToAdd = 'mzML',
                       Norm2One = False):
    if len(Feature_module) < max_Nspectra_cluster:
        feature_cluster_data = CosineOverlappingClustering(All_FeaturesTable = All_FeaturesTable,
                                                           Feature_module = Feature_module,
                                                           sample_id_col = sample_id_col,
                                                           SamplesNames = SamplesNames,
                                                           ms2_spec_id_col = ms2_spec_id_col,
                                                           min_spectra = min_spectra,
                                                           cos_tol = cos_tol,
                                                           percentile = percentile,
                                                           slice_id = slice_id,
                                                           ms2Folder = ms2Folder,
                                                           ToAdd = ToAdd,
                                                           Norm2One = Norm2One,
                                                           Intensity_to_explain = Intensity_to_explain)  
        return [feature_cluster_data, 0]
    feature_clusterList = []
    for sampling in np.arange(SamplingTimes):
        rng = np.random.default_rng()
        Sample_Feature_module = rng.choice(Feature_module,
                                           size = Nspectra_sampling)
        feature_cluster_data = CosineOverlappingClustering(All_FeaturesTable = All_FeaturesTable,
                                                           Feature_module = Sample_Feature_module,
                                                           sample_id_col = sample_id_col,
                                                           ms2_spec_id_col = ms2_spec_id_col,
                                                           SamplesNames = SamplesNames,
                                                           Intensity_to_explain = Intensity_to_explain,
                                                           min_spectra = min_spectra,
                                                           cos_tol = cos_tol,
                                                           percentile = percentile,
                                                           slice_id = slice_id,
                                                           ms2Folder = ms2Folder,
                                                           ToAdd = ToAdd,
                                                           Norm2One = Norm2One)          
        feature_clusterList.append(feature_cluster_data)
    feature_cluster_data = SummarizeSampling(feature_clusterList = feature_clusterList,
                                             All_FeaturesTable = All_FeaturesTable.copy(),
                                             SamplesNames = SamplesNames,
                                             Intensity_to_explain = Intensity_to_explain,
                                             min_spectra = min_spectra,
                                             cos_tol = cos_tol,
                                             percentile = percentile,
                                             slice_id = slice_id,
                                             sample_id_col = sample_id_col,
                                             ms2_spec_id_col = ms2_spec_id_col,
                                             percentile_mz = percentile_mz,
                                             percentile_Int = percentile_Int,
                                             ms2Folder = ms2Folder,
                                             ToAdd = ToAdd,
                                             Norm2One = Norm2One)
    
    return [feature_cluster_data, 1]
