#!/usr/bin/env python

import pytemplate as temp
import sys
import repS as rs
import matplotlib.pyplot as plt

wanted=sys.argv[1]
print wanted
symboldB,tagClassification,averages=temp.readTemplate()
rs.repr([tagClassification[wanted][0]])
plt.show()
