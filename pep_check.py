#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import csv

if __name__ == '__main__':
    """Look for line overflows."""

    print """
████╗ █████╗████╗     ███╗ 
█╔══█╗█╔════█╔══█╗   █╔══█╗
████╔╝████╗ ████╔╝██╗ ███╔╝
█╔══╝ █╔══╝ █╔══╝ ╚═╝█╔══█╗
█║    █████╗█║        ███╔╝
╚╝    ╚════╝╚╝         ╚═╝ 
Overflow Inspector v1.0
    """

    # Validate arguments
    if len(sys.argv) < 3:
        print "Usage: %s <directory> <line_length>\n" \
              % sys.argv[0]
        sys.exit()
    PATH = sys.argv[1] # os.getcwd() # Current working directory
    PEP_LINE_LENGTH = int(sys.argv[2]) # 80
    FILE_EXT = '.py' # '.py'

    # Find files recursively
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(PATH)
                                     for f in filenames
                                        if os.path.splitext(f)[1] == FILE_EXT]

    # Find overflowing lines
    overflow = {}
    for file in files:
        with open(file) as f:
            for lineno, line in enumerate(f):
                if len(line) > PEP_LINE_LENGTH+1:
                    overflow.setdefault(file, []).append((lineno, line))

    # No overflow
    if not overflow:
        print "No overflow :)"
        sys.exit()

    # Write to CSV
    overflow_list = [['File', 'Line#', 'Length', 'Line']]
    for (key, value) in overflow.iteritems():
        overflow_list.extend([[key, v[0], len(v[1]), v[1]] for v in value])
    with open('pep_check.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(overflow_list)
    print "Files:"
    for k in overflow.keys():
        print os.path.abspath(k)
    print "Found: %s lines in %s files" % (len(overflow_list) - 1,
                                    len(overflow.keys()))
