def UpdateUniqueModulesAfterClustering(New_Modules,
                                       Modules):
    UpdatedModules = []
    for new_module in New_Modules:
        updatedModule = []
        for module in new_module:
            updatedModule += Modules[module]
        updatedModule = list(set(updatedModule))
        UpdatedModules.append(updatedModule)
    return UpdatedModules
