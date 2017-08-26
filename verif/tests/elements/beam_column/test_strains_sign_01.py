# -*- coding: utf-8 -*-
# home made test

# ForceBeamColum3d element sign criteria.

#     Axial and shear forces have the same direction and sense that
#     the local axes.
#     Mx torque and My bending moment have the same direction and sense
#     that the local axes.
#     Bending moment Mz has the same direction and its sense is the OPPOSITE to local Z axis.
#     Section's y axis is element z axis.
#Section scheme:

#             y
#             ^
#             |
#             |
#       o 3   |     o 2
#             |
# z<----------+
#             
#       o 4         o 1
# 

from __future__ import division
import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from materials import typical_materials
from postprocess import prop_statistics

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2015, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

# Material properties
E= 2.1e6 # Elastic modulus (Pa)
epsilon= 3.5e-3
sigma= E*epsilon

# Cross section properties
width= 4
depth= 2
fiberArea= 1e-4 # Área de cada fibra (m2)
A= 4*fiberArea # Área de cada fibra (m2)
Iy= 4*(fiberArea*(width/2.0)**2) # Cross section moment of inertia (m4)
Iz= 4*(fiberArea*(depth/2.0)**2) # Cross section moment of inertia (m4)

F= sigma*fiberArea
N= 4*F
My= 0.0
Mz= 0.0

L= 1.0 # Bar length (m)

# Problem type
prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor   

# Materials definition
elast= typical_materials.defElasticMaterial(preprocessor, "elast",E)

# Fibers
y1= -depth/2.0
z1= -width/2.0
fourFibersSection= preprocessor.getMaterialLoader.newMaterial("fiber_section_3d","fourFibersSection")

f1= fourFibersSection.addFiber("elast",fiberArea,xc.Vector([y1,z1]))
f2= fourFibersSection.addFiber("elast",fiberArea,xc.Vector([-y1,z1]))
f3= fourFibersSection.addFiber("elast",fiberArea,xc.Vector([-y1,-z1]))
f4= fourFibersSection.addFiber("elast",fiberArea,xc.Vector([y1,-z1]))


f1.getMaterial().setTrialStrain(epsilon,0.0)
f2.getMaterial().setTrialStrain(epsilon,0.0)
f3.getMaterial().setTrialStrain(epsilon,0.0)
f4.getMaterial().setTrialStrain(epsilon,0.0)

N0= fourFibersSection.getFibers().getResultant()
Mz0= fourFibersSection.getFibers().getMz(0.0)
My0= fourFibersSection.getFibers().getMy(0.0)

fourFibersSection.setupFibers()
RR= fourFibersSection.getStressResultant()
R0= xc.Vector([RR[0],RR[2],RR[1]])

fourFibersSection.revertToStart()
nodes= preprocessor.getNodeLoader
modelSpace= predefined_spaces.StructuralMechanics3D(nodes)
nodes.defaultTag= 1 #First node number.
nod= nodes.newNodeXYZ(0.0,0.0,0.0)
nod= nodes.newNodeXYZ(L,0.0,0.0)

lin= modelSpace.newLinearCrdTransf("lin",xc.Vector([0,1,0]))

# Elements definition
elements= preprocessor.getElementLoader
elements.defaultTransformation= "lin"
elements.defaultMaterial= "fourFibersSection"
zl= elements.newElement("force_beam_column_3d",xc.ID([1,2]))

# Constraints
modelSpace.fixNode000_000(1)
spc= modelSpace.constraints.newSPConstraint(2,1,0.0)
spc= modelSpace.constraints.newSPConstraint(2,2,0.0)
spc= modelSpace.constraints.newSPConstraint(2,3,0.0)


# Loads definition
cargas= preprocessor.getLoadLoader
casos= cargas.getLoadPatterns
#Load modulation.
ts= casos.newTimeSeries("constant_ts","ts")
casos.currentTimeSeries= "ts"
#Load case definition
lp0= casos.newLoadPattern("default","0")
lp0.newNodalLoad(2,xc.Vector([N,0,0,0,My,Mz])) #Section's y axis is element z axis.

#Add the load pattern to the domain.
casos.addToDomain("0")

# Solution
analisis= predefined_solutions.simple_static_linear(prueba)
result= analisis.analyze(1)

zl.getResistingForce()
section= zl.getSections()[0]

N1= section.getFibers().getResultant()
Mz1= section.getFibers().getMz(0.0)
My1= section.getFibers().getMy(0.0)

section.setupFibers()
RR= section.getStressResultant()
R1= xc.Vector([RR[0],RR[2],RR[1]])

vTeor= xc.Vector([N,My,Mz])
v0= xc.Vector([N0,My0,Mz0])
v1= xc.Vector([N1,My1,Mz1])

import math
error= math.sqrt((vTeor-v0).Norm2()+(vTeor-v1).Norm2()+(vTeor-R0).Norm2()+(vTeor-R1).Norm2())

'''
print "I= ", zl.getIVector
print "K= ", zl.getKVector
print "EA= ",E*A
print "EIz= ",E*Iz
print "EIy= ",E*Iy
print fourFibersSection.getInitialTangentStiffness()

print "v0= ",v0
print "v1= ",v1
print "R0= ",R0
print "R1= ",R1
print "vTeor= ", vTeor
print "error= ", error
'''

import os
from miscUtils import LogMessages as lmsg
fname= os.path.basename(__file__)
if (error < 1e-3):
  print "test ",fname,": ok."
else:
  lmsg.error(fname+' ERROR.')
