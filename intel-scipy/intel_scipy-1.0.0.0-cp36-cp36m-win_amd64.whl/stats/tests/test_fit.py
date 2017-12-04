from __future__ import division, print_function, absolute_import

import os

import numpy as np
from numpy.testing import assert_allclose
from scipy._lib._numpy_compat import suppress_warnings
import pytest
from scipy import stats

from .test_continuous_basic import distcont

# this is not a proper statistical test for convergence, but only
# verifies that the estimate and true values don't differ by too much

fit_sizes = [1000, 5000]  # sample sizes to try

thresh_percent = 0.25  # percent of true parameters for fail cut-off
thresh_min = 0.75  # minimum difference estimate - true to fail test

failing_fits = [
        'burr',
        'chi2',
        'gausshyper',
        'genexpon',
        'gengamma',
        'kappa4',
        'ksone',
        'mielke',
        'ncf',
        'ncx2',
        'pearson3',
        'powerlognorm',
        'truncexpon',
        'tukeylambda',
        'vonmises',
        'wrapcauchy',
        'levy_stable',
        'trapz'
]

# Don't run the fit test on these:
skip_fit = [
    'erlang',  # Subclass of gamma, generates a warning.
]


def cases_test_cont_fit():
    # this tests the closeness of the estimated parameters to the true
    # parameters with fit method of continuous distributions
    # Note: is slow, some distributions don't converge with sample size <= 10000
    for distname, arg in distcont:
        if distname not in skip_fit:
            yield distname, arg


@pytest.mark.slow
@pytest.mark.parametrize('distname,arg', cases_test_cont_fit())
def test_cont_fit(distname, arg):
    if distname in failing_fits:
        # Skip failing fits unless overridden
        xfail = True
        try:
            xfail = not int(os.environ['SCIPY_XFAIL'])
        except:
            pass
        if xfail:
            msg = "Fitting %s doesn't work reliably yet" % distname
            msg += " [Set environment variable SCIPY_XFAIL=1 to run this test nevertheless.]"
            pytest.xfail(msg)

    distfn = getattr(stats, distname)

    truearg = np.hstack([arg, [0.0, 1.0]])
    diffthreshold = np.max(np.vstack([truearg*thresh_percent,
                                      np.ones(distfn.numargs+2)*thresh_min]),
                           0)

    for fit_size in fit_sizes:
        # Note that if a fit succeeds, the other fit_sizes are skipped
        np.random.seed(1234)

        with np.errstate(all='ignore'), suppress_warnings() as sup:
            sup.filter(category=DeprecationWarning, message=".*frechet_")
            rvs = distfn.rvs(size=fit_size, *arg)
            est = distfn.fit(rvs)  # start with default values

        diff = est - truearg

        # threshold for location
        diffthreshold[-2] = np.max([np.abs(rvs.mean())*thresh_percent,thresh_min])

        if np.any(np.isnan(est)):
            raise AssertionError('nan returned in fit')
        else:
            if np.all(np.abs(diff) <= diffthreshold):
                break
    else:
        txt = 'parameter: %s\n' % str(truearg)
        txt += 'estimated: %s\n' % str(est)
        txt += 'diff     : %s\n' % str(diff)
        raise AssertionError('fit not very good in %s\n' % distfn.name + txt)


def _check_loc_scale_mle_fit(name, data, desired, atol=None):
    d = getattr(stats, name)
    actual = d.fit(data)[-2:]
    assert_allclose(actual, desired, atol=atol,
                    err_msg='poor mle fit of (loc, scale) in %s' % name)


def test_non_default_loc_scale_mle_fit():
    data = np.array([1.01, 1.78, 1.78, 1.78, 1.88, 1.88, 1.88, 2.00])
    _check_loc_scale_mle_fit('uniform', data, [1.01, 0.99], 1e-3)
    _check_loc_scale_mle_fit('expon', data, [1.01, 0.73875], 1e-3)


def test_expon_fit():
    """gh-6167"""
    data = [0, 0, 0, 0, 2, 2, 2, 2]
    phat = stats.expon.fit(data, floc=0)
    assert_allclose(phat, [0, 1.0], atol=1e-3)

