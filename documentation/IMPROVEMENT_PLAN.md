---
title: ms2Gauss Improvement Plan
kind: meta
source: documentation/IMPROVEMENT_PLAN.md
last_updated: 2025-02-14
---

# Improvement Plan

Roadmap tracking conceptual refinements, computational efficiency, and missing building blocks.

## 1. Conceptual enhancements

1. **Explicit MS2-first rationale in docs.** Expand [`documentation/Functions/ms2_spectrum.md`](./Functions/ms2_spectrum.md) and [`documentation/Variables/SummMS2.md`](./Variables/SummMS2.md) with comparisons to MS1-first workflows and cite supporting references to strengthen scientific framing.
2. **Noise modeling and detection limits.** Introduce a documented parameter set (`NoiseThresholds` table) that records instrument-specific noise estimates for both MS1 and MS2 to rationalize `minSignals`, `minInt`, and `NoiseTresList` used in chromatogram modules.
3. **Experimental design filters.** Extend [`Features_ms2_SamplesAligment`](./Functions/Features_ms2_SamplesAligment.md) documentation with strategies for blank subtraction, replicate consistency, and isotopic labeling, referencing tables such as [`All_FeaturesTable`](./Variables/All_FeaturesTable.md).
4. **Uncertainty propagation to alignment.** Propagate ppm/RT confidence intervals into [`AlignedSamplesDF`](./Variables/AlignedSamplesDF.md) by averaging variances instead of simple means; document formulas in [`DEFINITIONS.md`](./DEFINITIONS.md).

## 2. Computational efficiency

1. **Vectorized redundancy filtering.** Replace Python loops inside [`ms2_SpectralRedundancy`](./Functions/ms2_SpectralRedundancy.md) with numpy/pandas group-bys to reduce runtime on large summary spreadsheets.
2. **Batch MS1 extraction.** Cache `closest_ms1_spec` results across features to avoid repeated searches through [`MS1IDVec`](./Variables/MS1IDVec.md) during [`feat_ms2_Gauss`](./Functions/feat_ms2_Gauss.md).
3. **Parallel Gaussian fits.** Use multiprocessing or joblib to run [`ms2_features_stats`](./Functions/ms2_features_stats.md) on feature batches, respecting reproducibility by seeding RNGs used in GA components.
4. **Sparse alignment storage.** When many samples are zero for a feature, store [`AlignedSamplesDF`](./Variables/AlignedSamplesDF.md) as a sparse matrix or parquet file to save disk space.

## 3. Missing or orphaned components

1. **`ms2_peakStats_safe` deep dive.** Create a full doc for [`ms2_peakStats_safe`](./Functions/ms2_peakStats_safe.md) describing how it stabilizes fragment peak estimation, since many upstream functions depend on it.
2. **Chromatographic GA tutorial.** Extract notebook logic into a `run_gaussian_chromatogram_fit` helper documented in `documentation/Functions/` so users can reproduce GA-based deconvolution without reading raw notebooks.
3. **Parameter tables.** Document CSV files controlling bounds (e.g., `ParametersTable.csv`, `MaxAtomicSubscripts.csv`) under `documentation/Variables/` to clarify chemical constraints.
4. **Reference integration.** Summaries of the 11 reference PDFs should be added to a future `documentation/REFERENCES.md`, linking each method to specific literature citations.

Track progress by checking off each bullet once the associated docs or code updates are merged.
