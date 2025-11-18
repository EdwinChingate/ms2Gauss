---
title: AligniningFragments_in_Feature
kind: function
source: Functions/AligniningFragments_in_Feature.py
last_updated: 2025-02-14
---

## Description
Aligns fragment modules into a matrix where rows represent aligned fragment groups and columns represent features within the module. Column 0 stores the fragment m/z, while subsequent columns store relative intensities for each feature. The matrix is used by [`CosineMatrix`](./CosineMatrix.md).

## Code
```python
import numpy as np
def AligniningFragments_in_Feature(Frag_Modules,All_ms2,N_features):
    N_Fragments=len(Frag_Modules)
    AlignedFragmentsMat=np.zeros((N_Fragments,N_features+1))
    for fragment_id in np.arange(N_Fragments,dtype='int'):
        Fragment_module=Frag_Modules[fragment_id]
        FragmentTable=All_ms2[Fragment_module,:]
        MaxInt=np.max(FragmentTable[:,2])
        MaxInt_Loc=np.where(FragmentTable[:,2]==MaxInt)[0]
        AlignedFragmentsMat[fragment_id,0]=FragmentTable[MaxInt_Loc,0]
        Fragments_ids=np.array(FragmentTable[:,10],dtype='int')
        AlignedFragmentsMat_loc=Fragments_ids+1
        AlignedFragmentsMat[fragment_id,AlignedFragmentsMat_loc]=FragmentTable[:,9]
    AlignedFragmentsMat=AlignedFragmentsMat[AlignedFragmentsMat[:,0].argsort()]
    return AlignedFragmentsMat
```

## Key operations
- For each fragment module, finds the m/z of the most intense instance and stores it in column 0.
- Places relative intensities (column 9 of `All_ms2`) into feature-specific columns using the stored feature IDs (column 10).
- Sorts rows by m/z to ease visualization.

## Parameters
- `Frag_Modules`: list of fragment index arrays from [`ms2_feat_modules`](./ms2_feat_modules.md).
- `All_ms2`: concatenated fragment array.
- `N_features`: number of features being compared.

## Output
- `AlignedFragmentsMat`: matrix consumed by [`CosineMatrix`](./CosineMatrix.md).

## Called by
- [`ms2_FeaturesDifferences`](./ms2_FeaturesDifferences.md)

## Example
```python
AlignedFragmentsMat = AligniningFragments_in_Feature(Frag_Modules, All_ms2, N_features=len(Feature_module))
```
