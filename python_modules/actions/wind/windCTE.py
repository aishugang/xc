# -*- coding: utf-8 -*-
from __future__ import division
'''Functions to compute wind actions according to Spanish CTE'''

import scipy.interpolate
import math

def ParamK(gae):
    '''
    Parámetro k en función del grado de aspereza del entorno
    according to CTE (table D.2).
    '''
    if gae==1:
          return 0.15
    elif gae==2:
          return 0.17
    elif gae==3:
          return 0.19
    elif gae==4:
          return 0.22
    elif gae==5:
          return 0.24
    else:
        print "Error en el grado de aspereza del entorno."
        return 0.0

def ParamL(gae):
    '''
    Parámetro L en función del grado de aspereza del entorno
    according to CTE (table D.2).}
    '''
    if gae==1:
          return 0.003
    elif gae==2:
          return 0.01
    elif gae==3:
          return 0.05
    elif gae==4:
          return 0.3
    elif gae==5:
          return 1.0
    else:
        print "Error en el grado de aspereza del entorno."
        return 0.0
      
def ParamZ(gae):
    '''
    Parámetro Z en función del grado de aspereza del entorno
    according to CTE (table D.2).
    '''
    if gae==1:
          return 1
    elif gae==2:
          return 1
    elif gae==3:
          return 2
    elif gae==4:
          return 5
    elif gae==5:
          return 10
    else:
      
        print "Error en el grado de aspereza del entorno."
        return 0.0
      
def ParamF(gae,z):
    '''
    Parámetro F en función del grado de aspereza del entorno
    y de la cota del punto according to CTE (expresión D.3).
    '''
    k= ParamK(gae)
    L= ParamL(gae)
    Z= ParamZ(gae)
    if z<Z:
        ZM= Z
    else:
        ZM= z
    return k*math.log(ZM/L)
  

def CoefExp(gae,z):
    '''
    Coeficiente de exposición en función del grado de aspereza del entorno
    y de la cota del punto sobre el terreno according to CTE (expresión D.2).
    '''
    if z>200:
        print "Expresión no válida para cotas sobre el terreno superiores a 200 m."
    k= ParamK(gae)
    F= ParamF(gae,z)
    return F*(F+7*k)

def interpolaCoefsPresion(A,Cpe1,Cpe10):
    '''
    Función para interpolar coeficientes de presión 
    according to expression D.4 of CTE (SE-AE-27).
    '''
    return Cpe1+(Cpe10-Cpe1)*math.log10(A)
  
'''
Coeficientes de presión exterior para una cubierta a dos aguas
according to table D.6 del CTE.
'''

#  FFFFFFF
#  F
#  F
#  FFFF
#  F
#  F
#  F

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona F de la cubierta 
para viento sensiblemente transversal (-45<theta<45) y
área mayor o igual a 10 metros cuadrados according to table D.6.
'''
x= []
y= []
x.append(math.radians(-45)); y.append(-0.6)
x.append(math.radians(-30)); y.append(-1.1)
x.append(math.radians(-15)); y.append(-2.5)
x.append(math.radians(-5)); y.append(-2.3)
x.append(math.radians(5)); y.append(-1.7)
x.append(math.radians(15)); y.append(-0.9)
x.append(math.radians(30)); y.append(-0.5)
x.append(math.radians(45)); y.append(-0.0)
x.append(math.radians(60)); y.append(0.7)
x.append(math.radians(75)); y.append(0.8)

cpDosAguasZonaFVTrsvAGrande= scipy.interpolate.interp1d(x,y)


'''
Coeficiente de presión exterior (positiva hacia abajo) en zona F de la cubierta 
para viento sensiblemente transversal (-45<theta<45) y
área menor o igual a 1 metro cuadrado according to table D.6.
'''

x= []
y= []
x.append(math.radians(-45)); y.append(-0.6)
x.append(math.radians(-30)); y.append(-2)
x.append(math.radians(-15)); y.append(-2.8)
x.append(math.radians(-5)); y.append(-2.5)
x.append(math.radians(5)); y.append(-2.5)
x.append(math.radians(15)); y.append(-2)
x.append(math.radians(30)); y.append(-1.5)
x.append(math.radians(45)); y.append(-0.0)
x.append(math.radians(60)); y.append(0.7)
x.append(math.radians(75)); y.append(0.8)
cpDosAguasZonaFVTrsvAPeq= scipy.interpolate.interp1d(x,y)

def ifte(cond,v1,v2):
  if(cond):
    return v1
  else:
    return v2

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona F de la cubierta 
para viento sensiblemente transversal (-45<theta<45) according to table D.6.
'''
def cpDosAguasZonaFVTrsv(A, alpha):
    cpPeq= cpDosAguasZonaFVTrsvAPeq(alpha)
    cpGrande= cpDosAguasZonaFVTrsvAGrande(alpha)
    return ifte(A<1,cpPeq,ifte(A>10,cpGrande,interpolaCoefsPresion(A,cpPeq,cpGrande)))

#  GGGGGGG
#  G
#  G
#  G   GGG
#  G     G
#  G     G
#  GGGGGGG

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona G de la cubierta 
para viento sensiblemente transversal (-45<theta<45) y
área mayor o igual a 10 metros cuadrados according to table D.6.
'''

x= []
y= []
x.append(math.radians(-45)); y.append(-0.6)
x.append(math.radians(-30)); y.append(-0.8)
x.append(math.radians(-15)); y.append(-1.3)
x.append(math.radians(-5)); y.append(-1.2)
x.append(math.radians(5)); y.append(-1.2)
x.append(math.radians(15)); y.append(-0.8)
x.append(math.radians(30)); y.append(-0.5)
x.append(math.radians(45)); y.append(-0.0)
x.append(math.radians(60)); y.append(0.7)
x.append(math.radians(75)); y.append(0.8)
cpDosAguasZonaGVTrsvAGrande= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona G de la cubierta 
para viento sensiblemente transversal (-45<theta<45) y
área menor o igual a 1 metro cuadrado according to table D.6.
'''

