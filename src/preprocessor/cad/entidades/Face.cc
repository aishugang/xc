//----------------------------------------------------------------------------
//  XC program; finite element analysis code
//  for structural analysis and design.
//
//  Copyright (C)  Luis Claudio Pérez Tato
//
//  This program derives from OpenSees <http://opensees.berkeley.edu>
//  developed by the  «Pacific earthquake engineering research center».
//
//  Except for the restrictions that may arise from the copyright
//  of the original program (see copyright_opensees.txt)
//  XC is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or 
//  (at your option) any later version.
//
//  This software is distributed in the hope that it will be useful, but 
//  WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details. 
//
//
// You should have received a copy of the GNU General Public License 
// along with this program.
// If not, see <http://www.gnu.org/licenses/>.
//----------------------------------------------------------------------------
//Face.cc

#include "Face.h"
#include "xc_utils/src/geom/pos_vec/Vector3d.h"
#include "xc_utils/src/geom/d3/BND3d.h"

#include "domain/mesh/node/Node.h"
#include "domain/mesh/element/Element.h"
#include "med.h"
#include "preprocessor/Preprocessor.h"
#include "preprocessor/set_mgmt/Set.h"
#include "vtkCellType.h"

//! @brief Constructor.
XC::Face::Face(void)
  : CmbEdge(nullptr,0), ndivj(0) {}

//! @brief Constructor.
XC::Face::Face(Preprocessor *m,const size_t &ndivI, const size_t &ndivJ)
  : CmbEdge(m,ndivI), ndivj(ndivJ) {}

//! @brief Constructor.
//! @param nombre: Identificador del objeto.
//! @param m: Pointer to preprocesador.
//! @param nd: Número de divisiones.
XC::Face::Face(const std::string &nombre,Preprocessor *m,const size_t &ndivI, const size_t &ndivJ)
  : CmbEdge(nombre,m,ndivI), ndivj(ndivJ) {}

//! @brief Asigna el número de divisiones en el eje i.
void XC::Face::SetNDivI(const size_t &ndi)
  { CmbEdge::ndiv= ndi; }

//! @brief Asigna el número de divisiones en el eje j.
void XC::Face::SetNDivJ(const size_t &ndj)
  { ndivj= ndj; }

//! @brief Inserts the body being passed as parameter neighbors
//! container of this surface.
void XC::Face::inserta_body(Body *b)
  { cuerpos_sup.insert(b); }

//! @brief Actualiza la topología.
void XC::Face::actualiza_topologia(void)
  {
    for(std::deque<Lado>::iterator i=lineas.begin();i!=lineas.end();i++)
      (*i).Borde()->inserta_surf(this);
  }

//! @brief Returns the index of the edge in common with the surface
//! being passed as parameter (if it exists).
size_t XC::Face::BordeComun(const XC::Face &otra) const
  {
    size_t cont= 1;
    if(this == &otra) return cont; //Son la misma todos los bordes son comunes.
    for(std::deque<Lado>::const_iterator i=lineas.begin();i!=lineas.end();i++,cont++)
      {
        if((*i).Borde()->Toca(otra))
          return cont;
      }
    return 0;
  }

//! Returns:
//! - 1 if the line belongs to both surfaces and the orientation is the same.
//! - -1 if the line belongs to both surfaces and the orientation is the opposite.
//! - 0 line doesn't belongs to both surfaces.
int XC::Face::SentidoBorde(const XC::Edge *l,const XC::Face &otra) const
  {
    //Buscamos los indices de las lineas en una 
    const size_t ind_l_esta= IndiceEdge(l);
    if(ind_l_esta == 0)
      {
        std::cerr << "Line :" << l->GetNombre() 
                  << " is not an edge of the surface: " << GetNombre() << std::endl;
        return 0;
      }
    const size_t ind_l_otra= otra.IndiceEdge(l);
    if(ind_l_otra == 0)
      {
        std::cerr << "Line :" << l->GetNombre() 
                  << " is not an edge of the surface: " << otra.GetNombre() << std::endl;
        return 0;
      }
    //Search the edges on each surface;
    const Lado *l_esta= GetLado(ind_l_esta);
    const Lado *l_otra= otra.GetLado(ind_l_otra);
    if(l_esta->P2() == l_otra->P2())
      return 1;
    else
      return -1;
  }

