#!/usr/bin/env python

import sys, fileinput
import tree

for line in fileinput.input():
    t = tree.Tree.from_str(line)
    if t.root is None:
        print
        continue

    #t.remove_horizontal_markov(t.root)
    t.remove_vertical_markov(t.root)

    t.restore_unit()
    t.unbinarize()

    print t