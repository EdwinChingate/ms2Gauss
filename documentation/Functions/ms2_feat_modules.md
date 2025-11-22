---
title: ms2_feat_modules
kind: function
source: Functions/ms2_feat_modules.py
last_updated: 2025-02-14
---

## Description
`ms2_feat_modules` converts an adjacency list (e.g., from [`AdjacencyListFeatures`](./AdjacencyListFeatures.md)) into connected components. It repeatedly selects an unvisited feature ID, performs graph traversal via [`AdjacencyClustering`](./AdjacencyClustering.md), and records the resulting module. The modules are used in redundancy removal and alignment.

## Code
```python
from AdjacencyClustering import *
def ms2_feat_modules(AdjacencyList,ms2_ids):
    Modules=[]
    while len(ms2_ids)>0:
        ms2_candidate_id=list(ms2_ids)[0]
        module=AdjacencyClustering(ms2_id=ms2_candidate_id,AdjacencyList=AdjacencyList)
        ms2_ids=ms2_ids-set(module)
        Modules.append(module)
    return Modules
```

## Key operations
- Maintains a set `ms2_ids` of unassigned vertices.
- Calls [`AdjacencyClustering`](./AdjacencyClustering.md) to retrieve all nodes connected to the candidate.
- Removes clustered IDs from `ms2_ids` and appends the module list.

## Parameters
- `AdjacencyList (list)`: neighbors per feature.
- `ms2_ids (set)`: indices that still require clustering.

## Input
- Output from [`AdjacencyListFeatures`](./AdjacencyListFeatures.md) or fragment adjacency lists.

## Output
- `Modules`: list of lists (feature indices belonging to the same connected component).

## Functions
- [`AdjacencyClustering`](./AdjacencyClustering.md)

## Called by
- [`Cluster_ms2_Features`](./Cluster_ms2_Features.md)
- [`ms2_SpectralSimilarityClustering`](./ms2_SpectralSimilarityClustering.md)
- [`ms2_FeaturesDifferences`](./ms2_FeaturesDifferences.md)

## Examples
```python
from Functions.ms2_feat_modules import ms2_feat_modules
AdjacencyList = [ [0,1], [0,1], [2] ]
modules = ms2_feat_modules(AdjacencyList, ms2_ids=set([0,1,2]))
print(modules)  # [[0,1], [2]]
```
Visualize module sizes:
```python
import matplotlib.pyplot as plt
sizes = [len(m) for m in modules]
plt.bar(range(len(sizes)), sizes)
plt.xlabel('Module index')
plt.ylabel('# features')
plt.show()
```
