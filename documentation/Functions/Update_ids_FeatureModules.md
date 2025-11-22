---
title: Update_ids_FeatureModules
kind: function
source: Functions/Update_ids_FeatureModules.py
last_updated: 2025-02-14
---

## Description
Maps module indices computed on temporary arrays back to the original feature indices. Essential when clustering operates on zero-based slices but alignment expects absolute row numbers.

## Code
```python
import numpy as np
def Update_ids_FeatureModules(Feature_module,Feature_Modules):
    npFeature_module=np.array(Feature_module)
    Modules=[]
    for module in Feature_Modules:
        feature_module=list(npFeature_module[module])
        Modules.append(feature_module)
    return Modules
```

## Parameters
- `Feature_module`: original list/array of feature IDs passed to the clustering stage.
- `Feature_Modules`: list of lists with indices relative to `Feature_module`.

## Output
- New list of modules expressed in original indices.

## Called by
- [`ms2_FeaturesDifferences`](./ms2_FeaturesDifferences.md)

## Example
```python
Feature_module = [10, 25, 30]
Feature_Modules = [[0,1],[2]]
print(Update_ids_FeatureModules(Feature_module, Feature_Modules))  # [[10,25],[30]]
```
