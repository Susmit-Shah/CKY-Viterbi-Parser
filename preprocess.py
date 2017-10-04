#!/usr/bin/env python

import sys, fileinput
import tree

for line in fileinput.input():
    t = tree.Tree.from_str(line)

    # Binarize, inserting 'X*' nodes.
    t.binarize()

    # Remove unary nodes
    t.remove_unit()

    # The tree is now strictly binary branching, so that the CFG is in Chomsky normal form.

    t.vertical_markov(t.root)
    #t.horizontal_markov(t.root)

    # Make sure that all the roots still have the same label.
    assert t.root.label == 'TOP'

    print t
    
    
