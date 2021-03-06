import numpy as np
import scipy.stats
import pysb.builder

class Builder(pysb.builder.Builder):

    def __init__(self, params_dict=None):
        # Sets self.model = Model(), and self.param_dict
        super(Builder, self).__init__(params_dict=params_dict)

    def __getstate__(self):
        # Clear nbd_func since it causes problems with pickling
        state = self.__dict__.copy()
        if 'obs_func' in state:
            del state['obs_func']
        return state

    def __setstate__(self, state):
        # Re-init the obs_func which we didn't pickle
        self.__dict__.update(state)
        self.set_obs_func()


    def build_model_multiconf(self, num_confs, c0_scaling, nbd_lbound=None,
                              nbd_ubound=None, normalized_data=False,
                              scaling_prior_type='linear',
                              reversible=False):
        if num_confs < 2:
            raise ValueError('There must be a minimum of two conformations.')

        self.num_confs = num_confs
        self.reversible = reversible

        # Initialize monomer and initial condition
        Bax = self.monomer('Bax', ['conf'],
                           {'conf': ['c%d' % i for i in range(num_confs)]})
        Bax_0 = self.parameter('Bax_0', 1, prior=None)
        self.initial(Bax(conf='c0'), Bax_0)

        # Scaling for initial conformation
        scaling = self.parameter('c0_scaling', c0_scaling, prior=None)
        obs = self.observable('Bax_c0', Bax(conf='c0'))
        sympy_expr = (scaling * obs)

        # Set the bounds for the scaling parameters
        if scaling_prior_type == 'linear':
            if normalized_data:
                scaling_prior = UniformLinear(-1, 1)
            else:
                if nbd_lbound is None or nbd_ubound is None:
                    raise ValueError("If NBD data is not normalized, upper and "
                                     "lower bounds for the scaling parameters "
                                     "must be explicitly specified.")
                scaling_prior = UniformLinear(np.log10(nbd_lbound),
                                              np.log10(nbd_ubound))
        elif scaling_prior_type == 'normal':
            scaling_prior = Normal(np.log10(c0_scaling), np.log10(1.5))
        else:
            raise ValueError('Unknown scaling prior type.')

        # Rules for transitions between other conformations
        for i in range(num_confs-1):
            rate = self.parameter('c%d_to_c%d_k' % (i, i+1), 1e-3,
                                  prior=Uniform(-6, -1))
            scaling = self.parameter('c%d_scaling' % (i+1), 1,
                                     prior=scaling_prior)

            self.rule('c%d_to_c%d' % (i, i+1),
                      Bax(conf='c%d' % i) >> Bax(conf='c%d' % (i+1)), rate)
            if reversible:
                rate = self.parameter('c%d_to_c%d_k' % (i+1, i), 1e-3,
                                      prior=Uniform(-6, -1))
                self.rule('c%d_to_c%d' % (i+1, i),
                          Bax(conf='c%d' % (i+1)) >> Bax(conf='c%d' % i), rate)

            obs = self.observable('Bax_c%d' % (i+1), Bax(conf='c%d' % (i+1)))

            sympy_expr += (scaling * obs)

        # The expression mapping to our experimental observable
        self.expression('NBD', sympy_expr)

        # Set the model name
        self.model.name = "%dconfs" % num_confs

        # Set the model obs func
        self.set_obs_func()

    def build_model_multiconf_nbd_fret(self, num_confs, c0_scaling,
                                       nbd_lbound=None, nbd_ubound=None,
                                       scaling_prior_type='linear',
                                       normalized_data=False, reversible=False):
        if num_confs < 2:
            raise ValueError('There must be a minimum of two conformations.')

        self.num_confs = num_confs
        self.reversible = reversible

        # Initialize monomer and initial condition
        Bax = self.monomer('Bax', ['conf'],
                           {'conf': ['c%d' % i for i in range(num_confs)]})
        Bax_0 = self.parameter('Bax_0', 1, prior=None)
        self.initial(Bax(conf='c0'), Bax_0)

        # Scaling for initial NBD conformation
        scaling = self.parameter('c0_scaling', c0_scaling, prior=None)
        obs = self.observable('Bax_c0', Bax(conf='c0'))
        sympy_expr = (scaling * obs)

        # Scaling for initial NBD conformation
        fret_scaling = self.parameter('fret0_scaling', 0, prior=None)
        fret_sympy_expr = (fret_scaling * obs)

        # Set the bounds for the scaling parameters
        fret_scaling_prior = UniformLinear(-1, 2)

        if scaling_prior_type == 'linear':
            if normalized_data:
                scaling_prior = UniformLinear(-1, 1)
            else:
                if nbd_lbound is None or nbd_ubound is None:
                    raise ValueError("If NBD data is not normalized, upper and "
                                     "lower bounds for the scaling parameters "
                                     "must be explicitly specified.")
                scaling_prior = UniformLinear(np.log10(nbd_lbound),
                                              np.log10(nbd_ubound))
        elif scaling_prior_type == 'normal':
            scaling_prior = Normal(np.log10(c0_scaling), np.log10(1.5))
        else:
            raise ValueError('Unknown scaling prior type.')

        # Rules for transitions between other conformations
        for i in range(num_confs-1):
            rate = self.parameter('c%d_to_c%d_k' % (i, i+1), 1e-3,
                                  prior=Uniform(-6, -1))
            scaling = self.parameter('c%d_scaling' % (i+1), 1,
                                     prior=scaling_prior)
            fret_scaling = self.parameter('fret%d_scaling' % (i+1), 20.,
                                     prior=fret_scaling_prior)

            self.rule('c%d_to_c%d' % (i, i+1),
                      Bax(conf='c%d' % i) >> Bax(conf='c%d' % (i+1)), rate)
            if reversible:
                rate = self.parameter('c%d_to_c%d_k' % (i+1, i), 1e-3,
                                      prior=Uniform(-6, -1))
                self.rule('c%d_to_c%d' % (i+1, i),
                          Bax(conf='c%d' % (i+1)) >> Bax(conf='c%d' % i), rate)

            obs = self.observable('Bax_c%d' % (i+1), Bax(conf='c%d' % (i+1)))

            sympy_expr += (scaling * obs)
            fret_sympy_expr += (fret_scaling * obs)
        # The expression mapping to our experimental observable
        self.expression('NBD', sympy_expr)
        self.expression('FRET', fret_sympy_expr)

        # Set the model name
        self.model.name = "%dconfs" % num_confs

        # Set the model obs func
        self.set_nbd_fret_obs_func()

    def set_obs_func(self):
        """Assigns a function to self.formula that, when called after setting
        the parameter values of self.model, returns the timecourse for the
        given parameters."""
        if self.num_confs == 2 and self.reversible == False:
            def nbd_func(t):
                Bax_0 = self['Bax_0'].value
                c0 = Bax_0 * np.exp(-self['c0_to_c1_k'].value * t)
                nbd = (self['c0_scaling'].value * c0 +
                       self['c1_scaling'].value * (Bax_0 - c0))
                return {'NBD': nbd}
        elif self.num_confs == 2 and self.reversible == True:
            def nbd_func(t):
                kf = self['c0_to_c1_k'].value
                kr = self['c1_to_c0_k'].value
                Bax_0 = self['Bax_0'].value
                c0eq = (kr * Bax_0) / float(kf + kr)
                c1eq = (kf * Bax_0) / float(kf + kr)
                c0 = c1eq * np.exp(-(kf+kr)*t) + c0eq
                nbd = (self['c0_scaling'].value * c0 +
                       self['c1_scaling'].value * (Bax_0 - c0))
                return {'NBD': nbd}
        elif self.num_confs == 3 and self.reversible == False:
            def nbd_func(t):
                k1 = self['c0_to_c1_k'].value
                k2 = self['c1_to_c2_k'].value
                Bax_0 = self['Bax_0'].value
                # First, the case where k1 and k2 are equal (need to treat
                # separately to avoid divide by 0 errors)
                if k1 == k2:
                    print "nbd_func, equal"
                    c0 = Bax_0 * np.exp(-k1 * t)
                    c1 = Bax_0 * t * k1 * np.exp(-k1 * t)
                    nbd = (self['c0_scaling'].value * c0 +
                           self['c1_scaling'].value * c1 +
                           self['c2_scaling'].value * (Bax_0 - c0 - c1))
                    return {'NBD': nbd}
                # The typical case, where k1 and k2 are not equal
                else:
                    c0 = Bax_0 * np.exp(-k1 * t)
                    c1 = (((np.exp(-k1*t) - np.exp(-k2*t)) * k1 * Bax_0) /
                          (k2 - k1))
                    nbd = (self['c0_scaling'].value * c0 +
                           self['c1_scaling'].value * c1 +
                           self['c2_scaling'].value * (Bax_0 - c0 - c1))
                    return {'NBD': nbd}
        elif self.num_confs == 4 and self.reversible == False:
            # Here we don't specifically handle the case where the parameters are
            # equal since it's so unlikely to come up in parameter estimation,
            # which is the immediate concern
            def nbd_func(t):
                k1 = self['c0_to_c1_k'].value
                k2 = self['c1_to_c2_k'].value
                k3 = self['c2_to_c3_k'].value
                if k1 == k2 or k2 == k3 or k1 == k3:
                    raise ValueError('Function for equal values of k1, k2, or '
                                     'k3 is not currently implemented.')
                Bax_0 = self['Bax_0'].value
                c0 = np.exp(-k1*t)*Bax_0
                c1 = (((np.exp(-k1*t) - np.exp(-k2*t)) * k1 * Bax_0) /
                      (k2 - k1))
                c2 = ((np.exp(-(k1 + k2 + k3) * t) * k1 * k2 *
                       (np.exp((k1+k2)*t) * (k1 - k2) +
                        np.exp((k2+k3)*t) * (k2 - k3) +
                        np.exp((k1+k3)*t) * (k3 - k1)) * Bax_0) /
                        ((k1 - k2) * (k1 - k3) * (k2 - k3)))
                c3 = Bax_0 - c0 - c1 - c2
                nbd = (self['c0_scaling'].value * c0 +
                       self['c1_scaling'].value * c1 +
                       self['c2_scaling'].value * c2 +
                       self['c3_scaling'].value * c3)
                return {'NBD': nbd}
        elif self.num_confs == 5 and self.reversible == False:
            # Here we don't specifically handle the case where the parameters are
            # equal since it's so unlikely to come up in parameter estimation,
            # which is the immediate concern
            def nbd_func(t):
                k1 = self['c0_to_c1_k'].value
                k2 = self['c1_to_c2_k'].value
                k3 = self['c2_to_c3_k'].value
                k4 = self['c3_to_c4_k'].value
                if k1 == k2 or k1 == k3 or k2 == k3 or k1 == k4 or k2 == k4 or \
                   k3 == k4:
                    raise ValueError('Function for equal values of k1, k2, k3, '
                                     'or k4 is not currently implemented.')
                Bax_0 = self['Bax_0'].value
                c0 = np.exp(-k1*t)*Bax_0
                c1 = (((np.exp(-k1*t) - np.exp(-k2*t)) * k1 * Bax_0) /
                      (k2 - k1))
                c2 = ((np.exp(-(k1 + k2 + k3) * t) * k1 * k2 *
                       (np.exp((k1+k2)*t) * (k1 - k2) +
                        np.exp((k2+k3)*t) * (k2 - k3) +
                        np.exp((k1+k3)*t) * (k3 - k1)) * Bax_0) /
                        ((k1 - k2) * (k1 - k3) * (k2 - k3)))
                c3 = ((np.exp(-(k1+k2+k3+k4)*t) * k1 * k2 * k3 *
                       (np.exp((k1+k2+k3)*t)*(k1-k2)*(k1-k3)*(k2-k3) -
                        np.exp((k1+k2+k4)*t)*(k1-k2)*(k1-k4)*(k2-k4) +
                        np.exp((k1+k3+k4)*t)*(k1-k3)*(k1-k4)*(k3-k4) -
                        np.exp((k2+k3+k4)*t)*(k2-k3)*(k2-k4)*(k3-k4)) * Bax_0) /
                       ((k1-k2)*(k1-k3)*(k2-k3)*(k1-k4)*(k2-k4)*(k3-k4)))
                c4 = Bax_0 - c0 - c1 - c2 - c3
                nbd = (self['c0_scaling'].value * c0 +
                       self['c1_scaling'].value * c1 +
                       self['c2_scaling'].value * c2 +
                       self['c3_scaling'].value * c3 +
                       self['c4_scaling'].value * c4)
                return {'NBD': nbd}
        # If we don't fit one of these categories, set to None
        else:
            nbd_func = None
        # Assign the function to the instance
        self.obs_func = nbd_func

    def set_nbd_fret_obs_func(self):
        """Assigns a function to self.formula that, when called after setting
        the parameter values of self.model, returns the timecourse for the
        given parameters."""
        if self.num_confs == 3 and self.reversible == False:
            def nbd_fret_func(t):
                k1 = self['c0_to_c1_k'].value
                k2 = self['c1_to_c2_k'].value
                Bax_0 = self['Bax_0'].value
                # First, the case where k1 and k2 are equal (need to treat
                # separately to avoid divide by 0 errors)
                if k1 == k2:
                    print "nbd_func, equal"
                    c0 = Bax_0 * np.exp(-k1 * t)
                    c1 = Bax_0 * t * k1 * np.exp(-k1 * t)
                    nbd = (self['c0_scaling'].value * c0 +
                           self['c1_scaling'].value * c1 +
                           self['c2_scaling'].value * (Bax_0 - c0 - c1))
                    fret = (self['fret0_scaling'].value * c0 +
                           self['fret1_scaling'].value * c1 +
                           self['fret2_scaling'].value * (Bax_0 - c0 - c1))
                    return {'NBD': nbd, 'FRET': fret}
                # The typical case, where k1 and k2 are not equal
                else:
                    c0 = Bax_0 * np.exp(-k1 * t)
                    c1 = (((np.exp(-k1*t) - np.exp(-k2*t)) * k1 * Bax_0) /
                          (k2 - k1))
                    nbd = (self['c0_scaling'].value * c0 +
                           self['c1_scaling'].value * c1 +
                           self['c2_scaling'].value * (Bax_0 - c0 - c1))
                    fret = (self['fret0_scaling'].value * c0 +
                           self['fret1_scaling'].value * c1 +
                           self['fret2_scaling'].value * (Bax_0 - c0 - c1))
                    return {'NBD': nbd, 'FRET': fret}
        elif self.num_confs == 4 and self.reversible == False:
            # Here we don't specifically handle the case where the parameters are
            # equal since it's so unlikely to come up in parameter estimation,
            # which is the immediate concern
            def nbd_fret_func(t):
                k1 = self['c0_to_c1_k'].value
                k2 = self['c1_to_c2_k'].value
                k3 = self['c2_to_c3_k'].value
                if k1 == k2 or k2 == k3 or k1 == k3:
                    raise ValueError('Function for equal values of k1, k2, or '
                                     'k3 is not currently implemented.')
                Bax_0 = self['Bax_0'].value
                c0 = np.exp(-k1*t)*Bax_0
                c1 = (((np.exp(-k1*t) - np.exp(-k2*t)) * k1 * Bax_0) /
                      (k2 - k1))
                c2 = ((np.exp(-(k1 + k2 + k3) * t) * k1 * k2 *
                       (np.exp((k1+k2)*t) * (k1 - k2) +
                        np.exp((k2+k3)*t) * (k2 - k3) +
                        np.exp((k1+k3)*t) * (k3 - k1)) * Bax_0) /
                        ((k1 - k2) * (k1 - k3) * (k2 - k3)))
                c3 = Bax_0 - c0 - c1 - c2
                nbd = (self['c0_scaling'].value * c0 +
                       self['c1_scaling'].value * c1 +
                       self['c2_scaling'].value * c2 +
                       self['c3_scaling'].value * c3)
                fret = (self['fret0_scaling'].value * c0 +
                       self['fret1_scaling'].value * c1 +
                       self['fret2_scaling'].value * c2 +
                       self['fret3_scaling'].value * c3)
                return {'NBD': nbd, 'FRET': fret}
        # If we don't fit one of these categories, set to None
        else:
            nbd_fret_func = None
        # Assign the function to the instance
        self.obs_func = nbd_fret_func


