# Copyright 1996-2015 PSERC. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Builds the vector of complex bus power injections.
"""

from numpy import ones, flatnonzero as find
from scipy.sparse import csr_matrix as sparse

from pypower.idx_bus import PD, QD
from pypower.idx_gen import GEN_BUS, PG, QG, GEN_STATUS
from pandapower.idx_bus import CID, CZD


def makeSbus(baseMVA, bus, gen, vm=None):
    """Builds the vector of complex bus power injections.

    Returns the vector of complex bus power injections, that is, generation
    minus load. Power is expressed in per unit.

    @see: L{makeYbus}

    @author: Ray Zimmerman (PSERC Cornell)
    @author: Richard Lincoln
    """
    ## generator info
    on = find(gen[:, GEN_STATUS] > 0)      ## which generators are on?
    gbus = gen[on, GEN_BUS]                   ## what buses are they at?

    ## form net complex bus power injection vector
    nb = bus.shape[0]
    ngon = on.shape[0]
    ## connection matrix, element i, j is 1 if gen on(j) at bus i is ON
    Cg = sparse((ones(ngon), (gbus, range(ngon))), (nb, ngon))

    S_load = bus[:, PD] + 1j * bus[:, QD]
    if vm is not None:
        ci = bus[:, CID]
        cz = bus[:, CZD]
        cp = (1 - ci - cz)
        volt_depend = cp + ci * vm + cz * vm ** 2
        S_load *= volt_depend
    ## power injected by gens plus power injected by loads converted to p.u.
    Sbus = (Cg * (gen[on, PG] + 1j * gen[on, QG])
            - S_load) / baseMVA

    return Sbus
