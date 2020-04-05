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

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class showCoordinates(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({'en': u'Coordinates'})
	
	@objc.python_method
	def drawCoordinates( self, layer ):
		try:
			initPos = 5
			fontColor1 = 0.8, 0.2, 1, 1
			fontColor2 = 0, 0, 0, 0.45
			fontColor3 = 0.0, 0.5, 0.3, 0.8

			for thisPath in layer.paths:
				for thisNode in thisPath.nodes:
					if thisNode.type != "offcurve":
						x = int(round(thisNode.position.x))
						y = int(round(thisNode.position.y))
						text = str(x)+ ", " + str(y)
						self.drawText( layer, text, (x, y), 12.0, fontColor1, 'bottomleft')

					if thisNode.type == "offcurve" and thisNode.nextNode.type != "offcurve":
						x1 = thisNode.position.x
						x2 = thisNode.nextNode.position.x
						deltaX = int(round(x1-x2))
						y1 = thisNode.position.y
						y2 = thisNode.nextNode.position.y
						deltaY = int(round(y1-y2))
						text = str(deltaX)+ ", " + str(deltaY)
						self.drawText( layer, text, (x1, y1), 12.0, fontColor2, 'bottomleft' )
					
					if thisNode.type == "offcurve" and thisNode.prevNode.type !="offcurve":
						x1 = thisNode.position.x
						x2 = thisNode.prevNode.position.x
						deltaX = int(round(x1-x2))
						y1 = thisNode.position.y
						y2 = thisNode.prevNode.position.y
						deltaY = int(round(y1-y2))
						text = str(deltaX)+ ", " + str(deltaY)
						self.drawText( layer, text, (x1, y1), 12.0, fontColor2, 'bottomleft' )
					

		except Exception as e:
			print (e)
	
	@objc.python_method
	def drawText (self, layer, text, textPosition, fontSize, fontColor, textAlign):

		try:
			thisFont = layer.parent.parent
			currentTab = Glyphs.font.currentTab
			NSFontColor = NSColor.colorWithCalibratedRed_green_blue_alpha_( *fontColor )
			self.drawTextAtPoint(text, textPosition, fontSize, NSFontColor, textAlign)
			# glyphEditView = self.controller.graphicView()
			# currentZoom = thisFont.currentTab.scale
			# fontAttributes = { 
			# 	NSFontAttributeName: NSFont.labelFontOfSize_( fontSize/currentZoom ),
			# 	NSForegroundColorAttributeName: fontColor }
			# displayText = NSAttributedString.alloc().initWithString_attributes_( text, fontAttributes )
			# textAlignment = 0 # top left: 6, top center: 7, top right: 8, center left: 3, center center: 4, center right: 5, bottom left: 0, bottom center: 1, bottom right: 2
			# glyphEditView.drawText_atPoint_alignment_( displayText, textPosition, textAlignment )

		except Exception as e:
			print (e)
			pass

	@objc.python_method
	def foreground(self, layer):
		self.drawCoordinates( layer )
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
