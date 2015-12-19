# -*- coding: utf-8 -*-
# Concrete according to EHE-08.
from __future__ import division

__author__= "Ana Ortega (AOO) and Luis C. Pérez Tato (LCPT)"
__cppyright__= "Copyright 2015, AOO and LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"



import math
import scipy.interpolate
from materials import concreteBase

class EHEConcrete(concreteBase.Concrete):
    """ Concrete model according to EHE
    Attributes:
        typeAggregate:types of aggregate= 
            "cuarcita", "arenisca", "caliza normal", 
            "caliza densa", "volcanica porosa", 
            "volcanica normal", "granito", "diabasa"

    """
    typeAggregate='cuarcita'

    def getAlphaEcm(self):
        '''getAlphaEcm()
        Coeficiente corrector del módulo de deformación
        longitudinal del hormigón en función de la naturaleza
        del árido.
        '''
        if self.typeAggregate=="cuarcita":
            return 1
        elif self.typeAggregate=="arenisca":
            return 0.7
        elif self.typeAggregate=="caliza normal":
            return 0.9
        elif self.typeAggregate=="caliza densa":
            return 1.2
        elif self.typeAggregate=="volcanica porosa":
            return 0.9
        elif self.typeAggregate=="volcanica normal":
            return 1.2
        elif self.typeAggregate=="granito":
            return 1.1
        elif self.typeAggregate=="diabasa":
            return 1.3
        else:
            print "Error en tipo de árido."
            return 0.0

    def getEcm(self):
        """Módulo de deformación longitudinal secante a 28 días expresado
        en [Pa] [+] de acuerdo con el artículo 39.6 de EHE-08."""
        fcmMPa=abs(self.getFcm())*1e-6
        return 8500*(fcmMPa**(1/3))*1e6

    def getEc0(self):
        '''Módulo de deformación longitudinal inicial a 28 días expresado
        en [Pa] [+] de acuerdo con el artículo 39.6 de EHE-08.
        '''
        return self.getAlphaEcm()*self.getEcm()

    def getEcmT(self,t):
        '''Módulo de deformación longitudinal secante a t días expresado
        en [Pa] [+] de acuerdo con los comentarios al artículo 39.6 de EHE-08.
        Attributes:
            t: Edad del hormigón expresada en días.
        '''
        return math.pow(self.getBetaCC(t),0.3)*self.getEcm()

    def getFctm(self):
        """Fctm: mean tensile strength [Pa][+]
        (art. 39.1 EHE)
        """
        if self.fckMPa()<= 50:
            return 0.3*self.fckMPa()**(2.0/3.0)*1e6
        else:
            return 0.58*(self.fckMPa()**(1.0/2.0))*1e6

    def fctkInf(self):
        """Resistencia característica inferior del hormigón a tracción [Pa][+]
        (según artículo 39.1 EHE)
        """
        return 0.21e6*(self.fckMPa())**(2.0/3.0)

    def fctkSup(self):
        """Resistencia característica superior del hormigón a tracción [Pa][+]
        (según artículo 39.1 EHE)
        """
        return 0.39e6*(self.fckMPa())**(2.0/3.0)

    def fctMedEHE08(self):
        """Resistencia media del hormigón a tracción  [Pa][+]
        (según artículo 39.1 EHE-08)
        """
        if self.fckMPa()<50:
            return 0.30e6*self.fckMPa()**(2/3)
        else:
            return 0.58e6*self.fckMPa()**(1/2)

    def fctkEHE08(self):
        """Resistencia característica del hormigón a tracción  [Pa][+]
        (según artículo 39.1 EHE-08)
        """
        return 0.7*self.fctMedEHE08()

    def getEpsc2(self):
        """
        epsc2: strain [-] at peak stress at parabola-rectangle diagram 
        (art. 39.5 EHE, figure 39.5.a EHE)
        """
        if self.fckMPa()<=50:
            return (2.0)*(-1e-3)
        else:
            return (2.0+0.085*(self.fckMPa()-50)**0.50)*(-1e-3)

    def getExpN(self):
        """
        expN: exponent n for the parabola-rectangle diagram 
        (art. 39.5 EHE, figure 39.5.a EHE)
        """
        if self.fckMPa()<=50:
            return 2.0
        else:
            return 1.4+9.6*((100-self.fckMPa())/100)**4

    def getEpscu2(self):
        """
        epscu2: nominal ultimate strain [-] at parabola-rectangle diagram 
        (art. 39.5 EHE, figure 39.5.a EHE)
        """
        if self.fckMPa()<=50:
            return 3.5*(-1e-3)
        else:
            return (2.6+14.4*((100-self.fckMPa())/100)**4)*(-1e-3)

