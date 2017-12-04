"""
Precompute coefficients of Temme's asymptotic expansion for gammainc.

This takes about 8 hours to run on a 2.3 GHz Macbook Pro with 4GB ram.

Sources:
[1] NIST, "Digital Library of Mathematical Functions",
    http://dlmf.nist.gov/

"""
from __future__ import division, print_function, absolute_import

import os
from scipy.special._precompute.utils import lagrange_inversion

try:
    import mpmath as mp
except ImportError:
    pass


def compute_a(n):
    """a_k from DLMF 5.11.6"""
    a = [mp.sqrt(2)/2]
    for k in range(1, n):
        ak = a[-1]/k
        for j in range(1, len(a)):
            ak -= a[j]*a[-j]/(j + 1)
        ak /= a[0]*(1 + mp.mpf(1)/(k + 1))
        a.append(ak)
    return a


def compute_g(n):
    """g_k from DLMF 5.11.3/5.11.5"""
    a = compute_a(2*n)
    g = []
    for k in range(n):
        g.append(mp.sqrt(2)*mp.rf(0.5, k)*a[2*k])
    return g


def eta(lam):
    """Function from DLMF 8.12.1 shifted to be centered at 0."""
    if lam > 0:
        return mp.sqrt(2*(lam - mp.log(lam + 1)))
    elif lam < 0:
        return -mp.sqrt(2*(lam - mp.log(lam + 1)))
    else:
        return 0


def compute_alpha(n):
    """alpha_n from DLMF 8.12.13"""
    coeffs = mp.taylor(eta, 0, n - 1)
    return lagrange_inversion(coeffs)
    

def compute_d(K, N):
    """d_{k, n} from DLMF 8.12.12"""
    M = N + 2*K
    d0 = [-mp.mpf(1)/3]
    alpha = compute_alpha(M + 2)
    for n in range(1, M):
        d0.append((n + 2)*alpha[n+2])
    d = [d0]
    g = compute_g(K)
    for k in range(1, K):
        dk = []
        for n in range(M - 2*k):
            dk.append((-1)**k*g[k]*d[0][n] + (n + 2)*d[k-1][n+2])
        d.append(dk)
    for k in range(K):
        d[k] = d[k][:N]
    return d


header = \
r"""/* This file was automatically generated by _precomp/gammainc.py.
 * Do not edit it manually!
 */

#ifndef IGAM_H
#define IGAM_H

#define K {}
#define N {}

double d[K][N] =
{{"""

footer = \
r"""
#endif
"""

def main():
    print(__doc__)
    K = 25
    N = 25
    with mp.workdps(50):
        d = compute_d(K, N)
    fn = os.path.join(os.path.dirname(__file__), '..', 'cephes', 'igam.h')
    with open(fn + '.new', 'w') as f:
        f.write(header.format(K, N))
        for k, row in enumerate(d):
            row = map(lambda x: mp.nstr(x, 17, min_fixed=0, max_fixed=0), row)
            f.write('{')
            f.write(", ".join(row))
            if k < K - 1:
                f.write('},\n')
            else:
                f.write('}};\n')
        f.write(footer)
    os.rename(fn + '.new', fn)


if __name__ == "__main__":
    main()
