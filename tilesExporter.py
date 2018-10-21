# encoding: utf-8

import gvsig
from java.awt import Dimension
from org.gvsig.andami import PluginServices
from org.gvsig.andami import Utilities
import os
import shutil
from com.sun.jimi.core import Jimi
from org.gvsig.app import ApplicationLocator
import time
from gvsig import geom

zoomScale = {
  0: 500000000,
  1: 250000000,
  2: 150000000,
  3: 70000000,
  4: 35000000,
  5: 15000000,
  6: 10000000,
  7: 4000000,
  8: 2000000,
  9: 1000000,
  10: 500000,
  11: 250000,
  12: 150000,
  13: 70000,
  14: 35000,
  15: 15000,
  16: 8000,
  17: 4000,
  18: 2000,
  19: 1000
  }
  
def createTiles( newFolder = "Tiles2", zoomLevels  = [0, 2]):
  pathZoom = {}
  view = gvsig.currentView()
  vp = view.getMapContext().getViewPort()
  # Create main folder
  empdir = "/home/osc/temp/" #Utilities.TEMPDIRECTORYPATH
  
  pathFolder = os.path.join(empdir,newFolder)
  if os.path.exists(pathFolder):
    shutil.rmtree(pathFolder)
  os.mkdir(pathFolder)
  # Create Zooms levels
  for z in range(zoomLevels[0], zoomLevels[1]+1):
    p = os.path.join(pathFolder,str(z))
    pathZoom[z]=p
    os.mkdir(p)
  
  print "Zoom path: ", pathZoom
  
  # for 1 zoom
  for zoom in range(zoomLevels[0], zoomLevels[1]+1):
    #Get scale
    # dividir en cuantos tiles hacen falta para cierto zoom
    # crear carpeta para cada columna / fila
    pathForThisTileCol = os.path.join(pathZoom[zoom],"{0}".format(zoom))
    os.mkdir(pathForThisTileCol)
    rowTile = 0
    pathForThisTileRow = os.path.join(pathForThisTileCol, "{0}.png".format(rowTile))
    # en zoom 0 es /zoom/col/row.png
    print "Scale:", zoomScale[zoom]
    application = ApplicationLocator.getManager()
    docwin = application.getDocumentWindow(view())


    gsv = zoomScale[zoom]#view.getMapContext().getScaleView()
    #Envelope global
    #envelope = view.getMap().getLayers().getMapContext().getFullEnvelope()
    #view.getMapContext().getViewPort().setEnvelope(envelope)
    view.getMapContext().setScaleView(gsv)
    time.sleep(2)
    img = docwin.getMapControl().getImage()
    print pathForThisTileRow
    Jimi.putImage(img, pathForThisTileRow)


def main(*args):
  createTiles()
  return
  
  view = gvsig.currentView()
  vp = view.getMapContext().getViewPort()
  print vp, type(vp)
  print vp.getImageSize()
  return
  d =  Dimension(256,256)
  vp.setImageSize(d)
  print vp.getImageSize()

  window =  PluginServices.getMDIManager().getActiveWindow()
  vd = window.getViewDocument()
  tempImage = PluginServices.getMDIManager().getActiveWindow().getImage()
  print tempImage