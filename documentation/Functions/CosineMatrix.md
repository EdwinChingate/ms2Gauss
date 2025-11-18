---
title: CosineMatrix
kind: function
source: Functions/CosineMatrix.py
last_updated: 2025-02-14
---

## Description
`CosineMatrix` computes pairwise cosine similarities between aligned fragment intensity vectors. It iterates over feature pairs, extracts the relevant columns from `AlignedFragmentsMat`, and delegates the computation to [`Cosine_2VecSpec`](./Cosine_2VecSpec.md).

## Code
```python
import numpy as np
from Cosine_2VecSpec import *
def CosineMatrix(AlignedFragmentsMat,N_features):
    CosineMat=np.zeros((N_features,N_features))
    for feature_id1 in np.arange(N_features,dtype='int'):
        for feature_id2 in np.arange(feature_id1,N_features,dtype='int'):
            AlignedSpecMat=AlignedFragmentsMat[:,[0,feature_id1+1,feature_id2+1]]
            Cosine=Cosine_2VecSpec(AlignedSpecMat=AlignedSpecMat)
            CosineMat[feature_id1,feature_id2]=Cosine
            CosineMat[feature_id2,feature_id1]=Cosine
    return CosineMat
```

## Key operations
- Builds symmetric cosine matrix by reusing computed values.
- `AlignedSpecMat` stores fragment m/z plus two intensity columns, which [`Cosine_2VecSpec`](./Cosine_2VecSpec.md) interprets as aligned spectra.

## Parameters
- `AlignedFragmentsMat`: output from [`AligniningFragments_in_Feature`](./AligniningFragments_in_Feature.md).
- `N_features`: number of aligned features.

## Output
- `CosineMat`: NxN similarity matrix.

## Called by
- [`ms2_FeaturesDifferences`](./ms2_FeaturesDifferences.md)

## Example
```python
CosineMat = CosineMatrix(AlignedFragmentsMat, N_features)
```
