# -*- coding: utf-8 -*-
# Home-made test.
import math
from rough_calculations import ng_isolated_footing as za

footing= za.IsolatedFooting(1.0)
iBeta01= footing.getNearSlopeReductionFactor(math.radians(30),8*footing.Lzapata)
iBeta02= footing.getNearSlopeReductionFactor(math.atan(2/3.0),0.0)

ratio1= (iBeta01-1.0)/1.0
ratio2= (iBeta02-0.2)/0.2

# print "iBeta01= ", iBeta01
# print "ratio1= ", ratio1
# print "iBeta02= ", iBeta02
# print "ratio2= ", ratio2


import os
fname= os.path.basename(__file__)
if (abs(ratio1)<1e-11) and (abs(ratio2)<1e-11):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
