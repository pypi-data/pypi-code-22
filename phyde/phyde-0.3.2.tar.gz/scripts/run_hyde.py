#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# run_hyde.py
# Written by PD Blischak

"""
<< run_hyde.py >>

Run a full hybridization detection analysis or test for hybridization in a
specified set of triples.

Arguments
---------

    - infile <string>   : name of the DNA sequence data file.
    - mapfile <string>  : name of the taxon map file.
    - outgroup <string> : name of the outgroup.
    - nind <int>        : number of sampled individuals.
    - nsites <int>      : number of sampled sites.
    - ntaxa <int>       : number of sampled taxa/populations.
    - triples <string>  : name of the file containing triples for testing [optional].

Output
------

    Writes a file ('hyde-out.txt') listing each triple that was tested (P1, Hybrid, P2),
    along with the corresponding Z-score, p-value, gamma estimate, and
    site pattern counts.
"""

from __future__ import print_function
import phyde as hd
import argparse
import sys
import os

def parse_triples(triples_file):
    """
    Parse a three column table or previous results file to get the names
    of the taxa that are going to be tested for hybridization.

    Returns a list of three-tuples of the form (P1, Hybrid, P2) for all triples
    that are to be tested.
    """
    triples = []
    with open(triples_file) as f:
        lines = f.read().splitlines()
        # remove header information if reading in a previous results file
        if lines[0].split()[0] == "P1" and lines[0].split()[1] == "Hybrid" and lines[0].split()[2] == "P2":
            lines = lines[1:]
        # catch the case where the last line in the file is blank
        if len(lines[-1]) == 0:
            triples = [(l.split()[0], l.split()[1], l.split()[2]) for l in lines[:-1]]
        else:
            triples = [(l.split()[0], l.split()[1], l.split()[2]) for l in lines]
    return triples

def write_out(out, triple, outfile):
    """
    Take the output from test_triple() and write it to file.
    """
    print(triple[0], "\t", triple[1], "\t", triple[2], "\t", sep='', end='', file=outfile)
    print(out['Zscore'], "\t", sep='', end='', file=outfile)
    print(out['Pvalue'], "\t", sep='', end='', file=outfile)
    print(out['Gamma'], "\t", sep='', end='', file=outfile)
    print(out['AAAA'], "\t", sep='', end='', file=outfile)
    print(out['AAAB'], "\t", sep='', end='', file=outfile)
    print(out['AABA'], "\t", sep='', end='', file=outfile)
    print(out['AABB'], "\t", sep='', end='', file=outfile)
    print(out['AABC'], "\t", sep='', end='', file=outfile)
    print(out['ABAA'], "\t", sep='', end='', file=outfile)
    print(out['ABAB'], "\t", sep='', end='', file=outfile)
    print(out['ABAC'], "\t", sep='', end='', file=outfile)
    print(out['ABBA'], "\t", sep='', end='', file=outfile)
    print(out['BAAA'], "\t", sep='', end='', file=outfile)
    print(out['ABBC'], "\t", sep='', end='', file=outfile)
    print(out['CABC'], "\t", sep='', end='', file=outfile)
    print(out['BACA'], "\t", sep='', end='', file=outfile)
    print(out['BCAA'], "\t", sep='', end='', file=outfile)
    print(out['ABCD'], "\n", sep='', end='', file=outfile)