class Uniform():
    """A uniform prior distribution.

    Parameters
    ----------
    lower_bound : number
        The lower bound of the interval.
    upper_bound : number
        The upper bound of the interval.
    """
    def __init__(self, lower_bound, upper_bound):
        self.lower_bound = float(lower_bound)
        self.upper_bound = float(upper_bound)
        self.p = 1. / (upper_bound - lower_bound)

    def pdf(self, num):
        """Returns the negative log probability of the given number.

        The negative log probability is given by:

        infinity, if num is outside of the bounds of the interval;
        log(1 / (upper - lower)), otherwise.
        """
        if num < self.lower_bound or num > self.upper_bound:
            return np.inf
        else:
            return -np.log(self.p)

    def random(self):
        """Get a random sample from the uniform distribution."""
        return np.random.uniform(low=self.lower_bound, high=self.upper_bound)

    def inverse_cdf(self, percentile):
        """Get the value associated with the percentile probability.

        Also known as the percent point function. A wrapper around
        scipy.stats.uniform.ppf().
        """
        scale = self.upper_bound - self.lower_bound
        return scipy.stats.uniform.ppf(percentile, loc=self.lower_bound,
                                       scale=scale)


class UniformLinear(Uniform):
    """A uniform prior distribution that inverts a log10-transformation.

    Parameters
    ----------
    lower_bound : number
        The lower bound of the interval.
    upper_bound : number
        The upper bound of the interval.
    """
    def __init__(self, lower_bound, upper_bound):
        self.linear_lower_bound = 10 ** float(lower_bound)
        self.linear_upper_bound = 10 ** float(upper_bound)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.p = 1. / (self.linear_upper_bound - self.linear_lower_bound)

    def pdf(self, num):
        """Returns the negative log probability of the given number.

        The negative log probability is given by:

        infinity, if num is outside of the bounds of the interval;
        -log(1 / (upper - lower)), otherwise.
        """
        num = 10 ** num
        if num < self.linear_lower_bound or num > self.linear_upper_bound:
            return np.inf
        else:
            return -np.log(self.p)

    def random(self):
        """Get a random sample from the (non-log) uniform distribution."""
        rand_sample = np.random.uniform(low=self.linear_lower_bound,
                                        high=self.linear_upper_bound)
        return np.log10(rand_sample)

    def inverse_cdf(self, percentile):
        """Get the value associated with the percentile probability.

        Also known as the percent point function. A wrapper around
        scipy.stats.uniform.ppf().
        """
        scale = self.linear_upper_bound - self.linear_lower_bound
        value = scipy.stats.uniform.ppf(percentile, loc=self.linear_lower_bound,
                                        scale=scale)
        return np.log10(value)


class Normal():
    def __init__(self, mean, stdev):
        self.mean = float(mean)
        self.stdev = float(stdev)

    def pdf(self, num):
        """Returns the negative log probability of the given number.

        The negative log probability is given by:

        (num - mean)^2 / (2 * stdev ** 2)
        """
        return ((num - self.mean)**2) / (2. * self.stdev ** 2)

    def random(self):
        """Get a random sample from the normal distribution."""
        return (self.stdev * np.random.randn()) + self.mean

    def inverse_cdf(self, percentile):
        """Get the value associated with the percentile probability.

        Also known as the percent point function. A wrapper around
        scipy.stats.norm.ppf().
        """
        return scipy.stats.norm.ppf(percentile, loc=self.mean,
                                    scale=self.stdev)