x= []
y= []
x.append(math.radians(-45)); y.append(-0.6)
x.append(math.radians(-30)); y.append(-1.5)
x.append(math.radians(-15)); y.append(-2)
x.append(math.radians(-5)); y.append(-2)
x.append(math.radians(5)); y.append(-2)
x.append(math.radians(15)); y.append(-1.5)
x.append(math.radians(30)); y.append(-1.5)
x.append(math.radians(45)); y.append(-0.0)
x.append(math.radians(60)); y.append(0.7)
x.append(math.radians(75)); y.append(0.8)
cpDosAguasZonaGVTrsvAPeq= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona G de la cubierta 
para viento sensiblemente transversal (-45<theta<45) according to table D.6.
'''
def cpDosAguasZonaGVTrsv(A, alpha):
    cpPeq= cpDosAguasZonaGVTrsvAPeq(alpha)
    cpGrande= cpDosAguasZonaGVTrsvAGrande(alpha)
    return ifte(A<1,cpPeq,ifte(A>10,cpGrande,interpolaCoefsPresion(A,cpPeq,cpGrande)))

#  H     H
#  H     H
#  H     H
#  HHHHHHH
#  H     H
#  H     H
#  H     H

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona H de la cubierta 
para viento sensiblemente transversal (-45<theta<45) y
área mayor o igual a 10 metros cuadrados according to table D.6.
'''

x= []
y= []
x.append(math.radians(-45)); y.append(-0.8)
x.append(math.radians(-30)); y.append(-0.8)
x.append(math.radians(-15)); y.append(-0.9)
x.append(math.radians(-5)); y.append(-0.8)
x.append(math.radians(5)); y.append(-0.6)
x.append(math.radians(15)); y.append(-0.3)
x.append(math.radians(30)); y.append(-0.2)
x.append(math.radians(45)); y.append(-0.0)
x.append(math.radians(60)); y.append(0.7)
x.append(math.radians(75)); y.append(0.8)
cpDosAguasZonaHVTrsvAGrande= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona H de la cubierta 
para viento sensiblemente transversal (-45<theta<45) y
área menor o igual a 1 metro cuadrado according to table D.6.
'''

x= []
y= []
x.append(math.radians(-45)); y.append(-0.8)
x.append(math.radians(-30)); y.append(-0.8)
x.append(math.radians(-15)); y.append(-1.2)
x.append(math.radians(-5)); y.append(-1.2)
x.append(math.radians(5)); y.append(-1.2)
x.append(math.radians(15)); y.append(-0.3)
x.append(math.radians(30)); y.append(-0.2)
x.append(math.radians(45)); y.append(-0.0)
x.append(math.radians(60)); y.append(0.7)
x.append(math.radians(75)); y.append(0.8)
cpDosAguasZonaHVTrsvAPeq= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona H de la cubierta 
para viento sensiblemente transversal (-45<theta<45) according to table D.6.
'''
def cpDosAguasZonaHVTrsv(A, alpha):
    cpPeq= cpDosAguasZonaHVTrsvAPeq(alpha)
    cpGrande= cpDosAguasZonaHVTrsvAGrande(alpha)
    return ifte(A<1,cpPeq,ifte(A>10,cpGrande,interpolaCoefsPresion(A,cpPeq,cpGrande)))

#  IIIII
#    I
#    I
#    I
#    I
#    I
#  IIIII

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona I de la cubierta 
para viento sensiblemente transversal (-45<theta<45) y
área mayor o igual a 10 metros cuadrados according to table D.6.
'''

x= []
y= []
x.append(math.radians(-45)); y.append(-0.7)
x.append(math.radians(-30)); y.append(-0.6)
x.append(math.radians(-15)); y.append(-0.5)
x.append(math.radians(-5)); y.append(0.2)
x.append(math.radians(5)); y.append(0.2)
x.append(math.radians(15)); y.append(-0.4)
x.append(math.radians(30)); y.append(-0.4)
x.append(math.radians(45)); y.append(-0.2)
x.append(math.radians(60)); y.append(-0.2)
x.append(math.radians(75)); y.append(-0.2)
cpDosAguasZonaIVTrsvAGrande= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona I de la cubierta 
para viento sensiblemente transversal (-45<theta<45) y
área menor o igual a 1 metro cuadrado according to table D.6.
'''

x= []
y= []
x.append(math.radians(-45)); y.append(-0.7)
x.append(math.radians(-30)); y.append(-0.6)
x.append(math.radians(-15)); y.append(-0.5)
x.append(math.radians(-5)); y.append(0.2)
x.append(math.radians(5)); y.append(0.2)
x.append(math.radians(15)); y.append(-0.4)
x.append(math.radians(30)); y.append(-0.4)
x.append(math.radians(45)); y.append(-0.2)
x.append(math.radians(60)); y.append(-0.2)
x.append(math.radians(75)); y.append(-0.2)
cpDosAguasZonaIVTrsvAPeq= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona I de la cubierta 
para viento sensiblemente transversal (-45<theta<45) according to table D.6.
'''
def cpDosAguasZonaIVTrsv(A, alpha):
    cpPeq= cpDosAguasZonaIVTrsvAPeq(alpha)
    cpGrande= cpDosAguasZonaIVTrsvAGrande(alpha)
    return ifte(A<1,cpPeq,ifte(A>10,cpGrande,interpolaCoefsPresion(A,cpPeq,cpGrande)))


#    JJJJ
#      J
#      J
#      J
#      J
#   J  J
#    JJ

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona J de la cubierta 
para viento sensiblemente transversal (-45<theta<45) y
área mayor o igual a 10 metros cuadrados according to table D.6.
'''

