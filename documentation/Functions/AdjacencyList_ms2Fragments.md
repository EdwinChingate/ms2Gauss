---
title: AdjacencyList_ms2Fragments
kind: function
source: Functions/AdjacencyList_ms2Fragments.py
last_updated: 2025-02-14
---

## Description
Builds adjacency lists for aligned MS2 fragments. Two fragments are considered neighbors when their m/z windows overlap. The output guides fragment clustering prior to cosine similarity calculations.

## Code
```python
import numpy as np
def AdjacencyList_ms2Fragments(All_ms2):
    N_fragments=len(All_ms2[:,0])
    mzMaxVec=All_ms2[:,0]+All_ms2[:,5]
    mzMinVec=All_ms2[:,0]-All_ms2[:,5]
    AdjacencyList=[]
    frag_ids=[]
    for feat_id in np.arange(N_fragments):
        mz=All_ms2[feat_id,0]
        mz_CI=All_ms2[feat_id,5]
        min_mz=mz-mz_CI
        max_mz=mz+mz_CI
        NearFilter=(mzMaxVec>min_mz)&(mzMinVec<max_mz)
        Neigbours=np.where(NearFilter)[0]
        AdjacencyList.append(Neigbours)
        if len(Neigbours)>0:
            frag_ids.append(feat_id)
    frag_ids=set(frag_ids)
    return [AdjacencyList,frag_ids]
```

## Key operations
- Computes dynamic m/z bounds per fragment using column 5 (`mz_CI`).
- Marks neighbors when intervals overlap.

## Parameters
- `All_ms2`: array returned by [`Retrieve_and_Join_ms2_for_feature`](./Retrieve_and_Join_ms2_for_feature.md).

## Output
- `AdjacencyList`, `frag_ids`

## Called by
- [`ms2_FeaturesDifferences`](./ms2_FeaturesDifferences.md)

## Example
```python
AdjList, ids = AdjacencyList_ms2Fragments(All_ms2)
```
