import os
from pyopenms import *
def ChargeDataSet_in_AnotherFolder(DataSetName, DataFolder):
    DataSet = MSExperiment()
    MzMLFile().load(DataFolder + '/' + DataSetName, DataSet)
    return DataSet