x= []
y= []
x.append(math.radians(-45)); y.append(-1)
x.append(math.radians(-30)); y.append(-0.8)
x.append(math.radians(-15)); y.append(-0.7)
x.append(math.radians(-5)); y.append(0.2)
x.append(math.radians(5)); y.append(0.2)
x.append(math.radians(15)); y.append(-1)
x.append(math.radians(30)); y.append(-0.5)
x.append(math.radians(45)); y.append(-0.3)
x.append(math.radians(60)); y.append(-0.3)
x.append(math.radians(75)); y.append(-0.3)
cpDosAguasZonaJVTrsvAGrande= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona J de la cubierta 
para viento sensiblemente transversal (-45<theta<45) y
área menor o igual a 1 metro cuadrado according to table D.6.
'''

x= []
y= []
x.append(math.radians(-45)); y.append(-1.5)
x.append(math.radians(-30)); y.append(-1.4)
x.append(math.radians(-15)); y.append(-1.2)
x.append(math.radians(-5)); y.append(0.2)
x.append(math.radians(5)); y.append(0.2)
x.append(math.radians(15)); y.append(-1.5)
x.append(math.radians(30)); y.append(-0.5)
x.append(math.radians(45)); y.append(-0.3)
x.append(math.radians(60)); y.append(-0.3)
x.append(math.radians(75)); y.append(-0.3)
cpDosAguasZonaJVTrsvAPeq= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona J de la cubierta 
para viento sensiblemente transversal (-45<theta<45) according to table D.6.
'''
def cpDosAguasZonaJVTrsv(A, alpha):
    cpPeq= cpDosAguasZonaJVTrsvAPeq(alpha)
    cpGrande= cpDosAguasZonaJVTrsvAGrande(alpha)
    return ifte(A<1,cpPeq,ifte(A>10,cpGrande,interpolaCoefsPresion(A,cpPeq,cpGrande)))


#  FFFFFFF
#  F
#  F
#  FFFF
#  F
#  F
#  F

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona F de la cubierta 
para viento sensiblemente longitudinal (45<theta<135) y
área mayor o igual a 10 metros cuadrados according to table D.6.
'''

x= []
y= []
x.append(math.radians(-45)); y.append(-1.4)
x.append(math.radians(-30)); y.append(-1.5)
x.append(math.radians(-15)); y.append(-1.9)
x.append(math.radians(-5)); y.append(-1.8)
x.append(math.radians(5)); y.append(-1.6)
x.append(math.radians(15)); y.append(-1.3)
x.append(math.radians(30)); y.append(-1.1)
x.append(math.radians(45)); y.append(-1.1)
x.append(math.radians(60)); y.append(-1.1)
x.append(math.radians(75)); y.append(-1.1)
cpDosAguasZonaFVLongAGrande= scipy.interpolate.interp1d(x,y)


'''
Coeficiente de presión exterior (positiva hacia abajo) en zona F de la cubierta 
para viento sensiblemente longitudinal (45<theta<135) y
área menor o igual a 1 metro cuadrado according to table D.6.
'''

x= []
y= []
x.append(math.radians(-45)); y.append(-2.0)
x.append(math.radians(-30)); y.append(-2.1)
x.append(math.radians(-15)); y.append(-2.5)
x.append(math.radians(-5)); y.append(-2.5)
x.append(math.radians(5)); y.append(-2.2)
x.append(math.radians(15)); y.append(-2)
x.append(math.radians(30)); y.append(-1.5)
x.append(math.radians(45)); y.append(-1.5)
x.append(math.radians(60)); y.append(-1.5)
x.append(math.radians(75)); y.append(-1.5)
cpDosAguasZonaFVLongAPeq= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona F de la cubierta 
para viento sensiblemente longitudinal (45<theta<135) according to table D.6.
'''
def cpDosAguasZonaFVLong(A, alpha):
    cpPeq= cpDosAguasZonaFVLongAPeq(alpha)
    cpGrande= cpDosAguasZonaFVLongAGrande(alpha)
    return ifte(A<1,cpPeq,ifte(A>10,cpGrande,interpolaCoefsPresion(A,cpPeq,cpGrande)))

#  GGGGGGG
#  G
#  G
#  G   GGG
#  G     G
#  G     G
#  GGGGGGG

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona G de la cubierta 
para viento sensiblemente longitudinal (45<theta<135) y
área mayor o igual a 10 metros cuadrados according to table D.6.
'''

x= []
y= []
x.append(math.radians(-45)); y.append(-1.2)
x.append(math.radians(-30)); y.append(-1.2)
x.append(math.radians(-15)); y.append(-1.2)
x.append(math.radians(-5)); y.append(-1.2)
x.append(math.radians(5)); y.append(-1.3)
x.append(math.radians(15)); y.append(-1.3)
x.append(math.radians(30)); y.append(-1.4)
x.append(math.radians(45)); y.append(-1.4)
x.append(math.radians(60)); y.append(-1.2)
x.append(math.radians(75)); y.append(-1.2)
cpDosAguasZonaGVLongAGrande= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona G de la cubierta 
para viento sensiblemente longitudinal (45<theta<135) y
área menor o igual a 1 metro cuadrado according to table D.6.
'''

