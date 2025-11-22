---
title: ms2Gauss Glossary
kind: meta
source: documentation/GLOSSARY.md
last_updated: 2025-02-14
---

# Glossary

Short definitions for recurring scientific and computational terms in ms2Gauss. Each entry links to deeper theory in [`DEFINITIONS.md`](./DEFINITIONS.md) or to the relevant function/variable docs.

## m/z
Mass-to-charge ratio of ions detected in Orbitrap spectra. It sets the horizontal axis for both MS1 and MS2 data and is modeled with Gaussian distributions to capture high-resolution peak shapes.

## Orbitrap
A Fourier-transform mass analyzer that measures ion oscillations as image currents. ms2Gauss assumes Orbitrap-level resolving power when setting Gaussian widths and ppm-level confidence intervals.

## MS1
Survey (precursor) scans containing intact ions. ms2Gauss uses MS1 chromatograms to refine MS2-derived features through [`ms2_features_stats`](./Functions/ms2_features_stats.md) and [`feat_ms2_Gauss`](./Functions/feat_ms2_Gauss.md).

## MS2
Fragmentation scans acquired after MS1. They anchor the workflow: peaks are first selected from MS2 summaries via [`AllMS2Data`](./Functions/AllMS2Data.md) and [`ms2_SpectralRedundancy`](./Functions/ms2_SpectralRedundancy.md) before MS1 refinement occurs.

## Retention time (RT)
Chromatographic elution time in seconds. RT windows bound chromatographic umbrellas and appear in tables such as [`SummMS2`](./Variables/SummMS2.md) and [`AlignedSamplesDF`](./Variables/AlignedSamplesDF.md).

## Spectral redundancy
Multiple MS2 spectra acquired for the same precursor. It is mitigated with cosine similarity clustering in [`ms2_SpectralRedundancy`](./Functions/ms2_SpectralRedundancy.md).

## Gaussian peak
A model of ion intensity as a normal distribution over m/z or RT:
\[
I(\text{axis}) = \frac{I_{\text{total}}}{\sigma\sqrt{2\pi}} \exp\left( -\frac{(x-\mu)^2}{2\sigma^2} \right)
\]
Implemented in [`GaussianPeak`](./Functions/GaussianPeak.md) and used throughout MS1/MS2 fits.

## ppm (parts per million)
Unit for mass error: \(\text{ppm} = 10^6 (m_{\text{measured}}-m_{\text{true}})/m_{\text{true}}\). Confidence intervals in [`MS2_Features`](./Variables/MS2_Features.md) are reported in ppm.

## Cosine similarity
Similarity metric for MS2 fragment vectors. Used inside [`ms2_SpectralSimilarityClustering`](./Functions/ms2_SpectralSimilarityClustering.md) to build redundancy modules.

## Chromatographic umbrella
RT window covering all detections for a feature. Derived from `min_RT`/`max_RT` columns in [`SummMS2`](./Variables/SummMS2.md) and propagated to [`AlignedSamplesDF`](./Variables/AlignedSamplesDF.md).

## Feature module
Cluster of spectra/features representing the same compound across samples. Created by [`Cluster_ms2_Features`](./Functions/Cluster_ms2_Features.md) or [`ms2_SpectralSimilarityClustering`](./Functions/ms2_SpectralSimilarityClustering.md).

## Genetic algorithm (GA)
Evolutionary strategy used in ms2Gauss for chromatogram deconvolution and parameter fitting. Populations, mutation rates, and fitness functions live in `Functions/` but share the Gaussian modeling assumptions summarized in [`DEFINITIONS.md`](./DEFINITIONS.md#genetic-algorithms-for-chromatograms).

## Alignment matrix
Table aligning MS2-derived features across samples, e.g., [`AlignedSamplesDF`](./Variables/AlignedSamplesDF.md) and [`AlignedSamples_RT_DF`](./Variables/AlignedSamples_RT_DF.md).

## Confidence interval (CI)
Statistical range estimated for m/z (Da and ppm) via Student’s t-distribution as shown in [`ms2_features_stats`](./Functions/ms2_features_stats.md).

## SummMS2
MS2 summary table after redundancy resolution. Described in detail in [`SummMS2`](./Variables/SummMS2.md).

## MS2_Features
Gaussian-refined feature table produced by [`feat_ms2_Gauss`](./Functions/feat_ms2_Gauss.md). Columns include fitted m/z, RT, intensities, uncertainties, and provenance metadata.

## Alignment tolerance
Pair of parameters (`mz_Tol`, `RT_tol`) controlling how features are grouped. Tuned in [`Features_ms2_SamplesAligment`](./Functions/Features_ms2_SamplesAligment.md).

Use this glossary whenever a documentation page references foundational terminology.
