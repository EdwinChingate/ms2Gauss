from AdjacencyList_ms2Fragments import *
from ms2_feat_modules import *
from AligniningFragments_in_Feature import *
from minimalAlignedFragmentsMat import *
def AlignFragmentsEngine(All_ms2,
                         Feature_module,
                         Intensity_to_explain = 0.9,
                         min_spectra = 3):
    AdjacencyListFragments, feat_ids = AdjacencyList_ms2Fragments(All_ms2 = All_ms2)
    N_features = len(Feature_module)
    Frag_Modules = ms2_feat_modules(AdjacencyList = AdjacencyListFragments,
                                    ms2_ids = feat_ids)
    AlignedFragmentsMat, AlignedFragments_mz_Mat = AligniningFragments_in_Feature(Frag_Modules = Frag_Modules,
                                                                                  All_ms2 = All_ms2,
                                                                                  N_features = N_features)   
    AlignedFragmentsMat, AlignedFragments_mz_Mat, Explained_fractionInt = minimalAlignedFragmentsMat(AlignedFragmentsMat = AlignedFragmentsMat,
                                                                                                     AlignedFragments_mz_Mat = AlignedFragments_mz_Mat,
                                                                                                     Intensity_to_explain = Intensity_to_explain,
                                                                                                     min_spectra = min_spectra)
    return [AlignedFragmentsMat, AlignedFragments_mz_Mat, Explained_fractionInt, N_features]
