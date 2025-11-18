---
title: Cosine_2VecSpec
kind: function
source: Functions/Cosine_2VecSpec.py
last_updated: 2025-02-14
---

## Description
Computes cosine similarity between two aligned MS2 spectra represented as column vectors. Used inside [`CosineMatrix`](./CosineMatrix.md).

## Code
```python
import numpy as np
def Cosine_2VecSpec(AlignedSpecMat):
    S1_dot_S2=np.sum(AlignedSpecMat[:,1]*AlignedSpecMat[:,2])
    S1_dot_S1=np.sum(AlignedSpecMat[:,1]*AlignedSpecMat[:,1])
    S2_dot_S2=np.sum(AlignedSpecMat[:,2]*AlignedSpecMat[:,2])
    dotXdot=S1_dot_S1*S2_dot_S2
    if dotXdot==0:
        return 0
    Cosine=S1_dot_S2/np.sqrt(dotXdot)
    return Cosine
```

## Key operations
- Computes dot products and normalizes to produce cosine similarity.
- Handles zero vectors by returning 0 to avoid division-by-zero.

## Parameters
- `AlignedSpecMat`: matrix with fragment m/z in column 0 and intensity vectors in columns 1–2.

## Output
- Cosine similarity scalar.

## Called by
- [`CosineMatrix`](./CosineMatrix.md)

## Example
```python
AlignedSpecMat = np.array([[100, 0.8, 0.7], [110, 0.2, 0.3]])
print(Cosine_2VecSpec(AlignedSpecMat))
```
