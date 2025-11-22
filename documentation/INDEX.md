---
title: ms2Gauss Documentation Index
kind: meta
source: documentation/INDEX.md
last_updated: 2025-02-14
---

# Documentation Index

Overview of all documentation assets created during this iteration. Links follow the ms2Gauss workflow order.

## Workflow snapshot

```
Raw Orbitrap files → [AllMS2Data](./Functions/AllMS2Data.md)
                  → [ms2_SpectralRedundancy](./Functions/ms2_SpectralRedundancy.md)
                  → [SummMS2](./Variables/SummMS2.md)
                  → [ms2_features_stats](./Functions/ms2_features_stats.md)
                  → [feat_ms2_Gauss](./Functions/feat_ms2_Gauss.md)
                  → [MS2_Features](./Variables/MS2_Features.md)
                  → [Features_ms2_SamplesAligment](./Functions/Features_ms2_SamplesAligment.md)
                  → [AlignedSamplesDF](./Variables/AlignedSamplesDF.md)
```

## Functions

| Function | Summary |
| --- | --- |
| [AllMS2Data](./Functions/AllMS2Data.md) | Streams MS2 profile data and builds [`SummMS2`](./Variables/SummMS2.md) arrays by applying RT/m/z filters via [`mz_RT_spectrum_filter`](./Functions/mz_RT_spectrum_filter.md). |
| [ms2_spectrum](./Functions/ms2_spectrum.md) | Iteratively extracts Gaussian MS2 fragment peaks with [`ms2_peakStats_safe`](./Functions/ms2_peakStats_safe.md) and enforces quality thresholds. |
| [ms2_SpectralRedundancy](./Functions/ms2_SpectralRedundancy.md) | Clusters redundant MS2 detections per sample using cosine similarity. |
| [ms2_features_stats](./Functions/ms2_features_stats.md) | Links MS2 detections to MS1 chromatograms, fits Gaussian centroids, and computes ppm confidence intervals. |
| [feat_ms2_Gauss](./Functions/feat_ms2_Gauss.md) | Aggregates per-detection stats into a full [`MS2_Features`](./Variables/MS2_Features.md) table. |
| [Features_ms2_SamplesAligment](./Functions/Features_ms2_SamplesAligment.md) | Aligns MS2-derived features across samples, producing [`AlignedSamplesDF`](./Variables/AlignedSamplesDF.md) and [`AlignedSamples_RT_DF`](./Variables/AlignedSamples_RT_DF.md). |
| [mz_RT_spectrum_filter](./Functions/mz_RT_spectrum_filter.md) | **Stub.** Documents how MS2 profile arrays are filtered by RT/m/z windows. |
| [ms2_peakStats_safe](./Functions/ms2_peakStats_safe.md) | **Stub.** Describes fragment peak fitting safeguards used by [`ms2_spectrum`](./Functions/ms2_spectrum.md). |
| [closest_ms1_spec](./Functions/closest_ms1_spec.md) | **Stub.** Explains MS1 spectrum selection around an MS2 event. |
| [Normal_Fit](./Functions/Normal_Fit.md) | **Stub.** Captures Gaussian fitting of MS1 peak windows. |
| [Cluster_ms2_Features](./Functions/Cluster_ms2_Features.md) | **Stub.** Placeholder for clustering features across MS2 detections. |
| [ms2_SpectralSimilarityClustering](./Functions/ms2_SpectralSimilarityClustering.md) | **Stub.** Placeholder describing cosine-based MS2 clustering. |
| [JoiningFeatures](./Functions/JoiningFeatures.md) | **Stub.** Placeholder summarizing concatenation of per-sample feature tables. |

## Variables and tables

| Variable/Table | Summary |
| --- | --- |
| [DataSet](./Variables/DataSet.md) | Container of MS1 or MS2 spectra (list of numpy arrays). |
| [RawSpectrum](./Variables/RawSpectrum.md) | Individual MS2 spectrum array with `[m/z, intensity]` columns. |
| [SummMS2](./Variables/SummMS2.md) | Redundancy-resolved MS2 table with umbrellas and provenance. |
| [MS1IDVec](./Variables/MS1IDVec.md) | Mapping of MS1 scan indices to RT for linking MS2 events back to chromatograms. |
| [MS2_Features](./Variables/MS2_Features.md) | Gaussian-refined MS2 feature catalog with ppm CI columns. |
| [All_FeaturesTable](./Variables/All_FeaturesTable.md) | Stacked per-sample feature table used before alignment. |
| [AlignedSamplesDF](./Variables/AlignedSamplesDF.md) | Feature × sample intensity matrix with umbrella metadata. |
| [AlignedSamples_RT_DF](./Variables/AlignedSamples_RT_DF.md) | Same as `AlignedSamplesDF` but storing RT for each sample column. |

## Meta references

- [Glossary](./GLOSSARY.md)
- [Definitions](./DEFINITIONS.md)
- [Improvement plan](./IMPROVEMENT_PLAN.md)
- [Agents](./Agents.md)

Use this index to navigate the evolving book-style documentation.
