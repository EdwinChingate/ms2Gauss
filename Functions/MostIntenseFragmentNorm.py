import numpy as np
def MostIntenseFragmentNorm(consensus_spectra):
    consensus_spectra = np.array(consensus_spectra)
    maxInt = np.max(consensus_spectra[:, 6])
    maxIntFragLoc = np.where(consensus_spectra[:, 6] == maxInt)
    if len(maxIntFragLoc) > 1:
        maxIntFragLoc = maxIntFragLoc[0][0]
    else: 
        maxIntFragLoc = maxIntFragLoc[0]
    NormIntenseVec = 100 * consensus_spectra[:, 6] / consensus_spectra[maxIntFragLoc, 6]
    NormIntenseVec = NormIntenseVec.reshape(-1, 1)
    NormIntenseCIVec = 100 * consensus_spectra[:, 8] / consensus_spectra[maxIntFragLoc, 6]
    NormIntenseCIVec = NormIntenseCIVec.reshape(-1, 1)
    consensus_spectra = np.hstack((consensus_spectra, NormIntenseVec))
    consensus_spectra = np.hstack((consensus_spectra, NormIntenseCIVec))
    return consensus_spectra
