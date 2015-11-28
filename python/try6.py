#!/usr/bin/env python

import pytemplate as temp
import featurePonderation as fP

symboldB,tagClassification,averages=temp.readTemplate()
fP.findConcentration(tagClassification)
