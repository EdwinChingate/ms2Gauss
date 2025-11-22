---
title: ms2Gauss Workflow User Guide
kind: guide
source: documentation/Workflow_UserGuide.md
last_updated: 2025-03-05
---

# End-to-End HRMS Workflow

This guide translates [`Description_HRMS_DataAnalisis.md`](../Description_HRMS_DataAnalisis.md) into actionable steps with parameter defaults so you can run the ms2Gauss pipeline from raw Orbitrap data to aligned features. Cross-links point to the function and table docs that implement each stage.

## Notebook prototypes that need completion

Several notebooks contain thin prototypes for functions that are conceptually described in the main workflow document but still need production-grade implementations:

- [`ChargeDataSet_in_AnotherFolder`](../Notebooks/feat.-ms2-Gauss.ipynb) loads mzML files from an external directory; it corresponds to the initial data-ingest step described alongside `AllMS2Data` and `All_ms2_spectra`.【F:Notebooks/feat.-ms2-Gauss.ipynb†L707-L774】【F:Description_HRMS_DataAnalisis.md†L3-L49】
- [`AllSubChromatograms`](../Notebooks/Chromatogram.ipynb) sketches chromatogram extraction for refining MS1 evidence around MS2 features; this aligns with the chromatogram refinement described for `RefineFeatureTable_withChromatogram` and `ExtractAllRawPeaks`.【F:Notebooks/Chromatogram.ipynb†L1057-L1095】【F:Description_HRMS_DataAnalisis.md†L151-L161】
- [`Joining_O2O_Features`](../Notebooks/Chromatogram.ipynb) and [`Features_O2O_SamplesAligment`](../Notebooks/Chromatogram.ipynb) prototype the per-sample feature stacking and cross-sample alignment noted for `Feature_ms2_SamplesAlignment`.【F:Notebooks/Chromatogram.ipynb†L3821-L3956】【F:Description_HRMS_DataAnalisis.md†L121-L131】

Treat these as starting points; they need to be hardened, migrated into `Functions/`, and wired into the documented workflow.

## Prerequisites

- Convert vendor RAW files to mzML (profile mode) with ProteoWizard `msconvert` and store them in a folder accessible to the notebooks or scripts.【F:Description_HRMS_DataAnalisis.md†L7-L49】
- Install Python dependencies used in the notebooks (e.g., `pyopenms`, `numpy`, `pandas`, `matplotlib`, `scipy`).
- Organize results folders as expected by the prototypes (`ms2_spectra/` for spectrum summaries, per-sample feature spreadsheets in a results directory).

## Step-by-step workflow

### 1) Load profile data

Use the loader to bring mzML data into memory:

```python
from Functions.AllMS2Data import AllMS2Data
from pyopenms import MSExperiment, MzMLFile

exp = MSExperiment()
MzMLFile().load("sample.mzML", exp)
SummMS2 = AllMS2Data(exp, min_RT=0, max_RT=1500, min_mz=100, max_mz=1200)
```

- Adjust RT/m/z windows to exclude acquisition noise or irrelevant precursors.【F:documentation/Functions/AllMS2Data.md†L12-L47】
- If mzML summaries already exist, `ms2_SpectralRedundancy` can be run on `ms2_spectra/*Summary.xlsx` files to rebuild `SummMS2` while collapsing redundant spectra.【F:documentation/Functions/ms2_SpectralRedundancy.md†L8-L64】

### 2) Clean individual MS2 spectra

For each MS2 spectrum referenced in `SummMS2`, extract fragment peaks:

```python
from Functions.ms2_spectrum import ms2_spectrum

frag_table = ms2_spectrum(raw_ms2_array, DataSetName="sample", ms_id=ms2_id,
                          LogFileName="logs/ms2_fit.log", mz_std=2e-3,
                          minQuality=100, minInt=1e2, minPeaks=2)
```

- Tune `minQuality`, `minSignals`, and `Points_for_regression` to balance sensitivity and fit robustness.【F:documentation/Functions/ms2_spectrum.md†L12-L69】
- The output fragment table feeds quality-controlled fragments into feature construction.

### 3) Build MS2-first feature seeds

Link MS2 events to nearby MS1 spectra and compute Gaussian descriptors:

```python
from Functions.ms2_features_stats import ms2_features_stats
from Functions.feat_ms2_Gauss import feat_ms2_Gauss

MS1IDVec, MS2_Features = feat_ms2_Gauss(SummMS2=SummMS2, DataSet=exp,
                                        mz_std=2e-3, RT_tol=20, mz_Tol=1e-2,
                                        minSignals=4, minQuality=100,
                                        min_peaks=2)
```

