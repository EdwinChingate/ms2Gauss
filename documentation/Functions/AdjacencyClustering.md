---
title: AdjacencyClustering
kind: function
source: Functions/AdjacencyClustering.py
last_updated: 2025-02-14
---

## Description
`AdjacencyClustering` performs a depth-first traversal of an adjacency list to collect all vertices reachable from a seed feature. It underpins module formation in [`ms2_feat_modules`](./ms2_feat_modules.md).

## Code
```python
import numpy as np
def AdjacencyClustering(ms2_id,AdjacencyList,Module=[]):
    CurrentModule=set(AdjacencyList[ms2_id])
    CurrentModule=CurrentModule-set(Module)
    Module=Module+list(CurrentModule)
    for ms2_id in CurrentModule:
        Module=AdjacencyClustering(ms2_id=ms2_id,AdjacencyList=AdjacencyList,Module=Module)
    return Module
```

## Key operations
- Recursively visits neighbors, ensuring each node is processed once.
- Accumulates nodes into `Module` and returns the complete connected component.

## Parameters
- `ms2_id (int)`: starting vertex.
- `AdjacencyList (list)`: neighbors per feature.
- `Module (list)`: accumulator (default empty).

## Input
- Called internally by [`ms2_feat_modules`](./ms2_feat_modules.md).

## Output
- List of indices belonging to the connected component.

## Functions
- Uses recursion only.

## Called by
- [`ms2_feat_modules`](./ms2_feat_modules.md)

## Examples
```python
AdjacencyList = [[0,1], [0,1], [2]]
from Functions.AdjacencyClustering import AdjacencyClustering
module = AdjacencyClustering(0, AdjacencyList, Module=[0])
print(module)
```
