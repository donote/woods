#!/usr/bin/env python
"""
Time: 2018.03.05
Author: Harry.liu
Description: using pyfpgrowth for frequent pattern data mine
Usage: cat data/data_fpgrowth.txt | python lib/fpgrowth.py
"""

import sys
import pickle
import pyfpgrowth

# modify this two threholds
SUPPORT = 50
CONFIDENCE = 0.70

def data_prep():
    """
    input: terms string split with SPACE
    output: [[term1, term2, ...], [term1, term2, ...] ...]
    """
    trans = []
    for line in sys.stdin:
        line = line.strip()
        terms = line.split(' ')
        if len(terms) != 0:
            trans.append(terms)
    return trans


def pattern_mine(trans, support, confidence):
    """
    input: [[term1, term2, ...], [term1, term2, ...] ...]
    output: 
    """
    pattern = pyfpgrowth.find_frequent_patterns(trans, support)
    rule = pyfpgrowth.generate_association_rules(pattern, confidence)
    return pattern, rule


def print_result(rule):
    """
    DESC: print result of format 'sourceitem \t confidence \t item1 item2 ...'
    """
    for k, v in rule.items():
        items = " ".join(list(k))
        sitem = " ".join(list(v[0]))
        score = v[1]
        print('%s\t%s\t%s' % (sitem, score, items))


def save_result(rule, filename):
    """
    DESC: using pickle to save rule to filename
    """
    fd = open(filename, 'w')
    pickle.dump(rule, fd)


if __name__ == "__main__":
    trans = data_prep()
    pattern, rule = pattern_mine(trans, SUPPORT, CONFIDENCE)
    save_result(rule, 'data/data.pkl')
    print_result(rule)

