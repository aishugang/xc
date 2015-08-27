# -*- coding: utf-8 -*-

#Based on sXML-master projet on gitHub

import Definition as df
import NodeContainer as nCtr
import EPPlaneContainer as eppc
import NodeSupportContainer as nsc
import ProjectProperties as prjDef
import xml.etree.cElementTree as ET

class SXMLMesh:
  def __init__(self,xmlns, defn,mesh):
    self.xmlns= xmlns
    self.uuid= ''
    self.defn= defn
    self.nodeContainer= nCtr.NodeContainer(mesh.nodes)
    self.epPlaneContainer= eppc.EPPlaneContainer(mesh.cells)
    self.nodeSupportContainer= nsc.NodeSupportContainer(mesh.nodeSupports)
    self.fileName= ''

  def getXMLElement(self,defFileName):
    project= ET.Element("project")
    project.set("xmlns",self.xmlns)
    df= ET.SubElement(project,"def")
    df.set("uri",defFileName)
    containers= [self.nodeContainer,self.epPlaneContainer]
    for c in containers:
      elem= c.getXMLElement(project)
    return project

  def getXMLTree(self,defFileName):
    project= self.getXMLElement(defFileName)
    tree = ET.ElementTree(project)
    return tree

  def getFileName(self):
    return self.fileName

  def getDefFileName(self):
    return self.fileName + ".def"

  def writeXMLFile(self): 
    defFileName= self.getDefFileName()
    prj_def= prjDef.ProjectProperties(self.xmlns,defFileName)
    def_tree= prj_def.getXMLTree(defFileName)
    def_tree.write(defFileName,encoding="UTF-8", xml_declaration=None, default_namespace=None, method="xml")
    tree= self.getXMLTree(defFileName)
    tree.write(self.fileName,encoding="UTF-8", xml_declaration=None, default_namespace=None, method="xml")