//! @brief Returns the vértice cuyo índice is being passed as parameter.
const XC::Pnt *XC::Face::GetVertice(const size_t &i) const
  { return GetLado(i)->P1(); }

//! @brief Return the surfaces that touch the line.
std::set<const XC::Face *> XC::GetSupsTocan(const Edge &p)
  { return p.SupsTocan(); }

//! @brief Returns true if the lines touches the body (neighbor).
bool XC::Face::Toca(const XC::Body &b) const
  {
    std::set<const Body *>::const_iterator i= cuerpos_sup.find(&b);
    return (i!=cuerpos_sup.end());
  }

//! @brief Returns the sets that contains this surface.
std::set<XC::SetBase *> XC::Face::get_sets(void) const
  {
    std::set<SetBase *> retval;
    const Preprocessor *preprocessor= GetPreprocessor();
    if(preprocessor)
      {
        MapSet &sets= const_cast<MapSet &>(preprocessor->get_sets());
        retval= sets.get_sets(this);
      }
    else
      std::cerr << "Face::get_sets; no se ha definido el preprocesador." << std::endl;
    return retval;
  }

//! @brief Appends the surface to each of the sets being passed as parameter.
void XC::Face::add_to_sets(std::set<SetBase *> &sets)
  {
    for(std::set<SetBase *>::iterator i= sets.begin();i!= sets.end();i++)
      {
        Set *s= dynamic_cast<Set *>(*i);
        if(s) s->getSurfaces().push_back(this);
      }
  }

//! @brief Returns a pointer to nodo cuyos índices se pasan como parámetro.
XC::Node *XC::Face::GetNodo(const size_t &i,const size_t &j,const size_t &k)
  { return CmbEdge::GetNodo(i,j,k); }

//! @brief Returns a pointer to nodo cuyos índices se pasan como parámetro.
const XC::Node *XC::Face::GetNodo(const size_t &i,const size_t &j,const size_t &k) const
  { return CmbEdge::GetNodo(i,j,k); }

//! @brief Returns a pointer to nodo cuyos índices is being passed as parameter.
XC::Node *XC::Face::GetNodo(const size_t &i,const size_t &j)
  { return const_cast<Node *>(static_cast<const Face &>(*this).GetNodo(i,j)); }

//! @brief Returns a pointer to nodo cuyos índices is being passed as parameter.
const XC::Node *XC::Face::GetNodo(const size_t &i,const size_t &j) const
  {
    const Node *retval= nullptr;
    if(nodos.EsCapaICte())
      retval= CmbEdge::GetNodo(1,i,j);
    else if(nodos.EsCapaJCte())
      retval= CmbEdge::GetNodo(i,1,j);
    else if(nodos.EsCapaKCte())
      retval= CmbEdge::GetNodo(i,j,1);
    else
      std::cerr << "Face::GetNodo; el node set is not one-dimensional." << std::endl;
    return retval;
  }

//! @brief Returns a pointer to nodo cuyo índice is being passed as parameter.
XC::Node *XC::Face::GetNodo(const size_t &i)
  {
    std::cerr << "No debe llamarse a Face::GetNodo con un sólo índice." << std::endl; 
    return nullptr;
  }

//! @brief Returns a pointer to nodo cuyo índice is being passed as parameter.
const XC::Node *XC::Face::GetNodo(const size_t &i) const
  { return const_cast<Node *>(static_cast<const Face &>(*this).GetNodo(i)); }

//! @brief Interfaz con VTK.
int XC::Face::getVtkCellType(void) const
  {
    int retval= VTK_EMPTY_CELL;
    const size_t nl= NumEdges();
    switch(nl)
      {
      case 1:
        retval= VTK_LINE;
      case 2:
        retval= VTK_EMPTY_CELL;
      case 3:
        retval= VTK_TRIANGLE;
      case 4:
        retval= VTK_QUAD;
      default:
        retval= VTK_POLYGON;
      }
    return retval;
  }

//! @brief Interfaz con el formato MED de Salome.
int XC::Face::getMEDCellType(void) const
  {
    const size_t nl= NumEdges();
    int retval= -1;
    switch(nl)
      {
      case 1:
        retval= MED_SEG2;
      case 2:
        retval= MED_NONE;
      case 3:
        retval= MED_TRIA3;
      case 4:
        retval= MED_QUAD4;
      default:
        retval= MED_NONE;
      }
    return retval;
  }
