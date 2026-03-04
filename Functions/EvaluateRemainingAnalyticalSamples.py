from __future__ import annotations
from ContrastSamplesCentroids import *
from FeatureClusterCentroids import *
from FillAlignedFragmentsSamplesSpectraMat import *
from Retrieve_ms2_afterSampling import *

def EvaluateRemainingAnalyticalSamples(Samples_FeaturesIdsList,
                                       Samples_ids2Check,
                                       feature_cluster_data,
                                       All_FeaturesTable,
                                       SamplesNames,
                                       BigFeature_Module,
                                       IntramoduleSimilarityModulesMat,
                                       sample_id_col = 6,
                                       ms2_spec_id_col = 0,
                                       ms2Folder = 'ms2_spectra',
                                       ToAdd = 'mzML',
                                       Norm2One = False,
                                       Nspectra_sampling = 3,
                                       std_distance = 3,
                                       ppm_tol = 20):

    Modules, Feature_Module, IntramoduleSimilarity, _, AlignedFragmentsMat, AlignedFragments_mz_Mat = feature_cluster_data
    N_modules = len(Modules)

    # Track which spectra have already been evaluated per sample
    # {sample_id: set of spectrum indices already evaluated}
    EvaluatedSpectraPerSample = {sample_id: set() 
                                 for sample_id in Samples_ids2Check}

    # Track confirmation status per sample per module
    # {sample_id: set of module_ids already confirmed (present or absent)}
    ConfirmedModulesPerSample = {sample_id: set() 
                                 for sample_id in Samples_ids2Check}

    # Track remaining spectra pool per sample (shrinks as spectra are evaluated)
    RemainingSpectraPerSample = {sample_id: list(Samples_FeaturesIdsList[sample_id])
                                 for sample_id in Samples_ids2Check}

    CentroidsAlignedFragmentsMat = FeatureClusterCentroids(
                                       feature_cluster_data = feature_cluster_data)

    while len(Samples_ids2Check) > 0:

        # Sample a few spectra from each remaining sample
        SamplesSamplesList, All_ms2 = Retrieve_ms2_afterSampling(Samples_FeaturesIdsList = RemainingSpectraPerSample,
                                                                 Samples_ids2Check = Samples_ids2Check,
                                                                 All_FeaturesTable = All_FeaturesTable,
                                                                 SamplesNames = SamplesNames,
                                                                 sample_id_col = sample_id_col,
                                                                 ms2_spec_id_col = ms2_spec_id_col,
                                                                 ms2Folder = ms2Folder,
                                                                 ToAdd = ToAdd,
                                                                 Norm2One = Norm2One,
                                                                 Nspectra_sampling = Nspectra_sampling)

        if len(All_ms2) == 0:
            continue

        AlignedFragmentsSamplesSpectraMat, AlignedFragmentsSamplesSpectra_mz_Mat = \
            FillAlignedFragmentsSamplesSpectraMat(
                AlignedFragmentsMat = AlignedFragmentsMat,
                AlignedFragments_mz_Mat = AlignedFragments_mz_Mat,
                All_ms2 = All_ms2,
                SamplesSamplesList = SamplesSamplesList,
                std_distance = std_distance,
                ppm_tol = ppm_tol)

        CosineToCentroids = ContrastSamplesCentroids(AlignedFragmentsSamplesSpectraMat = AlignedFragmentsSamplesSpectraMat,
                                                     CentroidsAlignedFragmentsMat = CentroidsAlignedFragmentsMat,
                                                     N_modules = N_modules)

        #  Update confirmed modules and modules lists 
        for spectrum_idx, true_spectrum_id in enumerate(SamplesSamplesList):

            # Identify which sample this spectrum belongs to
            sample_id = int(All_FeaturesTable[true_spectrum_id, sample_id_col])

            # Mark this spectrum as evaluated for this sample
            EvaluatedSpectraPerSample[sample_id].add(true_spectrum_id)

            # Remove from remaining pool so it won't be sampled again
            if true_spectrum_id in RemainingSpectraPerSample[sample_id]:
                RemainingSpectraPerSample[sample_id].remove(true_spectrum_id)

            for module_id in np.arange(N_modules):

                # Skip modules already confirmed for this sample
                if module_id in ConfirmedModulesPerSample[sample_id]:
                    continue

                best_cosine = CosineToCentroids[spectrum_idx, module_id]
                module_threshold = IntramoduleSimilarityModulesMat[module_id, 1]

                if best_cosine >= module_threshold:
                    # POSITIVE CONFIRMATION: one spectrum is enough
                    Modules[module_id].append(true_spectrum_id)
                    if true_spectrum_id not in BigFeature_Module:
                        BigFeature_Module.append(true_spectrum_id)
                    # Mark this module as confirmed for this sample
                    ConfirmedModulesPerSample[sample_id].add(module_id)

        #  Update Samples_ids2Check 
        # Remove a sample from the list when:
        # Option A: all modules confirmed (positive or negative) for this sample
        # Option B: no spectra left to evaluate for this sample
        Samples_ids_to_remove = []
        for sample_id in Samples_ids2Check:
            AllModulesResolved = len(ConfirmedModulesPerSample[sample_id]) == N_modules
            NoSpectraLeft = len(RemainingSpectraPerSample[sample_id]) == 0
            if AllModulesResolved or NoSpectraLeft:
                Samples_ids_to_remove.append(sample_id)

        for sample_id in Samples_ids_to_remove:
            print(sample_id)
            Samples_ids2Check.remove(sample_id)

        # Also update RemainingSpectraPerSample to exclude
        # already-confirmed modules from future sampling
        # to avoid wasting evaluations on confirmed samples
        for sample_id in Samples_ids2Check:
            confirmed_modules = ConfirmedModulesPerSample[sample_id]
            if len(confirmed_modules) > 0:
                # Only keep spectra needed for unconfirmed modules
                # (all remaining spectra are still valid candidates)
                pass  # RemainingSpectraPerSample already shrinks naturally

    feature_cluster_data = [Modules,
                            BigFeature_Module,
                            IntramoduleSimilarityModulesMat,
                            All_FeaturesTable,
                            AlignedFragmentsMat,
                            AlignedFragments_mz_Mat]

    return feature_cluster_data