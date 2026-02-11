from scipy import stats
def ttest(Nsignals,
          alpha = 0.01):
    tref = stats.t.interval(1 - alpha,
                            Nsignals - 1)[1]    
    return tref
