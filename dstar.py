#!/usr/bin/python

import json
import subprocess as sp
import sys

LOGPATH = "/home/dada/pin/CodeCoverage/log/"
BINARY = "bof1"
COVs = []
BBLs = []
    
def get_all_bbls():
    global BBLs

    for cov in COVs:
        bbls = cov["basic_blocks_info"]["list"]
        for bbl in bbls:
            if bbl["address"] not in BBLs:
                BBLs.append(str(bbl["address"]))

def get_covs():
    p = sp.Popen("ls %s" % (LOGPATH + BINARY + "*"), shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    assert p.stderr.read().strip() == "", "benchmark %s not found" % (BINARY)
    logs = p.stdout.read().strip().split("\n")

    for log in logs:
        with open(log, "r") as f:
            COVs.append(json.loads(f.read()))

def main(argc, argv):
    global BINARY
    if argc == 2:
        BINARY = argv[1]

    get_covs()
    get_all_bbls()
    print BBLs


main(len(sys.argv), sys.argv)    
