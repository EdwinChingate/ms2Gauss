---
title: ms2Gauss Theoretical Definitions
kind: meta
source: documentation/DEFINITIONS.md
last_updated: 2025-02-14
---

# ms2Gauss Theory and Data Structures

This chapter consolidates the physics, statistics, and data structures that appear across ms2Gauss documentation. Use it together with the [Glossary](./GLOSSARY.md) and individual function/variable pages.

## Orbitrap signal formation

Orbitrap instruments capture ion image currents and resolve them via Fourier transform. The resulting profile spectra have ppm-level mass accuracy, enabling Gaussian modeling of each peak. Functions such as [`AllMS2Data`](./Functions/AllMS2Data.md) and [`ms2_spectrum`](./Functions/ms2_spectrum.md) assume profile-mode arrays with columns `[m/z, intensity]`.

## Gaussian peak model {#gaussian-peak}

ms2Gauss represents both MS1 and MS2 peaks as normal distributions parameterized by centroid \(\mu\), standard deviation \(\sigma\), and total integrated intensity \(I_{\text{total}}\):
\[
I(m/z) = \frac{I_{\text{total}}}{\sigma\sqrt{2\pi}} \exp\left[-\frac{(m/z-\mu)^2}{2\sigma^2}\right]
\]
[`GaussianPeak`](./Functions/GaussianPeak.md) implements this expression. Curve fitting performed in [`Normal_Fit`](./Functions/Normal_Fit.md) refines \(\mu\) and \(\sigma\) for MS1 peaks associated with MS2 features.

## Confidence intervals and ppm error

[`ms2_features_stats`](./Functions/ms2_features_stats.md) propagates uncertainty using Student’s t-distribution:
\[
\text{CI}_{\text{Da}} = t_{1-\alpha,\,N-1} \frac{\sigma}{\sqrt{N}}, \quad
\text{CI}_{\text{ppm}} = 10^6 \frac{\text{CI}_{\text{Da}}}{m/z}
\]
These columns appear in [`MS2_Features`](./Variables/MS2_Features.md) and downstream alignment tables.

## Spectral redundancy {#spectral-redundancy}

Multiple MS2 scans may target the same precursor. [`ms2_SpectralRedundancy`](./Functions/ms2_SpectralRedundancy.md) reads summary spreadsheets, filters them by RT/m/z, and clusters spectra via cosine similarity from [`ms2_SpectralSimilarityClustering`](./Functions/ms2_SpectralSimilarityClustering.md). Cluster statistics (min/max RT, number of spectra, representative spectrum ID) populate [`SummMS2`](./Variables/SummMS2.md).

## MS2-first feature construction

1. [`AllMS2Data`](./Functions/AllMS2Data.md) extracts MS2 detections into `SummMS2` when only raw profile data are available.
2. [`ms2_spectrum`](./Functions/ms2_spectrum.md) builds clean fragment lists from raw spectra using [`ms2_peakStats_safe`](./Functions/ms2_peakStats_safe.md).
3. [`ms2_features_stats`](./Functions/ms2_features_stats.md) links each MS2 detection to MS1 chromatograms via [`closest_ms1_spec`](./Functions/closest_ms1_spec.md) and Gaussian fits.
4. [`feat_ms2_Gauss`](./Functions/feat_ms2_Gauss.md) aggregates these per-MS2 fits into [`MS2_Features`](./Variables/MS2_Features.md).
5. [`Features_ms2_SamplesAligment`](./Functions/Features_ms2_SamplesAligment.md) merges per-sample feature tables into [`AlignedSamplesDF`](./Variables/AlignedSamplesDF.md).

## Chromatographic umbrellas and alignment

Chromatographic umbrellas are defined by `min_RT`/`max_RT` windows in `SummMS2` and copied to `MS2_Features`. During alignment, these umbrellas anchor sample-specific intensities and retention times in `[AlignedSamplesDF, AlignedSamples_RT_DF]`. Tolerances `RT_tol` and `mz_Tol` govern clustering decisions.

## Genetic algorithms for chromatograms

Several modules (e.g., `ResolvingChromatogram`, `MutateParameters`, `EvaluatePopulation`) use genetic algorithms to deconvolve overlapping Gaussian RT profiles. Populations encode sets of Gaussian parameters; crossover/mutation operations explore parameter space; fitness evaluates r² or residual error against experimental chromatograms. While not fully documented here, these functions inherit the Gaussian model defined above.

## Data tables

- [`SummMS2`](./Variables/SummMS2.md): per-cluster MS2 metadata (centroid m/z, RT, MS2 IDs, umbrella bounds).
- [`MS2_Features`](./Variables/MS2_Features.md): MS1-refined precursor statistics tied to MS2 provenance.
- [`AlignedSamplesDF`](./Variables/AlignedSamplesDF.md): feature-by-sample matrix storing aligned intensities and umbrella metadata.
- [`AlignedSamples_RT_DF`](./Variables/AlignedSamples_RT_DF.md): same layout but retaining RT for each sample slot.
- [`All_FeaturesTable`](./Variables/All_FeaturesTable.md): concatenation of per-sample feature tables before alignment.

## Similarity measures

Cosine similarity for fragment vectors \(\vec{a}, \vec{b}\):
\[
\cos(\theta) = \frac{\vec{a}\cdot\vec{b}}{\|\vec{a}\|\,\|\vec{b}\|}
\]
Used in `ms2_SpectralSimilarityClustering` to create adjacency matrices. Alternative metrics (Tanimoto) appear in other clustering modules.

## References

Concepts summarized here draw from the ms2Gauss draft (references/draft.pdf) and Orbitrap-focused MS2 feature modeling literature such as Hu et al., Anal. Chem. (2020) on MS2-first workflows.
