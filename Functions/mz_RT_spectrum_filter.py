import numpy as np
def mz_RT_spectrum_filter(SpectralSignals,
                          SummMS2,
                          min_RT,
                          max_RT,
                          min_mz,
                          max_mz,
                          spectrum_id):
    MSLevel = SpectralSignals.getMSLevel()
    if MSLevel != 2:    
        return SummMS2
    RT = SpectralSignals.getRT()   
    if RT < min_RT or RT > max_RT:
        return SummMS2
    Precursor = SpectralSignals.getPrecursors()[0]
    MZ = Precursor.getMZ()
    if MZ < min_mz or MZ > max_mz:
        return SummMS2
    Spectrum = np.array(SpectralSignals.get_peaks()).T
    maxInt = np.max(Spectrum[:,1])
    TotalInt = np.sum(Spectrum[:,1])    
    AllInt = np.sum(Spectrum[:,1])
    maxInt_frac = maxInt/AllInt
    SummSpec = np.array([MZ,RT,spectrum_id,TotalInt,maxInt_frac])
    SummMS2.append(SummSpec)
    return SummMS2
