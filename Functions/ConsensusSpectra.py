import numpy as np
from ConsensusFragment import *
from MostIntenseFragmentNorm import *
def ConsensusSpectra(module,
                     N_Fragments,
                     AlignedFragments_mz_Mat,
                     AlignedFragmentsMat,
                     minSpectra = 3,
                     alpha = 0.01):
    consensus_spectra = []
    for fragment in np.arange(N_Fragments):
        SpectraFragmentVec = AlignedFragments_mz_Mat[fragment, np.array(module)+1]
        SpectraIntensityVec = AlignedFragmentsMat[fragment, np.array(module)+1]
        consensus_spectra = ConsensusFragment(SpectraFragmentVec = SpectraFragmentVec,
                                              SpectraIntensityVec = SpectraIntensityVec,
                                              consensus_spectra = consensus_spectra,
                                              minSpectra = minSpectra,
                                              alpha = alpha)  
    consensus_spectra = MostIntenseFragmentNorm(consensus_spectra = consensus_spectra)
    return consensus_spectra