- `ms2_features_stats` selects the closest MS1 scan per MS2 event via [`closest_ms1_spec`](./Functions/closest_ms1_spec.md) and computes ppm confidence intervals.【F:documentation/Functions/ms2_features_stats.md†L8-L70】
- `feat_ms2_Gauss` aggregates those per-MS2 descriptors into the `MS2_Features` table, preserving umbrella RT bounds (`min_RT`, `max_RT`).【F:documentation/Functions/feat_ms2_Gauss.md†L8-L78】

### 4) Align features across samples

Stack per-sample feature spreadsheets and cluster them into consensus rows:

```python
from Functions.JoiningFeatures import JoiningFeatures
from Functions.Features_ms2_SamplesAligment import Features_ms2_SamplesAligment

All_FeaturesTable, sample_names = JoiningFeatures(results_folder="results")
AlignedDF, AlignedRT_DF = Features_ms2_SamplesAligment(
    All_FeaturesTable=All_FeaturesTable, SamplesNames=sample_names,
    RT_tol=20, mz_Tol=1e-2, min_Int_Frac=2, cos_tol=0.9,
    saveAlignedTable=True, name="SamplesAlignment")
```

- `Features_ms2_SamplesAligment` clusters features using m/z proximity, RT umbrellas, and MS2 spectral similarity to populate `AlignedSamplesDF` and `AlignedSamples_RT_DF`.【F:documentation/Functions/Features_ms2_SamplesAligment.md†L8-L83】
- Adjust `mz_Tol`/`RT_tol` to reflect instrument precision and chromatographic stability across your batch.【F:documentation/Variables/AlignedSamplesDF.md†L6-L35】

### 5) Experiment-specific filtering and chromatogram refinement

- Apply blank/control filters (e.g., `RemoveBlankFeatures`, `Samples_NFeatures_Filter`) to drop ubiquitous background signals, as described for the experimental comparison step.【F:Description_HRMS_DataAnalisis.md†L127-L149】
- Refine each aligned feature with high-resolution chromatograms using `RefineFeatureTable_withChromatogram` once the supporting chromatogram utilities (`ExtractAllRawPeaks`, `ResolveFullChromatogram`, `Match_ms2Feature_Chrom`) are finalized.【F:Description_HRMS_DataAnalisis.md†L151-L161】

### 6) Quick QC visualization

Plot aligned intensities to sanity-check umbrella grouping:

```python
import matplotlib.pyplot as plt
row = AlignedDF.iloc[0]
row.iloc[7:].plot(kind='bar')
plt.ylabel('Intensity (a.u.)')
plt.title(f"Feature at m/z {row['mz_(Da)']:.4f}")
plt.show()
```

This mirrors the alignment QC shown in the function docs and helps confirm that samples share coherent MS2-driven features.【F:documentation/Functions/Features_ms2_SamplesAligment.md†L84-L109】

## Plan to implement missing pieces

1. **Lift notebook prototypes into the `Functions/` package.** Wrap `ChargeDataSet_in_AnotherFolder`, `AllSubChromatograms`, `Joining_O2O_Features`, and `Features_O2O_SamplesAligment` as importable modules with parameter docstrings, input validation, and logging hooks consistent with existing function docs.【F:Notebooks/Chromatogram.ipynb†L1057-L1095】【F:Notebooks/Chromatogram.ipynb†L3821-L3956】【F:Notebooks/feat.-ms2-Gauss.ipynb†L707-L774】
2. **Complete chromatogram refinement.** Implement `ExtractAllRawPeaks`, `ResolveFullChromatogram`, and `Match_ms2Feature_Chrom` according to the deconvolution workflow (Gaussian mixtures via `scipy.optimize.curve_fit`) so `RefineFeatureTable_withChromatogram` becomes runnable.【F:Description_HRMS_DataAnalisis.md†L151-L161】
3. **Add alignment QA utilities.** Port the spectral-similarity checks from the prototypes into reusable helpers that plot cosine-similarity heatmaps and RT overlays for each feature cluster.
4. **Testing strategy.**
   - Create small synthetic mzML fixtures to exercise RT/mz filtering, MS2 redundancy collapse, and feature alignment with known ground truth.
   - Add unit tests for parameter edge cases (empty spectra, low-intensity fragments, overlapping umbrellas) and integration tests that execute the full pipeline on the fixtures.
   - Instrument notebooks to save intermediate tables (`SummMS2`, `MS2_Features`, `AlignedSamplesDF`) and compare against expected shapes/summary stats.

Following these steps will close the gaps between the descriptive workflow and the current prototype code so the pipeline can be executed reproducibly.
