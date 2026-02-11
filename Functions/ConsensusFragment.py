from ttest import *
from scipy import stats
import numpy as np
def ConsensusFragment(SpectraFragmentVec,
                      SpectraIntensityVec,
                      consensus_spectra,
                      alpha = 0.01,
                      minSpectra = 3):
    SpectraFragmentLoc = np.where(SpectraFragmentVec > 0)
    N_spectra = len(SpectraFragmentVec[SpectraFragmentLoc])
    if N_spectra < minSpectra:
        return consensus_spectra
    mz = np.mean(SpectraFragmentVec[SpectraFragmentLoc])
    min_mz = np.min(SpectraFragmentVec[SpectraFragmentLoc])
    max_mz = np.max(SpectraFragmentVec[SpectraFragmentLoc])  
    mz_std = np.std(SpectraFragmentVec[SpectraFragmentLoc])
    stat, p = stats.shapiro(SpectraFragmentVec[SpectraFragmentLoc])
    t_ref = ttest(Nsignals = N_spectra,
                  alpha = alpha)
    mz_CI = t_ref * mz_std / np.sqrt(N_spectra)
    mz_CIppm = mz_CI / mz * 1e6       
    IntensityContribution = np.mean(SpectraIntensityVec) 
    IntensityContribution_std = np.std(SpectraIntensityVec)     
    IntensityContribution_CI = t_ref * IntensityContribution_std / np.sqrt(len(SpectraIntensityVec))
    consensus_spectra.append([mz,
                              mz_std,
                              p,
                              N_spectra,
                              mz_CI,
                              mz_CIppm,
                              IntensityContribution,
                              IntensityContribution_std,
                              IntensityContribution_CI,
                              min_mz,
                              max_mz,
                              (max_mz-min_mz)/mz*1e6])    
    return consensus_spectra
