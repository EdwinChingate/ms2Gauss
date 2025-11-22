---
title: JoiningFeatures
kind: function
source: Functions/JoiningFeatures.py
last_updated: 2025-02-14
---

## Description
`JoiningFeatures` scans a results folder for per-sample feature spreadsheets (typically exported from [`Cluster_ms2_Features`](./Cluster_ms2_Features.md) or downstream notebooks), loads them into numpy arrays, appends the sample index, and concatenates them into [`All_FeaturesTable`](../Variables/All_FeaturesTable.md). This prepares the data for cross-sample alignment.

## Code
```python
import pandas as pd
import numpy as np
import os
def JoiningFeatures(ResultsFolder,mz_min=0,mz_max=1200,RT_min=0,RT_max=2000,ToReplace='.mzML.xlsx'):
    SamplesNames=[]
    SamplesList=os.listdir(ResultsFolder)
    SamplesList.sort()
    N_samples=len(SamplesList)
    firstTable=True
    for sample_id in np.arange(N_samples,dtype='int'):
        features_table=SamplesList[sample_id]
        sample_name=features_table.replace(ToReplace,'')
        SamplesNames.append(sample_name)
        features_table_name=ResultsFolder+'/'+features_table
        FeaturesTableDF=pd.read_excel(features_table_name,index_col=0)
        FeaturesTable=np.array(FeaturesTableDF)
        N_features=len(FeaturesTable[:,0])
        featureLocVec=np.ones(N_features).reshape(-1,1)*sample_id
        FeaturesTable=np.append(FeaturesTable,featureLocVec,axis=1)
        if firstTable:
            All_FeaturesTable=FeaturesTable
            firstTable=False
        else:
            All_FeaturesTable=np.append(All_FeaturesTable,FeaturesTable,axis=0)
    Filter=(All_FeaturesTable[:,3]>mz_min)&(All_FeaturesTable[:,3]<mz_max)&(All_FeaturesTable[:,2]>RT_min)&(All_FeaturesTable[:,2]<RT_max)
    All_FeaturesTable=All_FeaturesTable[Filter,:]
    return [All_FeaturesTable,SamplesNames]
```

## Key operations
- Reads every file in `ResultsFolder`, sorts them for deterministic sample ordering, and derives `SamplesNames` by stripping `ToReplace` from filenames.
- Converts each Excel table to numpy, appends a column filled with the integer `sample_id`, and concatenates vertically.
- Applies coarse `mz`/`RT` filters to trim the merged array.

## Parameters
- `ResultsFolder (str)`: directory containing per-sample Excel outputs.
- `mz_min/max`, `RT_min/max`: filters applied after merging.
- `ToReplace`: suffix removed from filenames to obtain sample names.

## Input
- Excel files exported from feature detection (one per sample).

## Output
- [`All_FeaturesTable`](../Variables/All_FeaturesTable.md)
- `SamplesNames` (list of strings)

## Functions
- Uses pandas for I/O and numpy for concatenation.

## Called by
- [`Features_ms2_SamplesAligment`](./Features_ms2_SamplesAligment.md)

## Examples
```python
from Functions.JoiningFeatures import JoiningFeatures
All_FeaturesTable, SampleNames = JoiningFeatures('results', mz_min=250, mz_max=800)
print('Merged features:', All_FeaturesTable.shape[0])
print('Samples:', SampleNames)
```
Visualize the distribution of sample IDs in the merged table:
```python
import matplotlib.pyplot as plt
plt.hist(All_FeaturesTable[:,16], bins=range(len(SampleNames)+1))
plt.xlabel('Sample ID')
plt.ylabel('Number of features')
plt.show()
```