x= []
y= []
x.append(math.radians(-45)); y.append(-2)
x.append(math.radians(-30)); y.append(-2)
x.append(math.radians(-15)); y.append(-2)
x.append(math.radians(-5)); y.append(-2)
x.append(math.radians(5)); y.append(-2)
x.append(math.radians(15)); y.append(-2)
x.append(math.radians(30)); y.append(-2)
x.append(math.radians(45)); y.append(-2)
x.append(math.radians(60)); y.append(-2)
x.append(math.radians(75)); y.append(-2)
cpDosAguasZonaGVLongAPeq= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona G de la cubierta 
para viento sensiblemente longitudinal (45<theta<135) according to table D.6.
'''
def cpDosAguasZonaGVLong(A, alpha):
    cpPeq= cpDosAguasZonaGVLongAPeq(alpha)
    cpGrande= cpDosAguasZonaGVLongAGrande(alpha)
    return ifte(A<1,cpPeq,ifte(A>10,cpGrande,interpolaCoefsPresion(A,cpPeq,cpGrande)))

#  H     H
#  H     H
#  H     H
#  HHHHHHH
#  H     H
#  H     H
#  H     H

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona H de la cubierta 
para viento sensiblemente longitudinal (45<theta<135) y
área mayor o igual a 10 metros cuadrados according to table D.6.
'''

x= []
y= []
x.append(math.radians(-45)); y.append(-1)
x.append(math.radians(-30)); y.append(-1)
x.append(math.radians(-15)); y.append(-0.8)
x.append(math.radians(-5)); y.append(-0.7)
x.append(math.radians(5)); y.append(-0.7)
x.append(math.radians(15)); y.append(-0.6)
x.append(math.radians(30)); y.append(-0.8)
x.append(math.radians(45)); y.append(-0.9)
x.append(math.radians(60)); y.append(-0.8)
x.append(math.radians(75)); y.append(-0.8)
cpDosAguasZonaHVLongAGrande= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona H de la cubierta 
para viento sensiblemente longitudinal (45<theta<135) y
área menor o igual a 1 metro cuadrado according to table D.6.
'''

x= []
y= []
x.append(math.radians(-45)); y.append(-1.3)
x.append(math.radians(-30)); y.append(-1.3)
x.append(math.radians(-15)); y.append(-1.2)
x.append(math.radians(-5)); y.append(-1.2)
x.append(math.radians(5)); y.append(-1.2)
x.append(math.radians(15)); y.append(-1.2)
x.append(math.radians(30)); y.append(-1.2)
x.append(math.radians(45)); y.append(-1.2)
x.append(math.radians(60)); y.append(-1.0)
x.append(math.radians(75)); y.append(-1.0)
cpDosAguasZonaHVLongAPeq= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona H de la cubierta 
para viento sensiblemente longitudinal (45<theta<135) according to table D.6.
'''
def cpDosAguasZonaHVLong(A, alpha):
    cpPeq= cpDosAguasZonaHVLongAPeq(alpha)
    cpGrande= cpDosAguasZonaHVLongAGrande(alpha)
    return ifte(A<1,cpPeq,ifte(A>10,cpGrande,interpolaCoefsPresion(A,cpPeq,cpGrande)))

#  IIIII
#    I
#    I
#    I
#    I
#    I
#  IIIII

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona I de la cubierta 
para viento sensiblemente longitudinal (45<theta<135) y
área mayor o igual a 10 metros cuadrados according to table D.6.
'''

x= []
y= []
x.append(math.radians(-45)); y.append(-0.9)
x.append(math.radians(-30)); y.append(-0.9)
x.append(math.radians(-15)); y.append(-0.8)
x.append(math.radians(-5)); y.append(-0.6)
x.append(math.radians(5)); y.append(-0.6)
x.append(math.radians(15)); y.append(-0.5)
x.append(math.radians(30)); y.append(-0.5)
x.append(math.radians(45)); y.append(-0.5)
x.append(math.radians(60)); y.append(-0.5)
x.append(math.radians(75)); y.append(-0.5)
cpDosAguasZonaIVLongAGrande= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona I de la cubierta 
para viento sensiblemente longitudinal (45<theta<135) y
área menor o igual a 1 metro cuadrado according to table D.6.
'''

x= []
y= []
x.append(math.radians(-45)); y.append(-1.2)
x.append(math.radians(-30)); y.append(-1.2)
x.append(math.radians(-15)); y.append(-1.2)
x.append(math.radians(-5)); y.append(-1.2)
x.append(math.radians(5)); y.append(-0.6)
x.append(math.radians(15)); y.append(-0.5)
x.append(math.radians(30)); y.append(-0.5)
x.append(math.radians(45)); y.append(-0.5)
x.append(math.radians(60)); y.append(-0.5)
x.append(math.radians(75)); y.append(-0.5)
cpDosAguasZonaIVLongAPeq= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona I de la cubierta 
para viento sensiblemente longitudinal (45<theta<135) according to table D.6.
'''
def cpDosAguasZonaIVLong(A, alpha):
    cpPeq= cpDosAguasZonaIVLongAPeq(alpha)
    cpGrande= cpDosAguasZonaIVLongAGrande(alpha)
    return ifte(A<1,cpPeq,ifte(A>10,cpGrande,interpolaCoefsPresion(A,cpPeq,cpGrande)))


#***********************************************************************
'''
Coeficientes de presión exterior para una cubierta plana
according to table D.4 del CTE. In this norm cover decks are
considered flat when the slope is less than five per cent.
'''
#***********************************************************************

#  FFFFFFF
#  F
#  F
#  FFFF
#  F
#  F
#  F

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona F de la cubierta 
para viento sensiblemente transversal (-45<theta<45) y
área mayor o igual a 10 metros cuadrados according to table D.4.
'''

