#!/usr/bin/python

import json
import subprocess as sp
import sys

LOGPATH = "/home/dada/pin/CodeCoverage/log/"
BINARY = "bof1"
BBLs = []

def parse_report(report):
    global BBLs
    jr = json.loads(report)
    bbls = jr["basic_blocks_info"]["list"]
    for bbl in bbls:
        if bbl["address"] not in BBLs:
            BBLs.append(str(bbl["address"]))
    
def get_all_bbls():
    p = sp.Popen("ls %s" % (LOGPATH + BINARY + "*"), shell=True, stdout=sp.PIPE)
    logs = p.stdout.read().strip().split("\n")

    for log in logs:
        with open(log, "r") as f:
            report = f.read()
            parse_report(report)

    print BBLs

def main(argc, argv):
    global BINARY
    if argc == 2:
        BINARY = argv[1]
        
    get_all_bbls()


main(len(sys.argv), sys.argv)    
