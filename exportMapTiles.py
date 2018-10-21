# encoding: utf-8

import gvsig
from gvsig.libs.formpanel import FormPanel
from org.gvsig.gui.beans.doubleslider import DoubleSlider

from tilesExporter import createTiles

class ExportMapTilesPanel(FormPanel):
  def __init__(self):
    FormPanel.__init__(self, gvsig.getResource(__file__, "exportMapTiles.xml"))
    #self.setPreferredSize(300,300)
    #ds = DoubleSlider()
    #self.jpSlider.add(ds)
  def btnProcess_click(self, *args):
    try:
      zmin = int(self.txtZMin.getText())
      zmax = int(self.txtZMax.getText())
      size = int(self.txtSize.getText())
    except:
      return
    createTiles("NewTiles", [zmin, zmax])

def main(*args):
    l = ExportMapTilesPanel()
    l.showTool("_Export_map_tiles")
    pass