x= []
y= []
x.append(0); y.append(-1.8)
x.append(0.025); y.append(-1.6)
x.append(0.05); y.append(-1.4)
x.append(0.1); y.append(-1.2)
cpPlanaZonaFVTrsvAGrande= scipy.interpolate.interp1d(x,y)


'''
Coeficiente de presión exterior (positiva hacia abajo) en zona F de la cubierta 
para viento sensiblemente transversal (-45<theta<45) y
área menor o igual a 1 metro cuadrado according to table D.4.
'''

x= []
y= []
x.append(0); y.append(-2.5)
x.append(0.025); y.append(-2.2)
x.append(0.05); y.append(-2.0)
x.append(0.1); y.append(-1.8)
cpPlanaZonaFVTrsvAPeq= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona F de la cubierta 
para viento sensiblemente transversal (-45<theta<45) according to table D.4.
'''
def cpPlanaZonaFVTrsv(A, hp, h):
    cpPeq= cpPlanaZonaFVTrsvAPeq(hp/h)
    cpGrande= cpPlanaZonaFVTrsvAGrande(hp/h)
    return ifte(A<1,cpPeq,ifte(A>10,cpGrande,interpolaCoefsPresion(A,cpPeq,cpGrande)))

#  GGGGGGG
#  G
#  G
#  G   GGG
#  G     G
#  G     G
#  GGGGGGG

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona G de la cubierta 
para viento sensiblemente transversal (-45<theta<45) y
área mayor o igual a 10 metros cuadrados according to table D.4.
'''

x= []
y= []
x.append(0); y.append(-1.2)
x.append(0.025); y.append(-1.2)
x.append(0.05); y.append(-0.9)
x.append(0.1); y.append(-0.8)
cpPlanaZonaGVTrsvAGrande= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona G de la cubierta 
para viento sensiblemente transversal (-45<theta<45) y
área menor o igual a 1 metro cuadrado according to table D.4.
'''

x= []
y= []
x.append(0); y.append(-2.0)
x.append(0.025); y.append(-1.8)
x.append(0.05); y.append(-1.6)
x.append(0.1); y.append(-1.4)
cpPlanaZonaGVTrsvAPeq= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona G de la cubierta 
para viento sensiblemente transversal (-45<theta<45) according to table D.4.
'''
def cpPlanaZonaGVTrsv(A, hp, h):
    cpPeq= cpPlanaZonaGVTrsvAPeq(hp/h)
    cpGrande= cpPlanaZonaGVTrsvAGrande(hp/h)
    return ifte(A<1,cpPeq,ifte(A>10,cpGrande,interpolaCoefsPresion(A,cpPeq,cpGrande)))

#  H     H
#  H     H
#  H     H
#  HHHHHHH
#  H     H
#  H     H
#  H     H

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona H de la cubierta 
para viento sensiblemente transversal (-45<theta<45) y
área mayor o igual a 10 metros cuadrados according to table D.4.
'''

x= []
y= []
x.append(0); y.append(-0.7)
x.append(0.025); y.append(-0.7)
x.append(0.05); y.append(-0.7)
x.append(0.1); y.append(-0.7)
cpPlanaZonaHVTrsvAGrande= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona H de la cubierta 
para viento sensiblemente transversal (-45<theta<45) y
área menor o igual a 1 metro cuadrado according to table D.4.
'''

x= []
y= []
x.append(0); y.append(-1.2)
x.append(0.025); y.append(-1.2)
x.append(0.05); y.append(-1.2)
x.append(0.1); y.append(-1.2)
cpPlanaZonaHVTrsvAPeq= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona H de la cubierta 
para viento sensiblemente transversal (-45<theta<45) according to table D.4.
'''
def cpPlanaZonaHVTrsv(A, hp, h):
    cpPeq= cpPlanaZonaHVTrsvAPeq(hp/h)
    cpGrande= cpPlanaZonaHVTrsvAGrande(hp/h)
    return ifte(A<1,cpPeq,ifte(A>10,cpGrande,interpolaCoefsPresion(A,cpPeq,cpGrande)))

#  IIIII
#    I
#    I
#    I
#    I
#    I
#  IIIII

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona I de la cubierta 
para viento sensiblemente transversal (-45<theta<45) y
área mayor o igual a 10 metros cuadrados according to table D.4.
'''

x= []
y= []
x.append(0); y.append(0.2)
x.append(0.025); y.append(0.2)
x.append(0.05); y.append(0.2)
x.append(0.1); y.append(0.2)
cpPlanaZonaIVTrsvAGrande= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona I de la cubierta 
para viento sensiblemente transversal (-45<theta<45) y
área menor o igual a 1 metro cuadrado according to table D.4.
'''

x= []
y= []
x.append(0); y.append(-0.2)
x.append(0.025); y.append(-0.2)
x.append(0.05); y.append(-0.2)
x.append(0.1); y.append(-0.2)
cpPlanaZonaIVTrsvAPeq= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en zona I de la cubierta 
para viento sensiblemente transversal (-45<theta<45) according to table D.4.
'''
def cpPlanaZonaIVTrsv(A, hp, h):
    cpPeq= cpPlanaZonaIVTrsvAPeq(hp/h)
    cpGrande= cpPlanaZonaIVTrsvAGrande(hp/h)
    return ifte(A<1,cpPeq,ifte(A>10,cpGrande,interpolaCoefsPresion(A,cpPeq,cpGrande)))


