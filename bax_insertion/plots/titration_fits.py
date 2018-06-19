"""
This module contains code to fit data to a variety of mathematical functions.

Most fitting code is implemented in the superclass :py:class:`TitrationFit`;
specific mathematical functions are implemented in the various subclasses.  The
subclasses implement the specific mathematical function as a static method, and
also specify the number of parameters in the model, the names of the
parameters, and their initial values.
"""

import numpy as np
from matplotlib import pyplot as plt
from bax_insertion.util import fitting


class TitrationFit(object):
    """Superclass for fitting kinetic titrations using mathematical functions.

    Implementing subclasses must implement a ``@staticmethod`` called
    ``fit_func`` that takes the time vector and a list (or array) of parameter
    values.

    In addition, subclasses should implement an ``__init__`` method that calls
    the superclass ``__init__`` with a list of parameter names and initial
    guesses for the parameter values, in an order corresponding the parameters
    used in ``fit_func``.

    Parameters
    ----------
    param_names : list of strings
        List of strings giving human-readable names for the parameters used
        in the model. The order of the names should correspond to the order
        of the initial guesses.
    initial_guesses : list of numbers
        Values to be used as the starting guesses for fitting.
    log_transform : boolean
        Whether to log-transform the parameters during fitting. If
        log-transformed, negative parameter values are not permissible.

    Attributes
    ----------
    k_arr : numpy.array
        Array containing the fitted parameters. The array has shape
        (num_params, num_concentrations), i.e., there is a
        set of parameters from every fitted timecourse.
    num_params : int
        The number of parameters in the function used for fitting.
    initial_guesses : list
        Initial values used for fitting.
    """
    def __init__(self, param_names, initial_guesses, log_transform=True):
        if initial_guesses is None or len(initial_guesses) == 0:
            raise ValueError('initial_guesses cannot be None or empty.')
        if len(param_names) != len(initial_guesses):
            raise ValueError('There must be the same number of parameter names '
                             'and initial guesses.')

        self.param_names = param_names
        self.k_arr = None
        self.num_params = len(initial_guesses)
        self.initial_guesses = initial_guesses
        self.log_transform = log_transform

    def fit_timecourse(self, time, y):
        """Fit a single timecourse with the desired function.

        Parameters
        ----------
        time : numpy.array
            Vector of time values.
        y : numpy.array
            Vector of y-axis values (e.g., dye release).

        Returns
        -------
        list of numbers
            The best-fit parameter values produced by the fitting procedure.
        """
        params = [fitting.Parameter(self.initial_guesses[i])
                  for i in range(len(self.initial_guesses))]
        def fit_func_closure(t):
            return self.fit_func(t, [p() for p in params])
        fitting.fit(fit_func_closure, params, y, time,
                    log_transform=self.log_transform)
        return [p() for p in params]

##########################################
# Various Fitting functions (subclasses) #
##########################################

class LinearIntercept(TitrationFit):
    r"""Fit timecourses to a straight line through a fitted intercept.

    .. math::

        y(t) = k_1 * t + k_2
    """
    def __init__(self, initial_guesses=[5e-3, 1.], log_transform=True):
        super(LinearIntercept, self).__init__(param_names=['$k_1$', '$k_2$'],
                                              initial_guesses=initial_guesses,
                                              log_transform=log_transform)

    def fit_func(self, t, k_arr):
        """Linear (through intercept) fitting function."""
        return k_arr[0] * t + k_arr[1]

class Quadratic(TitrationFit):
    r"""Fit timecourses to a quadratic polynomial.

    .. math::

        y(t) = k_1 * t^2 + k_2 * t + k_3
    """
    def __init__(self, initial_guesses=[1e-3, 5e-3, 1.], log_transform=True):
        super(Quadratic, self).__init__(param_names=['$k_1$', '$k_2$', '$k_3$'],
                                        initial_guesses=initial_guesses,
                                        log_transform=log_transform)

    def fit_func(self, t, k_arr):
        """Quadratic fitting function."""
        return k_arr[0] * t**2 + k_arr[1] * t + k_arr[2]

class Cubic(TitrationFit):
    r"""Fit timecourses to a cubic polynomial.

    .. math::

        y(t) = k_1 * t^3 + k_2 * t^2 + k_3 * t + k_4
    """
    def __init__(self, initial_guesses=[1e-4, 1e-3, 5e-3, 1.],
                 log_transform=True):
        super(Cubic, self).__init__(
                param_names=['$k_1$', '$k_2$', '$k_3$', '$k_4$'],
                initial_guesses=initial_guesses, log_transform=log_transform)

    def fit_func(self, t, k_arr):
        """Cubic fitting function."""
        return k_arr[0] * t**3 + k_arr[1] * t**2 + k_arr[2] * t + k_arr[3]

class TwoExpSum(TitrationFit):
    r"""Fit timecourses to a four-parameter sum of two exponentials

    .. math::

        y(t) = F_{max1} \left(1 - e^{-k_1 t}\right +
               F_{max2} \left(1 - e^{-k_2 t}\right
    """
    def __init__(self):
        super(TwoExpSum, self).__init__(
                    param_names=['$k_1$', '$F_{max1}$', '$k_2$', '$F_{max2}$'],
                    initial_guesses=[1e-3, 20, 1e-4, 30])

    def fit_func(self, t, k_arr):
        """Two-exponential fitting function."""
        return (k_arr[1]* (1 - np.exp(-k_arr[0] * t))) +\
               (k_arr[3]* (1 - np.exp(-k_arr[2] * t)))

