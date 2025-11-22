---
title: ms2_SpectralSimilarityClustering
kind: function
source: Functions/ms2_SpectralSimilarityClustering.py
last_updated: 2025-02-14
---

## Description
`ms2_SpectralSimilarityClustering` groups MS2 detections that are close in m/z and RT and have similar fragment patterns. It constructs adjacency lists using [`AdjacencyListFeatures`](./AdjacencyListFeatures.md), refines them with cosine similarity scores computed inside [`ms2_FeaturesDifferences`](./ms2_FeaturesDifferences.md), and returns a list of feature modules. These modules drive redundancy removal in [`ms2_SpectralRedundancy`](./ms2_SpectralRedundancy.md) and multi-sample alignment.

## Code
```python
import pandas as pd
import numpy as np
from AdjacencyListFeatures import *
from ms2_feat_modules import *
from ms2_FeaturesDifferences import *
def ms2_SpectralSimilarityClustering(SummMS2_raw,SampleName='',SamplesNames=[],mz_col=1,RT_col=2,RT_tol=20,mz_Tol=1e-2,sample_id_col=-1,ms2_spec_id_col=0,ms2Folder='ms2_spectra',ToAdd='mzML',min_Int_Frac=2,cos_tol=0.9):
    if len(SamplesNames)==0:
        SamplesNames=[SampleName]
    AdjacencyList,feat_ids=AdjacencyListFeatures(MS2_features=SummMS2_raw,mz_col=mz_col,RT_col=RT_col,RT_tol=RT_tol,mz_Tol=mz_Tol)
    RawModules=ms2_feat_modules(AdjacencyList=AdjacencyList,ms2_ids=feat_ids)
    Modules=[]
    for Feature_module in RawModules:
        Feature_Modules=ms2_FeaturesDifferences(All_FeaturesTable=SummMS2_raw,Feature_module=Feature_module,SamplesNames=SamplesNames,sample_id_col=sample_id_col,ms2_spec_id_col=ms2_spec_id_col,ms2Folder=ms2Folder,ToAdd=ToAdd,min_Int_Frac=min_Int_Frac,cos_tol=cos_tol)
        Modules+=Feature_Modules
    return Modules
```

## Key operations
- Builds an adjacency list in RT/m/z space to limit pairwise comparisons to plausible neighbors.
- Converts adjacency information into connected components via [`ms2_feat_modules`](./ms2_feat_modules.md).
- Calls [`ms2_FeaturesDifferences`](./ms2_FeaturesDifferences.md) to compute cosine similarities using raw spectral files stored in `ms2Folder` and enforce `cos_tol` and `min_Int_Frac` constraints.
- Returns a list where each entry is an array of row indices referencing `SummMS2_raw` (or `All_FeaturesTable`).

## Parameters
- `SummMS2_raw (np.ndarray)`: MS2 detections prior to redundancy removal.
- `SampleName` / `SamplesNames`: textual identifiers for logging and retrieving files.
- `mz_col`, `RT_col`: columns used for tolerance checks.
- `RT_tol`, `mz_Tol`: bounds for adjacency creation.
- `sample_id_col`, `ms2_spec_id_col`: positions of sample and MS2 IDs, used to fetch raw spectra.
- `ms2Folder (str)`: path containing mzML-derived spectra needed for cosine comparisons.
- `ToAdd (str)`: suffix inserted when constructing filenames.
- `min_Int_Frac`: minimum intensity fraction for fragments compared during cosine calculations.
- `cos_tol`: similarity threshold.

## Input
- Called by [`ms2_SpectralRedundancy`](./ms2_SpectralRedundancy.md) with `SummMS2_raw` arrays.
- Also invoked by [`Features_ms2_SamplesAligment`](./Features_ms2_SamplesAligment.md) when clustering cross-sample features.

## Output
- `Modules`: list of numpy arrays (indices) describing feature clusters.

## Functions
- [`AdjacencyListFeatures`](./AdjacencyListFeatures.md)
- [`ms2_feat_modules`](./ms2_feat_modules.md)
- [`ms2_FeaturesDifferences`](./ms2_FeaturesDifferences.md)

## Called by
- [`ms2_SpectralRedundancy`](./ms2_SpectralRedundancy.md)
- [`Features_ms2_SamplesAligment`](./Features_ms2_SamplesAligment.md)

## Examples
```python
import numpy as np
from Functions.ms2_SpectralSimilarityClustering import ms2_SpectralSimilarityClustering

SummMS2_raw = np.array([
    [7001, 300.123, 245.5, 1.0e5, 0.35, 0],
    [7002, 300.125, 246.0, 0.9e5, 0.30, 0],
    [7010, 450.200, 512.0, 1.5e5, 0.45, 0]
])
modules = ms2_SpectralSimilarityClustering(SummMS2_raw, SampleName='Sample_A', mz_col=1, RT_col=2,
                                           RT_tol=30, mz_Tol=5e-3, cos_tol=0.9)
print(modules)
```
For visualization, count cluster sizes:
```python
import matplotlib.pyplot as plt
sizes = [len(mod) for mod in modules]
plt.bar(range(len(sizes)), sizes)
plt.xlabel('Module index')
plt.ylabel('Size (spectra)')
plt.show()
```
