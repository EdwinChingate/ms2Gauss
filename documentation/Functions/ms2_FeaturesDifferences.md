---
title: ms2_FeaturesDifferences
kind: function
source: Functions/ms2_FeaturesDifferences.py
last_updated: 2025-02-14
---

## Description
`ms2_FeaturesDifferences` refines feature clusters by comparing full MS2 spectra. Starting from an initial set of candidate indices (e.g., from [`ms2_SpectralSimilarityClustering`](./ms2_SpectralSimilarityClustering.md)), it reloads the raw MS2 spectra, aligns fragments, computes cosine similarities, and splits clusters when spectra diverge beyond `cos_tol`. The output modules feed alignment routines.

## Code
```python
from Retrieve_and_Join_ms2_for_feature import *
from AdjacencyList_ms2Fragments import *
from ms2_feat_modules import *
from AligniningFragments_in_Feature import *
from CosineMatrix import *
from AdjacencyList_from_matrix import *
from ms2_feat_modules import *
from Update_ids_FeatureModules import *
def ms2_FeaturesDifferences(All_FeaturesTable,Feature_module,SamplesNames,sample_id_col=16,ms2_spec_id_col=15,ms2Folder='ms2_spectra',ToAdd='mzML',min_Int_Frac=2,cos_tol=0.9):
    All_ms2=Retrieve_and_Join_ms2_for_feature(All_FeaturesTable=All_FeaturesTable,Feature_module=Feature_module,SamplesNames=SamplesNames,sample_id_col=sample_id_col,ms2_spec_id_col=ms2_spec_id_col,ms2Folder=ms2Folder,ToAdd=ToAdd,min_Int_Frac=min_Int_Frac)
    if len(All_ms2)==0:
        return []
    AdjacencyListFragments,feat_ids=AdjacencyList_ms2Fragments(All_ms2=All_ms2)
    N_features=len(Feature_module)
    Frag_Modules=ms2_feat_modules(AdjacencyList=AdjacencyListFragments,ms2_ids=feat_ids)
    AlignedFragmentsMat=AligniningFragments_in_Feature(Frag_Modules=Frag_Modules,All_ms2=All_ms2,N_features=N_features)
    CosineMat=CosineMatrix(AlignedFragmentsMat=AlignedFragmentsMat,N_features=N_features)
    AdjacencyList_Features,features_ids=AdjacencyList_from_matrix(AdjacencyMatrix=CosineMat,N_ms2_spectra=N_features,minAdjacency=cos_tol)
    Feature_Modules=ms2_feat_modules(AdjacencyList=AdjacencyList_Features,ms2_ids=features_ids)
    Feature_Modules=Update_ids_FeatureModules(Feature_module=Feature_module,Feature_Modules=Feature_Modules)
    return Feature_Modules
```

## Key operations
- Uses [`Retrieve_and_Join_ms2_for_feature`](./Retrieve_and_Join_ms2_for_feature.md) to load every MS2 spectrum for the candidate module.
- Builds fragment-level adjacency lists and modules, then aligns fragments with [`AligniningFragments_in_Feature`](./AligniningFragments_in_Feature.md).
- Computes cosine similarity matrix via [`CosineMatrix`](./CosineMatrix.md) and thresholds it using [`AdjacencyList_from_matrix`](./AdjacencyList_from_matrix.md).
- Runs [`ms2_feat_modules`](./ms2_feat_modules.md) again on the similarity graph and re-maps indices to the original feature IDs with [`Update_ids_FeatureModules`](./Update_ids_FeatureModules.md).

## Parameters
- `All_FeaturesTable`: stacked feature rows from [`JoiningFeatures`](./JoiningFeatures.md).
- `Feature_module (array-like)`: indices representing one coarse cluster.
- `SamplesNames (list)`: used to build file paths when reading spectra.
- `sample_id_col`, `ms2_spec_id_col`: columns in `All_FeaturesTable` storing sample IDs and raw MS2 IDs.
- `ms2Folder`, `ToAdd`: file-system hints for locating mzML spectra.
- `min_Int_Frac`: minimum fragment intensity fraction kept during alignment.
- `cos_tol`: cosine similarity threshold for splitting clusters.

## Input
- [`All_FeaturesTable`](../Variables/All_FeaturesTable.md)
- Candidate module indices from `ms2_SpectralSimilarityClustering`.

## Output
- `Feature_Modules`: list of refined modules (arrays of row indices) ready for alignment.

## Functions
- [`Retrieve_and_Join_ms2_for_feature`](./Retrieve_and_Join_ms2_for_feature.md)
- [`AdjacencyList_ms2Fragments`](./AdjacencyList_ms2Fragments.md)
- [`ms2_feat_modules`](./ms2_feat_modules.md)
- [`AligniningFragments_in_Feature`](./AligniningFragments_in_Feature.md)
- [`CosineMatrix`](./CosineMatrix.md)
- [`AdjacencyList_from_matrix`](./AdjacencyList_from_matrix.md)
- [`Update_ids_FeatureModules`](./Update_ids_FeatureModules.md)

## Called by
- [`ms2_SpectralSimilarityClustering`](./ms2_SpectralSimilarityClustering.md)

## Examples
```python
from Functions.ms2_FeaturesDifferences import ms2_FeaturesDifferences
modules = ms2_FeaturesDifferences(All_FeaturesTable, Feature_module=[0,1,2],
                                  SamplesNames=['Sample_A','Sample_B'],
                                  cos_tol=0.95)
```
Visualize cosine similarity matrix (mock data):
```python
import matplotlib.pyplot as plt
import numpy as np
cosine_mat = np.random.rand(3,3)
plt.imshow(cosine_mat, vmin=0, vmax=1, cmap='viridis')
plt.colorbar(label='cosine similarity')
plt.title('Fragment similarity heatmap')
plt.show()
```
