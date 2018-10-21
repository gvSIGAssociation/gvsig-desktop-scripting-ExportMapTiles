# encoding: utf-8

import gvsig

import os.path

from os.path import join, dirname

from gvsig import currentView
from gvsig import currentLayer

from java.io import File

from org.gvsig.app import ApplicationLocator
from org.gvsig.andami import PluginsLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.tools.swing.api import ToolsSwingLocator
  
from org.gvsig.tools import ToolsLocator

from exportMapTiles import ExportMapTilesPanel

class ExportMapTilesPanelExtension(ScriptingExtension):
  def __init__(self):
    pass

  def isVisible(self):
    return True

  def isLayerValid(self, layer):
    #if layer == None:
    #  #print "### reportbypointExtension.isLayerValid: None, return False"
    #  return False
    #mode = layer.getProperty("reportbypoint.mode")
    #if mode in ("", None):
    #  # Si la capa no tiene configurado el campo a mostrar
    #  # no activamos la herramienta
    #  return False
    return True
    
  def isEnabled(self):
    #layer = currentLayer()
    #if not self.isLayerValid(layer):
    #  return False
    return True

  def execute(self,actionCommand, *args):
    actionCommand = actionCommand.lower()
    if actionCommand == "settool-exportmaptiles":
      #print "### QuickinfoExtension.execute(%s)" % repr(actionCommand)
      layer = currentLayer()
      if not self.isLayerValid(layer):
        return
      viewPanel = currentView().getWindowOfView()
      mapControl = viewPanel.getMapControl()
      exportmaptiles = ExportMapTilesPanel()
      exportmaptiles.showTool("_Export_map_tiles")

def selfRegister():
  i18n = ToolsLocator.getI18nManager()
  application = ApplicationLocator.getManager()
  actionManager = PluginsLocator.getActionInfoManager()
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()

  exportmaptiles_icon = File(join(dirname(__file__),"images","exportmaptiles.png")).toURI().toURL()
  iconTheme.registerDefault("scripting.exportmaptiles", "action", "tools-exportmaptiles", None, exportmaptiles_icon)

  exportmaptiles_extension = ExportMapTilesPanelExtension()
  exportmaptiles_action = actionManager.createAction(
    exportmaptiles_extension,
    "tools-exportmaptiles",   # Action name
    "Export map tiles",   # Text
    "settool-exportmaptiles", # Action command
    "tools-exportmaptiles",   # Icon name
    None,                # Accelerator
    1009000000,          # Position
    i18n.getTranslation("_Export_map_tiles")    # Tooltip
  )
  exportmaptiles_action = actionManager.registerAction(exportmaptiles_action)

  # Añadimos la entrada "Quickinfo" en el menu herramientas
  application.addMenu(exportmaptiles_action, "tools/_ExportMapTiles")
  # Añadimos el la accion como un boton en la barra de herramientas "Quickinfo".
  application.addSelectableTool(exportmaptiles_action, "ExportMapTiles")

def main(*args):
  selfRegister()
  