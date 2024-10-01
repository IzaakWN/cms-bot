#!/usr/bin/env python3
import sys
from argparse import ArgumentParser
from collections import defaultdict

from categories_map import CMSSW_CATEGORIES


def package2category(filename):
    if not filename:
        return
    file_pack = "/".join(filename.split("/")[:2])
    cat = "unknown"
    if file_pack in pack2cat:
        cat = "-".join(sorted(pack2cat[file_pack]))
    cats[cat].add(file_pack)


parser = ArgumentParser()
parser.add_argument("-i", "--stdin", action="store_true", help="Also read file name(s) from stdin")
parser.add_argument("files", nargs="*", help="File name(s)")
args = parser.parse_args()

pack2cat = defaultdict(list)
for cat in CMSSW_CATEGORIES:
    for pack in CMSSW_CATEGORIES[cat]:
        pack2cat[pack].append(cat)

cats = defaultdict(set)

for line in args.files:
    package2category(line.strip())

if args.stdin:
    for line in sys.stdin:
        package2category(line.strip())

for cat in cats:
    print("%s %s" % (cat, " ".join(cats[cat])))
