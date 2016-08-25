#!/usr/bin/env python

import os
import sys
import random
import time
import urllib2

# Who is connection and query
if __name__ == "__main__":
    f=open(sys.argv[1], 'r')
    lines = f.readlines()
    for line in lines:
        line = line.rstrip('\n').rstrip('\r').rstrip()
        cmd = "./pywhois.py %s > whorecords/%s" % (line, line)
        #cmd = "whois -H %s > records/%s" % (line, line)
        try:
            print cmd
            os.system(cmd)
        except Exception:
            print "%s failed to resolve" % (line)
            pass
        time.sleep(random.randrange(0,3))
    f.close()