if __name__ == "__main__":
    """
    Runs the script.
    """
    # print docstring if only the name of the script is given
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    parser = argparse.ArgumentParser(description="Options for run_hyde.py",
                                     add_help=True)

    required = parser.add_argument_group("required arguments")
    required.add_argument('-i', '--infile', action="store", type=str, required=True,
                          metavar='\b', help="name of the data input file")
    required.add_argument('-m', '--map', action="store", type=str, required=True,
                          metavar='\b', help="map of individuals to taxa")
    required.add_argument('-o', '--outgroup', action="store", type=str, required=True,
                          metavar='\b', help="name of the outgroup (only one accepted)")
    required.add_argument('-n', '--num_ind', action="store", type=int, required=True,
                          metavar='\b', help="number of individuals in data matrix")
    required.add_argument('-t', '--num_taxa', action="store", type=int, required=True,
                          metavar='\b', help="number of taxa (species, OTUs)")
    required.add_argument('-s', '--num_sites', action="store", type=int, required=True,
                          metavar='\b', help="number of sites in the data matrix")

    additional = parser.add_argument_group("additional arguments")
    additional.add_argument('-tr','--triples', action="store", type=str, default="none",
                          metavar='\b', help="table of triples to be analyzed using bootstrapping.")
    additional.add_argument('-p', '--pvalue', action="store", type=float, default=0.05,
                            metavar='\b', help="p-value cutoff for test of significance [default=0.05]")
    additional.add_argument('--prefix', action="store", type=str, default="hyde",
                            metavar='\b', help="prefix appended to output files [default=hyde]")

    args     = parser.parse_args()
    infile   = args.infile
    mapfile  = args.map
    outgroup = args.outgroup
    nind     = args.num_ind
    ntaxa    = args.num_taxa
    nsites   = args.num_sites
    pvalue   = args.pvalue
    prefix   = args.prefix

    if os.path.exists(prefix+"-out-filtered.txt"):
        print("\n**  Warning: File '"+prefix+"-out-filtered.txt' already exists. **")
        print("**  Renaming to 'old-"+prefix+"-out-filtered.txt'. **\n")
        os.rename(prefix+"-out-filtered.txt", "old-"+prefix+"-out-filtered.txt")
        filtered_outfile = open(prefix+"-out-filtered.txt", 'wa')
    else:
        filtered_outfile = open(prefix+"-out-filtered.txt", 'wa')
    print("P1\tHybrid\tP2\tZscore\tPvalue\tGamma\tAAAA\t\tAABA\tAABB\tAABC\tABAA\tABAB\tABAC\tABBA\tBAAA\tABBC\tCABC\tBACA\tBCAA\tABCD\n", end='', file=filtered_outfile)

    if args.triples != "none":
        print("--> Using triples in file ", args.triples, sep='')
        triples = parse_triples(args.triples)
        if os.path.exists(prefix+"-out.txt"):
            print("\n**  Warning: File '"+prefix+"-out.txt' already exists. **")
            print("**  Renaming to 'old-"+prefix+"-out.txt'. **\n")
            os.rename(prefix+"-out.txt", "old-"+prefix+"-out.txt")
            outfile = open(prefix+"-out.txt", 'wa')
        else:
            outfile = open(prefix+"-out.txt", 'wa')

        # Read in data as HydeData object
        data = hd.HydeData(infile, mapfile, outgroup, nind, ntaxa, nsites)
        print("P1\tHybrid\tP2\tZscore\tPvalue\tGamma\tAAAA\t\tAABA\tAABB\tAABC\tABAA\tABAB\tABAC\tABBA\tBAAA\tABBC\tCABC\tBACA\tBCAA\tABCD\n", end='', file=outfile)
        for t in triples:
            res = data.test_triple(t[0], t[1], t[2])
            write_out(res, t, outfile)
            if res['Pvalue'] < (pvalue / len(triples)) and res['Gamma'] > 0.0 and res['Gamma'] < 1.0:
                write_out(res, t, filtered_outfile)
    else:
        print("--> Running full HyDe analysis with hyde_cpp")
        res = hd.run_hyde(infile, mapfile, outgroup, nind, ntaxa, nsites, pvalue, prefix)
        filtered_res = {k:v for k,v in res.res.items() if v['Pvalue'] < (pvalue / len(res.res)) and v['Gamma'] > 0.0 and v['Gamma'] < 1.0}
        for k,v in filtered_res.items():
            write_out(v, k, filtered_outfile)
