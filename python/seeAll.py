#!/usr/bin/env python
import os
f=open('exampleLooker.txt')
line='o'
while line!='':
	line=f.readline()
	os.system('./overAll.py '+line)
