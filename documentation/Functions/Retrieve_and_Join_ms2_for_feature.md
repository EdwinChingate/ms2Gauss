---
title: Retrieve_and_Join_ms2_for_feature
kind: function
source: Functions/Retrieve_and_Join_ms2_for_feature.py
last_updated: 2025-02-14
---

## Description
`Retrieve_and_Join_ms2_for_feature` loads raw MS2 spectra (CSV files) associated with a set of feature rows. Each spectrum is appended with the feature index and filtered by minimum relative intensity. The concatenated array feeds fragment-level clustering inside [`ms2_FeaturesDifferences`](./ms2_FeaturesDifferences.md).

## Code
```python
import pandas as pd
import numpy as np
import os
def Retrieve_and_Join_ms2_for_feature(All_FeaturesTable,Feature_module,SamplesNames,sample_id_col=16,ms2_spec_id_col=15,ms2Folder='ms2_spectra',ToAdd='mzML',min_Int_Frac=2):
    N_features=len(Feature_module)
    FeatureTable=All_FeaturesTable[Feature_module,:].copy()
    firstSpec=True
    All_ms2=[]
    for feature_id in np.arange(N_features,dtype='int'):
        features_stats=FeatureTable[feature_id,:]
        if sample_id_col>0:
            sample_id=int(features_stats[sample_id_col])
        else:
            sample_id=0
        ms2_spec_id=str(int(features_stats[ms2_spec_id_col]))
        sample_name_id=SamplesNames[sample_id]+ToAdd
        ms2_spectrumLoc=ms2Folder+'/'+sample_name_id+'/'+ms2_spec_id+'.csv'
        ExistSpectrum=os.path.exists(ms2_spectrumLoc)
        if ExistSpectrum:
            ms2_spectrumDF=pd.read_csv(ms2_spectrumLoc,index_col=0)
            ms2_spectrum=np.array(ms2_spectrumDF)
            N_peaks=len(ms2_spectrum[:,0])
            SpectrumLocVec=np.ones(N_peaks).reshape(-1,1)*feature_id
            ms2_spectrum=np.append(ms2_spectrum,SpectrumLocVec,axis=1)
            if firstSpec:
                All_ms2=ms2_spectrum
                firstSpec=False
            else:
                All_ms2=np.append(All_ms2,ms2_spectrum,axis=0)
    if len(All_ms2)==0:
        return []
    IntFrac_ms2_filter=All_ms2[:,9]>min_Int_Frac
    All_ms2=All_ms2[IntFrac_ms2_filter,:]
    return All_ms2
```

## Key operations
- Constructs file paths `ms2Folder/sampleName+ToAdd/ms2_spec_id.csv` for each feature.
- Loads spectra into numpy arrays and appends a column with the local `feature_id`.
- Filters fragments by relative intensity (`column 9 > min_Int_Frac`).

## Parameters
- `All_FeaturesTable`: stacked features.
- `Feature_module`: indices pointing to rows belonging to one cluster.
- `SamplesNames`: list mapping sample IDs to folder prefixes.
- `sample_id_col`, `ms2_spec_id_col`: column indices for sample and MS2 IDs.
- `ms2Folder`, `ToAdd`: folder structure hints.
- `min_Int_Frac`: minimum relative intensity percentage.

## Input
- [`All_FeaturesTable`](../Variables/All_FeaturesTable.md)
- Disk-stored MS2 spectra.

## Output
- `All_ms2`: numpy array containing concatenated MS2 fragments with appended feature indices.

## Functions
- Uses pandas and numpy only.

## Called by
- [`ms2_FeaturesDifferences`](./ms2_FeaturesDifferences.md)

## Examples
```python
from Functions.Retrieve_and_Join_ms2_for_feature import Retrieve_and_Join_ms2_for_feature
All_ms2 = Retrieve_and_Join_ms2_for_feature(All_FeaturesTable, Feature_module=[0,1],
                                           SamplesNames=['Sample_A','Sample_B'])
print(All_ms2.shape)
```
