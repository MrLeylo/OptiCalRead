#!/usr/bin/env python

import pytemplate as temp
import os

symboldB,tagClassification,averages=temp.readTemplate()
if os.path.isfile('symbolDictionary.txt'):
	os.remove('symbolDictionary.txt')
dicti=open('symbolDictionary.txt','w')
for s in tagClassification:
	dicti.write(s+'\n')
dicti.close()
