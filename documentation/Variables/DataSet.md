---
title: DataSet
kind: variable
source: Variables/DataSet
last_updated: 2025-02-14
---

## Description
`DataSet` is the iterable of Orbitrap spectra (MS1 or MS2) loaded from vendor files. Each element exposes `getMSLevel()`, `getRT()`, and `get_peaks()` so functions such as [`AllMS2Data`](../Functions/AllMS2Data.md) and [`ms2_features_stats`](../Functions/ms2_features_stats.md) can access intensities, retention times, and precursor metadata. Scientifically, it represents the raw experimental evidence before Gaussian modeling.

## Code
```python
# Example DataSet composed of simplified spectrum objects
class MockSpectrum:
    def __init__(self, level, rt, peaks, precursor_mz=None):
        self._level = level
        self._rt = rt
        self._peaks = peaks
        self._precursor_mz = precursor_mz
    def getMSLevel(self):
        return self._level
    def getRT(self):
        return self._rt
    def get_peaks(self):
        return self._peaks
    def getPrecursors(self):
        return [type('P', (), {'getMZ': lambda self: self})(self._precursor_mz)]

DataSet = [
    MockSpectrum(2, 145.2, peaks=[[300.12, 5e4], [300.14, 2e4]], precursor_mz=300.13),
    MockSpectrum(1, 145.4, peaks=[[300.11, 1.5e5], [300.13, 9e4]])
]
```

## Key operations
- Iterated by [`AllMS2Data`](../Functions/AllMS2Data.md) to stream every spectrum and build [`SummMS2`](./SummMS2.md).
- Accessed indirectly through [`MS1IDVec`](./MS1IDVec.md) and [`closest_ms1_spec`](../Functions/closest_ms1_spec.md) when MS1 scans are needed for chromatographic refinement.
- Serves as the source for extracting raw peaks (`get_peaks()`), precursor metadata (`getPrecursors()`), and retention time stamps.

## Parameters
- `level (int)`: 1 for MS1 chromatograms, 2 for MS2 spectra.
- `rt (float, seconds)`: chromatographic time of the scan.
- `peaks (array-like)`: Nx2 array `[m/z, intensity]` representing the profile data.
- `precursor_mz (float, Da)`: available for MS2 scans and used to filter by m/z.

## Input
- Consumed directly by [`AllMS2Data`](../Functions/AllMS2Data.md) and [`ms2_features_stats`](../Functions/ms2_features_stats.md) to obtain spectral information.

## Output
- Not produced directly; functions output tables such as [`SummMS2`](./SummMS2.md) or [`MS2_Features`](./MS2_Features.md).

## Functions
- [`AllMS2Data`](../Functions/AllMS2Data.md) iterates through the spectra to compile MS2 summaries.
- [`ms2_features_stats`](../Functions/ms2_features_stats.md) extracts MS1 peak windows using `DataSet` indices stored in [`MS1IDVec`](./MS1IDVec.md).

## Called by
- Any workflow entry point that loads raw data (e.g., notebooks calling `MS_L_IDs` or `feat_ms2_Gauss`).

## Example table

| spectrum_id | MS level | RT (s) | precursor_mz (Da) | N peaks |
| --- | --- | --- | --- | --- |
| 1024 | 2 | 145.2 | 300.13 | 2 |
| 1025 | 1 | 145.4 | – | 2 |

Each row summarizes an element of `DataSet`, emphasizing the metadata needed downstream.
