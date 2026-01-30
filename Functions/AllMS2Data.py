import numpy as np
from mz_RT_spectrum_filter import *
def AllMS2Data(DataSet,
               min_RT = 0,
               max_RT = 1e5,
               min_mz = 0,
               max_mz = 1e4):
    SummMS2 = []
    FirstSpec = True
    spectrum_id = 0
    for SpectralSignals in DataSet:
        SummMS2 = mz_RT_spectrum_filter(SpectralSignals = SpectralSignals,
                                        SummMS2 = SummMS2,
                                        min_RT = min_RT,
                                        max_RT = max_RT,
                                        min_mz = min_mz,
                                        max_mz = max_mz,
                                        spectrum_id = spectrum_id)
        spectrum_id += 1
    SummMS2 = np.array(SummMS2)      
    SummMS2 = SummMS2[SummMS2[:,0].argsort(),:]
    return SummMS2