#    def tangDConcrete(self,eps):
#        """Diagrama característico tensión deformación del hormigón según EHE."""
#        return tangc(eps,self.fcd())

#Parabola-rectangle diagrams for concrete under compression 
    # def sigmac(self,eps):
    #     '''Stress [Pa][-] from parabola-rectangle diagram
    #     Atributtes:
    #         eps: strain [-]
    #     '''
    #     if(eps<0):
    #         if(eps>self.getEpsc2()):
    #             return -850*self.fcd()*eps*(250*eps+1)
    #         else:
    #             return 0.85*self.fcd()
    #     else:
    #         return 0.0 

    # def tangc(self,eps):
    #     if(eps<0):
    #       if(eps>self.getEpsc2()):
    #         return (-850*self.fcd()*(500*eps+1)) 
    #       else:
    #         return 0.0
    #     else:
    #       return 0.0 
    def getDeformacionFluencia(self, t,t0,RH,h0mm, sigmaT0):
        '''
        Devuelve el valor de la deformación por fluencia en el hormigón
        que se produce entre los instantes t0 y t.
        Attributes:
            t:     age of concrete in days at the moment considered
            t0:    age of concrete in days at loading
            RH:    ambient relative humidity(%)
            h0mm:  notional size of the member in mm
                   h0mm=2*Ac/u, where:
                        Ac= cross sectional area
                        u = perimeter of the member in contact with the atmosphere
                        sigmaT0: Tensión constante aplicada en t0.
        '''
        return sigmaT0*(1.0/self.getEcmT(t0)+self.getCreepFitt0(t,t0,RH,h0mm)/self.getEcm())
 

# EHE concretes
HA20= EHEConcrete("HA20",-20e6,1.5)
HA25= EHEConcrete("HA25",-25e6,1.5)
HA30= EHEConcrete("HA30",-30e6,1.5)
HA35= EHEConcrete("HA35",-35e6,1.5)
HA40= EHEConcrete("HA40",-40e6,1.5)
HA45= EHEConcrete("HA45",-45e6,1.5)
HA50= EHEConcrete("HA50",-50e6,1.5)
HA55= EHEConcrete("HA55",-55e6,1.5)
HA60= EHEConcrete("HA60",-60e6,1.5)
HA70= EHEConcrete("HA70",-70e6,1.5)
HA80= EHEConcrete("HA80",-80e6,1.5)
HA90= EHEConcrete("HA90",-90e6,1.5)
HA100= EHEConcrete("HA100",-100e6,1.5)

HP45= EHEConcrete("HP45",-55e6,1.5)
HP50= EHEConcrete("HP50",-50e6,1.5)


'''
Factor a aplicar a la resistencia característica del hormigón a compresión en función de su edad en días.
   para hormigones de endurecimiento normal (tabla 30.4.b EHE)
'''
x= [-1.0,0.0,3.0,7.0,28.0,90,360,361]
y= [0.0,0.0,0.4,0.65,1.0,1.2,1.35,1.35]
factorRCompJDiasNormal= scipy.interpolate.interp1d(x,y)

'''
Factor a aplicar a la resistencia característica del hormigón a compresión en función de su edad en días.
   para hormigones de endurecimiento rápido (tabla 30.4.b EHE)
'''
x= [-1.0,0.0,3.0,7.0,28.0,90,360,361]
y= [0.0,0.0,0.55,0.75,1.0,1.15,1.20,1.20]
factorRCompJDiasRapido=  scipy.interpolate.interp1d(x,y)

'''
Factor a aplicar a la resistencia característica del hormigón a tracción en función de su edad en días.
   para hormigones de endurecimiento normal(tabla 30.4.c EHE)
'''
x= [-1.0,0.0,3.0,7.0,28.0,90,360,361]
y= [0.0,0.0,0.4,0.7,1.0,1.05,1.10,1.10]
factorRTraccJDiasNormal= scipy.interpolate.interp1d(x,y)