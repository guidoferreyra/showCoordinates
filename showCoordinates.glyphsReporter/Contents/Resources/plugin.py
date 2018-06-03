# encoding: utf-8

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class showCoordinates(ReporterPlugin):

	def settings(self):
		self.menuName = Glyphs.localize({'en': u'Coordinates', 'es': u'Coordenadas'})

	def drawCoordinates ( self, layer ):

		thisLayer = layer
				
		initPos = 5
		fontColor1 = NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.8, 0.2, 1, 1 )
		fontColor2 = NSColor.colorWithCalibratedRed_green_blue_alpha_( 0, 0, 0, 0.45 )
		fontColor3 = NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.5, 0.3, 0.8 )

		for thisPath in thisLayer.paths:
			nodes = thisPath.nodes
			for thisNode in nodes:
				if thisNode.type == "curve" or "line" and thisNode.type != "offcurve":
					x = int(round(thisNode.position.x))
					y = int(round(thisNode.position.y))
					self.drawText( thisLayer, str(x)+ ", " + str(y), (x, y), 10.0, fontColor1 )
					#print "rect"

				if thisNode.type == "offcurve" and thisNode.nextNode.type != "offcurve":
					x1 = thisNode.position.x
					x2 = thisNode.nextNode.position.x
					deltaX = int(round(x1-x2))
					y1 = thisNode.position.y
					y2 = thisNode.nextNode.position.y
					deltaY = int(round(y1-y2))
					self.drawText( thisLayer, str(deltaX)+ ", " + str(deltaY), (x1, y1), 10.0, fontColor2 )
					#print "next offcurve"

				if thisNode.type == "offcurve" and thisNode.prevNode.type !="offcurve":
					x1 = thisNode.position.x
					x2 = thisNode.prevNode.position.x
					deltaX = int(round(x1-x2))
					y1 = thisNode.position.y
					y2 = thisNode.prevNode.position.y
					deltaY = int(round(y1-y2))
					self.drawText( thisLayer, str(deltaX)+ ", " + str(deltaY), (x1, y1), 10.0, fontColor2 )
					#print "pre off "	


	def drawText ( self, thisLayer, text, textPosition, fontSize, fontColor):

		try:
			thisFont = thisLayer.parent.parent
			glyphEditView = self.controller.graphicView()
			currentZoom = thisFont.currentTab.scale
			fontAttributes = { 
				NSFontAttributeName: NSFont.labelFontOfSize_( fontSize/currentZoom ),
				NSForegroundColorAttributeName: fontColor }
			displayText = NSAttributedString.alloc().initWithString_attributes_( text, fontAttributes )
			textAlignment = 0 # top left: 6, top center: 7, top right: 8, center left: 3, center center: 4, center right: 5, bottom left: 0, bottom center: 1, bottom right: 2
			glyphEditView.drawText_atPoint_alignment_( displayText, textPosition, textAlignment )

		except Exception as e:
			print e
			pass

	def foreground(self, layer):
		self.drawCoordinates (layer)
			
	def conditionalContextMenus(self):
		pass

	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