#  FFFFFFF
#  F
#  F
#  FFFF
#  F
#  F
#  F



'''
Coeficiente de presión exterior (positiva hacia abajo) en zona F de la cubierta 
para viento sensiblemente longitudinal (45<theta<135) according to table D.4.
'''
def cpPlanaZonaFVLong(A, hp, h):
    cpPeq= cpPlanaZonaFVTrsvAPeq(hp/h)
    cpGrande= cpPlanaZonaFVTrsvAGrande(hp/h)
    return ifte(A<1,cpPeq,ifte(A>10,cpGrande,interpolaCoefsPresion(A,cpPeq,cpGrande)))

#  GGGGGGG
#  G
#  G
#  G   GGG
#  G     G
#  G     G
#  GGGGGGG


'''
Coeficiente de presión exterior (positiva hacia abajo) en zona G de la cubierta 
para viento sensiblemente longitudinal (45<theta<135) according to table D.4.
'''
def cpPlanaZonaGVLong(A, hp, h):
    cpPeq= cpPlanaZonaGVTrsvAPeq(hp/h)
    cpGrande= cpPlanaZonaGVTrsvAGrande(hp/h)
    return ifte(A<1,cpPeq,ifte(A>10,cpGrande,interpolaCoefsPresion(A,cpPeq,cpGrande)))

#  H     H
#  H     H
#  H     H
#  HHHHHHH
#  H     H
#  H     H
#  H     H



'''
Coeficiente de presión exterior (positiva hacia abajo) en zona H de la cubierta 
para viento sensiblemente longitudinal (45<theta<135) according to table D.4.
'''
def cpPlanaZonaHVLong(A, hp, h):
    cpPeq= cpPlanaZonaHVTrsvAPeq(hp/h)
    cpGrande= cpPlanaZonaHVTrsvAGrande(hp/h)
    return ifte(A<1,cpPeq,ifte(A>10,cpGrande,interpolaCoefsPresion(A,cpPeq,cpGrande)))

#  IIIII
#    I
#    I
#    I
#    I
#    I
#  IIIII



'''
Coeficiente de presión exterior (positiva hacia abajo) en zona I de la cubierta 
para viento sensiblemente longitudinal (45<theta<135) according to table D.4.
'''
def cpPlanaZonaIVLong(A, hp, h):
    cpPeq= cpPlanaZonaIVTrsvAPeq(hp/h)
    cpGrande= cpPlanaZonaIVTrsvAGrande(hp/h)
    return ifte(A<1,cpPeq,ifte(A>10,cpGrande,interpolaCoefsPresion(A,cpPeq,cpGrande)))

#***********************************************************************
# Coeficientes de presión exterior para una marquesina a un agua according to table D.10 del CTE.
#***********************************************************************


'''
Down external pressure in the A zone of a shed marquee
as a function of the slope according to table table D.10.
'''

x= []
y= []
x.append(math.radians(0)); y.append(0.5)
x.append(math.radians(5)); y.append(0.8)
x.append(math.radians(10)); y.append(1.2)
x.append(math.radians(15)); y.append(1.4)
x.append(math.radians(20)); y.append(1.7)
x.append(math.radians(25)); y.append(2.0)
x.append(math.radians(30)); y.append(2.2)
cpMarq1AguaAbajoZonaA= scipy.interpolate.interp1d(x,y)

'''
Up external pressure in the A zone of a shed marquee
with zero obstruction factor as a function of the slope 
according to table table D.10.
'''

x= []
y= []
x.append(math.radians(0)); y.append(-0.6)
x.append(math.radians(5)); y.append(-1.1)
x.append(math.radians(10)); y.append(-1.5)
x.append(math.radians(15)); y.append(-1.8)
x.append(math.radians(20)); y.append(-2.2)
x.append(math.radians(25)); y.append(-2.6)
x.append(math.radians(30)); y.append(-3.0)
cpMarq1AguaArribaZonaAFi0= scipy.interpolate.interp1d(x,y)

'''
Up external pressure in the A zone of a shed marquee
with obstruction factor equal 1 as a function of the slope 
according to table table D.10.
'''

x= []
y= []
x.append(math.radians(0)); y.append(-1.5)
x.append(math.radians(5)); y.append(-1.6)
x.append(math.radians(10)); y.append(-2.1)
x.append(math.radians(15)); y.append(-1.6)
x.append(math.radians(20)); y.append(-1.6)
x.append(math.radians(25)); y.append(-1.5)
x.append(math.radians(30)); y.append(-1.5)
cpMarq1AguaArribaZonaAFi1= scipy.interpolate.interp1d(x,y)

'''
Up external pressure in the A zone of a shed marquee
as a function of the slope for any value of the obstruction
factor according to table table D.10.
'''
def cpMarq1AguaArribaZonaA(alpha, fi):
    v0= cpMarq1AguaArribaZonaAFi0(alpha)
    v1= cpMarq1AguaArribaZonaAFi1(alpha)
    return fi*(v1-v0)+v0


#***********************************************************************
# Coeficientes de presión exterior en paramentos verticales according to table D.3 del CTE.
#***********************************************************************

#    AA
#   A  A
#  A    A
#  A    A
#  AAAAAA
#  A    A
#  A    A

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona A
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área mayor o igual a 10 metros cuadrados en función de h/d according to table D.3.
'''

x= []
y= []
x.append(.25); y.append(-1.2)
x.append(1); y.append(-1.2)
x.append(5); y.append(-1.2)
cpParamVertZonaAVTrsvAGE10= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona A
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área igual a 5 metros cuadrados en función de h/d according to table D.3.
'''

