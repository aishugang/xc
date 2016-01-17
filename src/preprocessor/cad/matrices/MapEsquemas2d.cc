//----------------------------------------------------------------------------
//  programa XC; cálculo mediante el método de los elementos finitos orientado
//  a la solución de problemas estructurales.
//
//  Copyright (C)  Luis Claudio Pérez Tato
//
//  El programa deriva del denominado OpenSees <http://opensees.berkeley.edu>
//  desarrollado por el «Pacific earthquake engineering research center».
//
//  Salvo las restricciones que puedan derivarse del copyright del
//  programa original (ver archivo copyright_opensees.txt) este
//  software es libre: usted puede redistribuirlo y/o modificarlo 
//  bajo los términos de la Licencia Pública General GNU publicada 
//  por la Fundación para el Software Libre, ya sea la versión 3 
//  de la Licencia, o (a su elección) cualquier versión posterior.
//
//  Este software se distribuye con la esperanza de que sea útil, pero 
//  SIN GARANTÍA ALGUNA; ni siquiera la garantía implícita
//  MERCANTIL o de APTITUD PARA UN PROPÓSITO DETERMINADO. 
//  Consulte los detalles de la Licencia Pública General GNU para obtener 
//  una información más detallada. 
//
// Debería haber recibido una copia de la Licencia Pública General GNU 
// junto a este programa. 
// En caso contrario, consulte <http://www.gnu.org/licenses/>.
//----------------------------------------------------------------------------
//MapEsquemas2d.cc

#include "MapEsquemas2d.h"
#include "MatrizPtrPnt.h"
#include "preprocessor/Preprocessor.h"
#include "domain/mesh/node/Node.h"
#include "domain/mesh/element/Element.h"

#include "preprocessor/cad/entidades/Pnt.h"
#include "preprocessor/set_mgmt/Set.h"
#include "xc_utils/src/base/utils_any.h"
#include "xc_utils/src/base/any_const_ptr.h"

//! @brief Constructor.
XC::MapEsquemas2d::MapEsquemas2d(Cad *cad)
  : MapCadMember<MatrizPtrPnt>(cad) {}

//! @brief Crea un nuevo punto.
XC::MatrizPtrPnt *XC::MapEsquemas2d::Crea(void)
  {
    MatrizPtrPnt *retval= new MatrizPtrPnt();
    retval->set_owner(this);
    (*this)[getTag()]= retval;
    //UpdateSets(retval);
    tag++;
    return retval;
  }

//! @brief Crea un nuevo esquema bidimensional.
XC::MatrizPtrPnt *XC::MapEsquemas2d::makeNew(void)
  {
    MatrizPtrPnt *retval= busca(getTag());
    if(!retval) //El esquema es nuevo.
      retval= Crea();
    return retval;
  }
