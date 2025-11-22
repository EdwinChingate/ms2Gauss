---
title: Features_ms2_SamplesAligment
kind: function
source: Functions/Features_ms2_SamplesAligment.py
last_updated: 2025-02-14
---

## Description
`Features_ms2_SamplesAligment` merges feature tables from multiple samples, clusters them via [`ms2_SpectralSimilarityClustering`](./ms2_SpectralSimilarityClustering.md), and produces aligned matrices containing consensus metadata plus per-sample intensities and RTs. The function returns [`AlignedSamplesDF`](../Variables/AlignedSamplesDF.md) and [`AlignedSamples_RT_DF`](../Variables/AlignedSamples_RT_DF.md), enabling experiment-wide comparisons.

## Code
```python
import numpy as np
import pandas as pd
import os
import datetime
from JoiningFeatures import *
from ms2_SpectralSimilarityClustering import *
def Features_ms2_SamplesAligment(ResultsFolderName,mz_min=254,mz_max=255,RT_min=0,RT_max=2000,RT_tol=30,mz_Tol=0,min_Int_Frac=1,cos_tol=0.9,ToReplace='.mzML.xlsx',ms2Folder='ms2_spectra',ToAdd='mzML',saveAlignedTable=False,name="SamplesAligment"):
    home=os.getcwd()
    ResultsFolder=home+'/'+ResultsFolderName
    All_FeaturesTable,SamplesNames=JoiningFeatures(ResultsFolder=ResultsFolder,mz_min=mz_min,mz_max=mz_max,RT_min=RT_min,RT_max=RT_max,ToReplace=ToReplace)
    Modules=ms2_SpectralSimilarityClustering(SummMS2_raw=All_FeaturesTable,SamplesNames=SamplesNames,mz_col=3,RT_col=2,RT_tol=RT_tol,mz_Tol=mz_Tol,sample_id_col=16,ms2_spec_id_col=15,ms2Folder=ms2Folder,ToAdd=ToAdd,min_Int_Frac=min_Int_Frac,cos_tol=cos_tol)
    N_samples=len(SamplesNames)
    N_Features=len(Modules)
    AlignedSamplesMat=np.zeros((N_Features,N_samples+7))
    AlignedSamples_RT_Mat=np.zeros((N_Features,N_samples+7))
    for feature_id in np.arange(N_Features,dtype='int'):
        Feature_module=Modules[feature_id]
        FeatureTable=All_FeaturesTable[Feature_module,:]
        AlignedSamplesMat[feature_id,0]=np.mean(FeatureTable[:,3])
        AlignedSamplesMat[feature_id,1]=np.mean(FeatureTable[:,4])
        AlignedSamplesMat[feature_id,2]=np.mean(FeatureTable[:,8])
        AlignedSamplesMat[feature_id,3]=np.mean(FeatureTable[:,9])
        AlignedSamplesMat[feature_id,4]=np.mean(FeatureTable[:,2])
        AlignedSamplesMat[feature_id,5]=np.min(FeatureTable[:,12])
        AlignedSamplesMat[feature_id,6]=np.max(FeatureTable[:,13])
        Samples_ids=np.array(FeatureTable[:,16],dtype='int')
        AlignedSamplesMat_loc=Samples_ids+7
        AlignedSamplesMat[feature_id,AlignedSamplesMat_loc]=FeatureTable[:,5]
        AlignedSamples_RT_Mat[feature_id,AlignedSamplesMat_loc]=FeatureTable[:,2]
    AlignedSamples_RT_Mat[:,:7]=AlignedSamplesMat[:,:7].copy()
    AlignedSamplesMat=AlignedSamplesMat[AlignedSamplesMat[:,0].argsort()]
    AlignedSamples_RT_Mat=AlignedSamples_RT_Mat[AlignedSamples_RT_Mat[:,0].argsort()]
    Columns=['mz_(Da)','mz_std_(Da)','mz_ConfidenceInterval_(Da)','mz_ConfidenceInterval_(ppm)','RT_(s)','min_RT_(s)','max_RT_(s)']+SamplesNames
    AlignedSamplesDF=pd.DataFrame(AlignedSamplesMat,columns=Columns)
    AlignedSamples_RT_DF=pd.DataFrame(AlignedSamples_RT_Mat,columns=Columns)
    if saveAlignedTable:
        date=datetime.datetime.now()
        string_date=str(date)
        string_date=string_date[:16].replace(':',"_")
        string_date=string_date.replace(' ',"_")
        name=name+"_"+string_date+'.xlsx'
        AlignedSamplesDF.to_excel(name)
        AlignedSamples_RT_DF.to_excel('RT_'+name)
    return [AlignedSamplesDF,AlignedSamples_RT_DF]
```

## Key operations
- Uses [`JoiningFeatures`](./JoiningFeatures.md) to stack per-sample tables into [`All_FeaturesTable`](../Variables/All_FeaturesTable.md).
- Clusters rows across samples using cosine similarity and RT/m/z tolerances.
- Computes consensus statistics (average m/z, CI, RT, umbrella bounds) per module.
- Populates two matrices: one with sample intensities (column 5 values) and one with sample RTs.
- Optionally writes Excel files with timestamps for archival purposes.

## Parameters
- `ResultsFolderName (str)`: directory containing per-sample feature spreadsheets.
- `mz_min/max`, `RT_min/max`: coarse filters applied before alignment.
- `RT_tol`, `mz_Tol`: tolerances passed to the clustering routine.
- `min_Int_Frac`, `cos_tol`: cosine similarity constraints.
- `ToReplace`: suffix removed from filenames when deriving sample names.
- `ms2Folder`, `ToAdd`: used when reloading raw spectra inside `ms2_SpectralSimilarityClustering`.
- `saveAlignedTable (bool)`, `name (str)`: control Excel export.

## Input
- [`All_FeaturesTable`](../Variables/All_FeaturesTable.md)

## Output
- [`AlignedSamplesDF`](../Variables/AlignedSamplesDF.md)
- [`AlignedSamples_RT_DF`](../Variables/AlignedSamples_RT_DF.md)

## Functions
- [`JoiningFeatures`](./JoiningFeatures.md)
- [`ms2_SpectralSimilarityClustering`](./ms2_SpectralSimilarityClustering.md)

## Called by
- Alignment notebooks and downstream statistical workflows.

## Examples
```python
from Functions.Features_ms2_SamplesAligment import Features_ms2_SamplesAligment
AlignedDF, AlignedRT = Features_ms2_SamplesAligment('results', mz_min=250, mz_max=800,
                                                    RT_min=0, RT_max=1500, RT_tol=20,
                                                    cos_tol=0.95)
print(AlignedDF.head())
```
Visualize intensities for a feature across samples:
```python
import matplotlib.pyplot as plt
row = AlignedDF.iloc[0]
row.iloc[7:].plot(kind='bar')
plt.ylabel('Intensity (a.u.)')
plt.title(f"Feature at m/z {row['mz_(Da)']:.4f}")
plt.show()
```
