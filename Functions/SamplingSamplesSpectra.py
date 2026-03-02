import numpy as np
from ConsensusSpectra import *
def SamplingSamplesSpectra(Samples_FeaturesIdsList,
                           Samples_ids2Check,
                           Nspectra_sampling = 3):
    SamplesSamplesList = []
    for sample_id in Samples_ids2Check:        
        if len(Samples_FeaturesIdsList[sample_id]) > Nspectra_sampling:
            rng = np.random.default_rng()
            sample_per_sample = rng.choice(Samples_FeaturesIdsList[sample_id],
                                           size = Nspectra_sampling).tolist()    
        else:
            sample_per_sample = Samples_FeaturesIdsList[sample_id]
        sample_per_sample = [int(spectra_id) for spectra_id in sample_per_sample] #Temp
        SamplesSamplesList += sample_per_sample
    return SamplesSamplesList