x= []
y= []
x.append(.25); y.append(-1.3)
x.append(1); y.append(-1.3)
x.append(5); y.append(-1.3)
cpParamVertZonaAVTrsvAEQ5= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona A
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área igual a 2 metros cuadrados en función de h/d according to table D.3.
'''

x= []
y= []
x.append(.25); y.append(-1.3)
x.append(1); y.append(-1.3)
x.append(5); y.append(-1.3)
x.append(1e6); y.append(-1.3)
cpParamVertZonaAVTrsvAEQ2= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona A
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área menor o igual a 1 metro cuadrado en función de h/d according to table D.3.
'''

x= []
y= []
x.append(0); y.append(-1.4)
x.append(.25); y.append(-1.4)
x.append(1); y.append(-1.4)
x.append(5); y.append(-1.4)
x.append(1e6); y.append(-1.4)
cpParamVertZonaAVTrsvALE1= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en 
paramento vertical zona A para viento sensiblemente 
transversal (-45<theta<45) according to table D.3.
'''
def cpParamVertZonaAVTrsv(A, h, d):
    ratio= h/d
    cpLE1= cpParamVertZonaAVTrsvALE1(ratio)
    cpEQ2= cpParamVertZonaAVTrsvAEQ2(ratio)
    cpEQ5= cpParamVertZonaAVTrsvAEQ5(ratio)
    cpGE10= cpParamVertZonaAVTrsvAGE10(ratio)


    x= []
    y= []
    x.append(0); y.append(cpLE1)
    x.append(1); y.append(cpLE1)
    x.append(2); y.append(cpEQ2)
    x.append(5); y.append(cpEQ5)
    x.append(10); y.append(cpGE10)
    x.append(100); y.append(cpGE10)
    interpolacion= scipy.interpolate.interp1d(x,y)
    return interpolacion(A)

#  BBBBB
#  B    B
#  B   B
#  BBBB
#  B    B
#  B   B 
#  BBBB

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona B
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área mayor o igual a 10 metros cuadrados en función de h/d according to table D.3.
'''

x= []
y= []
x.append(.25); y.append(-0.8)
x.append(1); y.append(-0.8)
x.append(5); y.append(-0.8)
cpParamVertZonaBVTrsvAGE10= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona B
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área igual a 5 metros cuadrados en función de h/d according to table D.3.
'''

x= []
y= []
x.append(.25); y.append(-0.9)
x.append(1); y.append(-0.9)
x.append(5); y.append(-0.9)
cpParamVertZonaBVTrsvAEQ5= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona B
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área igual a 2 metros cuadrados en función de h/d according to table D.3.
'''

x= []
y= []
x.append(.25); y.append(-1)
x.append(1); y.append(-1)
x.append(5); y.append(-1)
cpParamVertZonaBVTrsvAEQ2= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona B
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área menor o igual a 1 metro cuadrado en función de h/d according to table D.3.
'''

x= []
y= []
x.append(.25); y.append(-1.1)
x.append(1); y.append(-1.1)
x.append(5); y.append(-1.1)
cpParamVertZonaBVTrsvALE1= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en 
paramento vertical zona B para viento sensiblemente 
transversal (-45<theta<45) according to table D.3.
'''
def cpParamVertZonaBVTrsv(A, h, d):
    ratio= h/d
    cpLE1= cpParamVertZonaBVTrsvALE1(ratio)
    cpEQ2= cpParamVertZonaBVTrsvAEQ2(ratio)
    cpEQ5= cpParamVertZonaBVTrsvAEQ5(ratio)
    cpGE10= cpParamVertZonaBVTrsvAGE10(ratio)

    x= []
    y= []
    x.append(0); y.append(cpLE1)
    x.append(1); y.append(cpLE1)
    x.append(2); y.append(cpEQ2)
    x.append(5); y.append(cpEQ5)
    x.append(10); y.append(cpGE10)
    x.append(100); y.append(cpGE10)
    interpolacion= scipy.interpolate.interp1d(x,y)
    return interpolacion(A)

#   CCC
#  C   C
#  C   
#  C
#  C    
#  C   C 
#   CCC

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona C
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área mayor o igual a 10 metros cuadrados en función de h/d according to table D.3.
'''

x= []
y= []
x.append(.25); y.append(-0.5)
x.append(1); y.append(-0.5)
x.append(5); y.append(-0.5)
cpParamVertZonaCVTrsvAGE10= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona C
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área igual a 5 metros cuadrados en función de h/d according to table D.3.
'''

x= []
y= []
x.append(.25); y.append(-0.5)
x.append(1); y.append(-0.5)
x.append(5); y.append(-0.5)
cpParamVertZonaCVTrsvAEQ5= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona C
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área igual a 2 metros cuadrados en función de h/d according to table D.3.
'''

x= []
y= []
x.append(.25); y.append(-0.5)
x.append(1); y.append(-0.5)
x.append(5); y.append(-0.5)
cpParamVertZonaCVTrsvAEQ2= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona C
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área menor o igual a 1 metro cuadrado en función de h/d according to table D.3.
'''

