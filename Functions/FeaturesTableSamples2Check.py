import numpy as np
from ConsensusSpectra import *
def FeaturesTableSamples2Check(Feature_Module,
                               All_FeaturesTable):
    FeatureClusterTable = All_FeaturesTable[Feature_Module, :]
    Samples_ids_inFeatureCluster = FeatureClusterTable[:, 6].tolist()
   # Spectra2Check = list(set(np.arange(len(All_FeaturesTable)).tolist()) - set(Feature_Module))
   # FeatureTable = All_FeaturesTable[Spectra2Check, :]
    Samples_ids = All_FeaturesTable[:, 6].tolist()    
    Samples_ids2Check = list(set(Samples_ids) - set(Samples_ids_inFeatureCluster))
    Samples_ids2Check.sort()    
    Samples_ids2Check = [int(sample_id) for sample_id in Samples_ids2Check]
    #Samples_FeaturesTablesList = []
    Samples_FeaturesIdsList = [[]] * len(Samples_ids)
    for sample_id in Samples_ids2Check:
        FeaturesTable = All_FeaturesTable[Feature_Module, :]
        AllSamples_ids = np.array(FeaturesTable[:, 6],
                                  dtype = 'int')
        SampleFilter = np.where(AllSamples_ids == sample_id)[0]
        Sample_FeaturesTable = FeaturesTable[SampleFilter, :]
        Samples_FeaturesIdsList[sample_id] = Sample_FeaturesTable[:, 7].tolist()
        #Samples_FeaturesTablesList.append(Sample_FeaturesTable)
        #Samples_FeaturesIdsList.append(All_FeaturesTable[:, 7].tolist())
    return [Samples_FeaturesIdsList, Samples_ids2Check]
