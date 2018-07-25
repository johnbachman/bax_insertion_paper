import numpy as np
from bax_insertion.util.calculate_error_variance import calc_err_var


def mod_zscore(residuals):
    numer = 0.6745 * (residuals - np.median(residuals))
    denom = np.median(np.abs(residuals - np.median(residuals)))
    return numer / denom


def filtered(x, zscores, cutoff):
    x_copy = np.copy(x)
    for i in range(0, len(zscores)):
        if np.abs(zscores[-i]) > cutoff:
            x_copy[-i] = np.nan
    return x_copy


def find_outliers(values):
    (res, fig) = calc_err_var(values, last_n_pts=len(values),
                              fit_type='two_exp_sum', plot=False)
    zscores = mod_zscore(res)
    return filtered(values, zscores, 3.5)

