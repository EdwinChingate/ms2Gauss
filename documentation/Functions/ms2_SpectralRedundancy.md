---
title: ms2_SpectralRedundancy
kind: function
source: Functions/ms2_SpectralRedundancy.py
last_updated: 2025-02-14
---

## Description
`ms2_SpectralRedundancy` reads an MS2 summary spreadsheet, filters rows by RT/m/z, clusters redundant spectra via [`ms2_SpectralSimilarityClustering`](./ms2_SpectralSimilarityClustering.md), and builds a condensed [`SummMS2`](../Variables/SummMS2.md) array per sample. Scientifically, it merges multiple MS2 acquisitions targeting the same precursor so that downstream modeling works with a single umbrella per compound.

**Math notes**  
Redundancy is resolved with cosine similarity (threshold `cos_tol`) plus RT/m/z adjacency tolerances. For each cluster, the function selects the spectrum with the highest fragment intensity (`mostInt_ms2Frag`) as representative and records umbrella statistics (`min_RT`, `max_RT`, `N_spec`).

## Code
```python
import numpy as np
import pandas as pd
import os
from ms2_SpectralSimilarityClustering import *
def ms2_SpectralRedundancy(SummaryFile,min_RT=0,max_RT=1500,min_mz=0,max_mz=1200,ms2FolderName='ms2_spectra',ToReplace='mzML-ms2Summary.xlsx',mz_col=1,RT_col=2,RT_tol=20,mz_Tol=1e-2,sample_id_col=-1,ms2_spec_id_col=0,ToAdd='mzML',min_Int_Frac=2,cos_tol=0.9):
    home=os.getcwd()
    ms2Folder=home+'/'+ms2FolderName
    SummaryFileName=ms2Folder+'/'+SummaryFile
    SummMS2_raw=np.array(pd.read_excel(SummaryFileName))
    Filter=(SummMS2_raw[:,1]>min_mz)&(SummMS2_raw[:,1]<max_mz)&(SummMS2_raw[:,2]>min_RT)&(SummMS2_raw[:,2]<max_RT)
    SummMS2_raw=SummMS2_raw[Filter,:]
    SampleName=SummaryFile.replace(ToReplace,'')
    Modules=ms2_SpectralSimilarityClustering(SummMS2_raw=SummMS2_raw,SampleName=SampleName,mz_col=mz_col,RT_col=RT_col,RT_tol=RT_tol,mz_Tol=mz_Tol,sample_id_col=sample_id_col,ms2_spec_id_col=ms2_spec_id_col,ms2Folder=ms2Folder,ToAdd=ToAdd,min_Int_Frac=min_Int_Frac,cos_tol=cos_tol)
    N_modules=len(Modules)
    SummMS2=[]
    for mod_p in np.arange(N_modules,dtype='int'):
        mod=Modules[mod_p]
        mod_loc=0
        SummMS2_mod=SummMS2_raw[mod,:].copy()
        min_RT=np.min(SummMS2_mod[:,2])
        max_RT=np.max(SummMS2_mod[:,2])
        N_spec=len(mod)
        if N_spec>1:
            mostInt_ms2Frag=np.max(SummMS2_mod[:,4])
            mostInt_ms2Frag_Filter=SummMS2_mod[:,4]==mostInt_ms2Frag
            mod_loc=int(np.where(mostInt_ms2Frag_Filter)[0])
        SummMS2_mod=list(SummMS2_mod[mod_loc,:])
        ms2_spec_id=SummMS2_mod[0]
        SummMS2_mod=SummMS2_mod[1:]+[min_RT]+[max_RT]+[N_spec]+[ms2_spec_id]
        SummMS2.append(SummMS2_mod)
    SummMS2=np.array(SummMS2)
    return SummMS2
```

## Key operations
- Loads Excel summaries from `ms2_spectra/SummaryFile` and filters rows by RT/m/z bounds.
- Calls [`ms2_SpectralSimilarityClustering`](./ms2_SpectralSimilarityClustering.md) to obtain redundancy modules using cosine similarity on MS2 fragment intensities.
- For each module, finds the spectrum with maximum fragment intensity (column 4) to represent the cluster.
- Computes `min_RT`, `max_RT`, and `N_spec`, then appends them plus the representative `ms2_spec_id` to each row to match the [`SummMS2`](../Variables/SummMS2.md) schema.

## Parameters
- `SummaryFile (str)`: Excel filename inside `ms2FolderName`.
- `min_RT`, `max_RT`, `min_mz`, `max_mz`: filtering bounds.
- `ms2FolderName (str)`: folder storing per-sample summaries.
- `ToReplace`, `ToAdd`: strings controlling sample-name derivation.
- `mz_col`, `RT_col`: column indices for m/z and RT in the summary file.
- `RT_tol`, `mz_Tol`: tolerances passed to the clustering routine.
- `sample_id_col`, `ms2_spec_id_col`: column indices used to track sample IDs and raw MS2 IDs.
- `min_Int_Frac`, `cos_tol`: intensity fraction threshold and cosine similarity cutoff.

## Input
- [`SummMS2_raw`](../Variables/SummMS2.md) style table read from disk.
- Access to spectral folders for retrieving raw spectra inside [`ms2_SpectralSimilarityClustering`](./ms2_SpectralSimilarityClustering.md).

## Output
- [`SummMS2`](../Variables/SummMS2.md)

## Functions
- [`ms2_SpectralSimilarityClustering`](./ms2_SpectralSimilarityClustering.md)

## Called by
- Notebooks when raw vendor files are already summarized into Excel tables.

## Examples
```python
import numpy as np
from Functions.ms2_SpectralRedundancy import ms2_SpectralRedundancy

# Mocking by writing a temporary Excel file is omitted here; instead, assume SummMS2_raw is loaded.
# You can call the function directly once a summary workbook exists in ms2_spectra/.
SummMS2 = ms2_SpectralRedundancy('SampleA-mzML-ms2Summary.xlsx', min_RT=100, max_RT=800,
                                 min_mz=200, max_mz=800, cos_tol=0.95)
```
To visualize redundancy resolution, plot `N_spec` per feature:
```python
import matplotlib.pyplot as plt
plt.hist(SummMS2[:,7], bins=range(1,6))
plt.xlabel('Number of redundant MS2 spectra')
plt.ylabel('Count')
plt.show()
```
