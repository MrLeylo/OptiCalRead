#!/usr/bin/env python

import pytemplate as temp
from pprint import pprint
import matplotlib.pyplot as plt

update=1
sureUpdate=1
sureSureUpdate=1
if update==1 and sureUpdate==1 and sureSureUpdate==1:
	temp.templateGenerator()
symboldB,tagClassification,averages=temp.readTemplate()
print averages['b1']
#plt.figure(1)
#for j in range(len(tagClassification['r1'][0].tE)):
#	if j==0:
#		ini=-1
#	else:
#		ini=int(tagClassification['r1'][0].tE[j-1])
#	plt.plot(averages['r1'][range(ini+1,int(tagClassification['r1'][0].tE[j])+1),0],-averages['r1'][range(ini+1,int(tagClassification['r1'][0].tE[j])+1),1],'r')
#plt.show()