x= []
y= []
x.append(.25); y.append(-0.5)
x.append(1); y.append(-0.5)
x.append(5); y.append(-0.5)
cpParamVertZonaCVTrsvALE1= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en 
paramento vertical zona C para viento sensiblemente 
transversal (-45<theta<45) according to table D.3.
'''
def cpParamVertZonaCVTrsv(A, h, d):
    ratio= h/d

    cpLE1= cpParamVertZonaCVTrsvALE1(ratio)
    cpEQ2= cpParamVertZonaCVTrsvAEQ2(ratio)
    cpEQ5= cpParamVertZonaCVTrsvAEQ5(ratio)
    cpGE10= cpParamVertZonaCVTrsvAGE10(ratio)


    x= []
    y= []
    x.append(0); y.append(cpLE1)
    x.append(1); y.append(cpLE1)
    x.append(2); y.append(cpEQ2)
    x.append(5); y.append(cpEQ5)
    x.append(10); y.append(cpGE10)
    x.append(100); y.append(cpGE10)
    interpolacion= scipy.interpolate.interp1d(x,y)
    return interpolacion(A)

#  DDDD
#  D   D
#  D   D
#  D   D
#  D   D
#  D   D 
#  DDDD

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona D
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área mayor o igual a 10 metros cuadrados en función de h/d according to table D.3.
'''

x= []
y= []
x.append(0); y.append(0.7)
x.append(.25); y.append(0.7)
x.append(1); y.append(0.8)
x.append(5); y.append(0.8)
cpParamVertZonaDVTrsvAGE10= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona D
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área igual a 5 metros cuadrados en función de h/d according to table D.3.
'''

x= []
y= []
x.append(0); y.append(0.8)
x.append(.25); y.append(0.8)
x.append(1); y.append(0.9)
x.append(5); y.append(0.9)
cpParamVertZonaDVTrsvAEQ5= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona D
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área igual a 2 metros cuadrados en función de h/d according to table D.3.
'''

x= []
y= []
x.append(0); y.append(0.7)
x.append(.25); y.append(0.7)
x.append(1); y.append(0.9)
x.append(5); y.append(0.9)
cpParamVertZonaDVTrsvAEQ2= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona D
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área menor o igual a 1 metro cuadrado en función de h/d according to table D.3.
'''

x= []
y= []
x.append(.25); y.append(1)
x.append(1); y.append(1)
x.append(5); y.append(1)
cpParamVertZonaDVTrsvALE1= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en 
paramento vertical zona D para viento sensiblemente 
transversal (-45<theta<45) according to table D.3.
'''
def cpParamVertZonaDVTrsv(A, h, d):
    ratio= h/d

    cpLE1= cpParamVertZonaDVTrsvALE1(ratio)
    cpEQ2= cpParamVertZonaDVTrsvAEQ2(ratio)
    cpEQ5= cpParamVertZonaDVTrsvAEQ5(ratio)
    cpGE10= cpParamVertZonaDVTrsvAGE10(ratio)


    x= []
    y= []
    x.append(0); y.append(cpLE1)
    x.append(1); y.append(cpLE1)
    x.append(2); y.append(cpEQ2)
    x.append(5); y.append(cpEQ5)
    x.append(10); y.append(cpGE10)
    x.append(100); y.append(cpGE10)
    interpolacion= scipy.interpolate.interp1d(x,y)
    return interpolacion(A)

#  EEEEE
#  E   
#  E   
#  EEE
#  E   
#  E    
#  EEEEE

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona E
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área mayor o igual a 10 metros cuadrados en función de h/d according to table D.3.
'''

x= []
y= []
x.append(0); y.append(-0.3)
x.append(.25); y.append(-0.3)
x.append(1); y.append(-0.5)
x.append(5); y.append(-0.7)
cpParamVertZonaEVTrsvAGE10= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona E
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área igual a 5 metros cuadrados en función de h/d according to table D.3.
'''

x= []
y= []
x.append(.25); y.append(-0.3)
x.append(0); y.append(-0.3)
x.append(1); y.append(-0.5)
x.append(5); y.append(-0.7)
cpParamVertZonaEVTrsvAEQ5= scipy.interpolate.interp1d(x,y)

'''Coeficiente de presión exterior (positiva hacia adentro) en zona E
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área igual a 2 metros cuadrados en función de h/d according to table D.3.
'''

x= []
y= []
x.append(0); y.append(-0.3)
x.append(.25); y.append(-0.3)
x.append(1); y.append(-0.5)
x.append(5); y.append(-0.7)
cpParamVertZonaEVTrsvAEQ2= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia adentro) en zona E
paramento vertical para viento sensiblemente transversal (-45<theta<45) y
área menor o igual a 1 metro cuadrado en función de h/d according to table D.3.
'''

x= []
y= []
x.append(0); y.append(-0.3)
x.append(.25); y.append(-0.3)
x.append(1); y.append(-0.5)
x.append(5); y.append(-0.7)
cpParamVertZonaEVTrsvALE1= scipy.interpolate.interp1d(x,y)

'''
Coeficiente de presión exterior (positiva hacia abajo) en 
paramento vertical zona E para viento sensiblemente 
transversal (-45<theta<45) according to table D.3.
'''
def cpParamVertZonaEVTrsv(A, h, d):
    ratio= h/d

    cpLE1= cpParamVertZonaEVTrsvALE1(ratio)
    cpEQ2= cpParamVertZonaEVTrsvAEQ2(ratio)
    cpEQ5= cpParamVertZonaEVTrsvAEQ5(ratio)
    cpGE10= cpParamVertZonaEVTrsvAGE10(ratio)

    x= []
    y= []
    x.append(0); y.append(cpLE1)
    x.append(1); y.append(cpLE1)
    x.append(2); y.append(cpEQ2)
    x.append(5); y.append(cpEQ5)
    x.append(10); y.append(cpGE10)
    x.append(100); y.append(cpGE10)
    interpolacion= scipy.interpolate.interp1d(x,y)
    return interpolacion(A)

