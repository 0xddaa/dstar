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
        bbls_info = cov["basic_blocks_info"]["list"]
        for bbl_info in bbls_info:
            if bbl_info["address"] not in BBLs:
                BBLs.append(str(bbl_info["address"]))

def get_covs():
    p = sp.Popen("ls %s" % (LOGPATH + BINARY + "*"), shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    assert p.stderr.read().strip() == "", "benchmark %s not found" % (BINARY)

    logs = p.stdout.read().strip().split("\n")
    for log in logs:
        with open(log, "r") as f:
            COVs.append(json.loads(f.read()))

def dstar():
    global COVs
    global BBLs

    # init variable Ncf, Nuf, Ncs for dstar
    ins_vars = dict()
    for bbl in BBLs:
        v = {"Ncf" : 0, "Nuf" : 0, "Ncs" : 0, "Nus" : 0}
        ins_vars[bbl] = v

    for cov in COVs:
        bbls = [] 
        bbls_info = cov["basic_blocks_info"]["list"]
        for bbl_info in bbls_info:
            bbls.append(str(bbl_info["address"]))

        # count coverage bbls
        for bbl in bbls:
            if bool(cov["crash"]):
                ins_vars[bbl]["Ncf"] += 1
            else:
                ins_vars[bbl]["Ncs"] += 1

        # count uncoverage bbls
#        print list(set(BBLs) - set(bbls))
        for bbl in list(set(BBLs) - set(bbls)):
            if bool(cov["crash"]):
                ins_vars[bbl]["Nuf"] += 1
            else:
                ins_vars[bbl]["Nus"] += 1
    
    # calculate score
    scores = []
    for ins_var in ins_vars.items():
        ins_addr = ins_var[0]
        ins_v = ins_var[1]
        try:
            score = float(ins_v["Ncf"] * ins_v["Ncf"]) / (ins_v["Ncs"] + ins_v["Nuf"])
        except ZeroDivisionError:
            score = -1
        if score != 0:
            scores.append({ins_addr : score})

    for s in scores:
        print s

def main(argc, argv):
    global BINARY
    if argc == 2:
        BINARY = argv[1]

    get_covs()
    get_all_bbls()
    dstar()


main(len(sys.argv), sys.argv)    
