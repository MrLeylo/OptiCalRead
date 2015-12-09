#!/usr/bin/env python
import SClass as nsi
import pyStructural as stru

testCase=[nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0])]
testCase[0].bBox=[0.75,4,1,3.5]
testCase[1].bBox=[1.75,2.25,0.75,1.25]
testCase[2].bBox=[2,2.25,3.5,4.5]
testCase[3].bBox=[3,3.5,3.75,4.5]
testCase[4].bBox=[2.5,2.75,3.75,4.1]
testCase[5].bBox=[4.5,5,1.25,3.5]
testCase[6].bBox=[5.5,6.75,2,3.25]
testCase[7].bBox=[7,7.5,1.5,2]
testCase[8].bBox=[7.5,8,1.5,2]
testCase[9].bBox=[7,7.25,2.75,3.25]
testCase[10].bBox=[8.25,9.25,2,2.75]
testCase[11].bBox=[10,11,1,75,3.9]
testCase[12].bBox=[11,11.5,1.25,1.75]
testCase[13].bBox=[11.75,12,1.25,2]
testCase[14].bBox=[11.4,11.6,2.75,3.5]
testCase[15].bBox=[12.5,12.75,1,4]
for ntc in range(len(testCase)):
	testCase[ntc].center=[(testCase[ntc].bBox[0]+testCase[ntc].bBox[1])/2.0,(testCase[ntc].bBox[2]+testCase[ntc].bBox[3])/2.0]
tags=['\sum1','n1','i2','01','=2','(1','x2','21','x2','i2','+2','y1','21','y1','i2',')1']
print stru.expreBuilder(testCase,tags)
