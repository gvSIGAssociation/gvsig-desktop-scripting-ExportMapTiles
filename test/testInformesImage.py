
from gvsig import *
import sys
import os
path_script = os.path.dirname(__file__)
use_jar(os.path.join(path_script, "jar", "jOpenDocument-1.3.jar"))

from gvsig import geom
from java.io import File
from org.jopendocument.dom.template import JavaScriptFileTemplate
from org.jdom import Namespace
from com.sun.jimi.core import Jimi
from org.gvsig.app import ApplicationLocator
import time



def main(*args):
    #Input
    print "Script generacion de informes"
    
    path_script = os.path.dirname(__file__)
    pathTemplate = os.path.join(path_script, "plantilla", "plantilla_informe_test2.odt")

    #Output
    # Utilizar este formato con una unica barra
    path_output = os.path.join("C:/","gvsig_informes", "resultado")
    if os.path.exists(path_output) == False:
        raise Exception(OSError, "Path not found: " + path_output)

    pathOutputFile = os.path.join(path_output, "test_parcela%02d")
    pathEnvelope =   os.path.join(path_output, "envelope.png")
    pathImageOut = os.path.join(path_output, "img%02d.png")
    print pathImageOut
    print pathEnvelope
    print pathOutputFile
    
    #Inicio
    print "Informe parcelario"
    application = ApplicationLocator.getManager()
    layer = currentLayer()
    docvista = currentView()
    
    if layer == None or docvista == None:
      raise Exception(ValueError, 'Not layer selected')
      return

    docwin = application.getDocumentWindow(docvista())
    
    #Get scale
    gsv = currentView().getMapContext().getScaleView()
    
    #Envelope global
    envelope = currentView().getMap().getLayers().getMapContext().getFullEnvelope()
    currentView().getMapContext().getViewPort().setEnvelope(envelope)
    time.sleep(2)
    img = docwin.getMapControl().getImage()
    Jimi.putImage(img,pathEnvelope)
   
    #Create images and odt
    n=0
    for f in layer.getSelection():
        print f.MASA, f.geometry()
        #Center view and set same scale
        geomf = f.geometry()
        currentView().centerView(geomf.getEnvelope())
        currentView().getMapContext().setScaleView(gsv)
        time.sleep(4)
        #Imagen
        img = docwin.getMapControl().getImage()
        pathImage = pathImageOut % n
        Jimi.putImage(img,pathImage)

        # Create odt
        pathOutFile = pathOutputFile % n

        templateFile = pathTemplate #File(pathTemplate)
        outFile = File(pathOutFile)
        bcFile = pathImage
        template = JavaScriptFileTemplate(templateFile)

        values = f.getValues()
        template.setField("hoja", str(values['HOJA']))
        template.setField("area", str(values['AREA']))
        template.setField("coorx", f.COORX)
        template.setField("coory", f.COORY)
        ddoc = template.createDocument()
        
        pathGeometry = ("file:///" + bcFile).replace('\\','/')
        pathEnvelopeForHref  = ("file:///" +pathEnvelope).replace('\\','/')
        
        ddoc.getDescendantByName("draw:frame","Imagen2").setAttribute("href", pathGeometry,Namespace.getNamespace("xlink", "http://www.w3.org/1999/xlink"))
        ddoc.getDescendantByName("draw:frame","Imagen1").setAttribute("href", pathEnvelopeForHref,Namespace.getNamespace("xlink", "http://www.w3.org/1999/xlink"))

        ddoc.saveAs(outFile)
        #template.saveAs(outFile)
        n += 1
        
def use_jar(fname, root=__file__, isglobal=False):
  from org.gvsig.scripting import ScriptingLocator
  from java.io import File
  import sys
  import os

  if isinstance(fname,File):
    f = fname
    fname = f.getPath()
  else:
    f = File(fname)
  if not f.isAbsolute() :
    rf = File(root)
    if rf.isFile() :
      rf = rf.getParentFile()
    f = File( rf,fname)

  fname = f.getCanonicalPath()
  use_libs(fname,isglobal=isglobal)
