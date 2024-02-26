#!/usr/bin/env python
from __future__ import print_function

import re
import sys
from os.path import abspath, dirname

# TODO are these script used?
cmsbot_dir = None
if __file__:
    cmsbot_dir = dirname(dirname(abspath(__file__)))
else:
    cmsbot_dir = dirname(dirname(abspath(sys.argv[0])))
sys.path.insert(0, cmsbot_dir)

from time import time

from es_utils import close_index, find_indexes, get_indexes, open_index

try:
    weeks = int(sys.argv[1])
except:
    weeks = 20
ignore_index = []
for idx in sys.argv[2:]:
    ignore_index.append(idx)
cur_week = int(((time() / 86400) + 4) / 7)
idxs = []
odxs = []
try:
    if sys.argv[2]:
        for ix in sys.argv[2:]:
            ixs = find_indexes(ix)
            if "open" not in ixs:
                continue
            for i in ixs["open"]:
                idxs.append(i)
except:
    types = {"close": {}, "open": {}}
    rest = {"close": [], "open": []}
    ixs = find_indexes("cmssdt-*")
    for k in ixs:
        for idx in ixs[k]:
            m = re.match(r"^(.+)[_-]([\d]+)$", idx)
            if m:
                ix = m.group(1)
                wk = m.group(2)
                if k not in types:
                    types[k] = {}
                if ix not in types[k]:
                    types[k][ix] = []
                types[k][ix].append(wk)
                if ix in ignore_index:
                    continue
                if (k == "open") and ((cur_week - int(wk)) > weeks):
                    idxs.append(idx)
                if (k == "close") and ((cur_week - int(wk)) <= weeks):
                    odxs.append(idx)
            else:
                if k not in rest:
                    rest[k] = []
                rest[k].append(idx)
    for k in rest:
        print("REST:", k, ":", sorted(rest[k]))
    for k in types:
        for ix in sorted(types[k].keys()):
            print("WEEK:", k, ":", ix, sorted(types[k][ix]))

for idx in sorted(idxs):
    print("Closing ", idx)
    close_index(idx)
    print("  ", get_indexes(idx).strip())

for idx in sorted(odxs):
    print("Opening ", idx)
    open_index(idx)
    print("  ", get_indexes(idx).strip())
