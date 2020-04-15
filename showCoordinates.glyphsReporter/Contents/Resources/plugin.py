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

fontColor1 = 0.8, 0.2, 1, 1
fontColor1 = NSColor.colorWithCalibratedRed_green_blue_alpha_( *fontColor1 )
fontColor2 = 0, 0.45
fontColor2 = NSColor.colorWithCalibratedWhite_alpha_( *fontColor2 )
fontColor3 = 0.0, 0.5, 0.3, 0.8
fontColor3 = NSColor.colorWithCalibratedRed_green_blue_alpha_( *fontColor3 )

fontSize = 10

class showCoordinates(ReporterPlugin):
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({'en': u'Coordinates'})
	
	@objc.python_method
	def foregroundInViewCoords(self, layer = None):
		try:
			layer = self.activeLayer()
			self._pos = self.activePosition()
			self._scale = self.getScale()
			for thisPath in layer.paths:
				for thisNode in thisPath.nodes:
					if thisNode.type != "offcurve":
						x = int(round(thisNode.position.x))
						y = int(round(thisNode.position.y))
						text = str(x)+ ", " + str(y)
						self.drawText( text, (x, y), fontSize, fontColor1, 'bottomleft')

					if thisNode.type == "offcurve" and thisNode.nextNode.type != "offcurve":
						x1 = thisNode.position.x
						x2 = thisNode.nextNode.position.x
						deltaX = int(round(x1-x2))
						y1 = thisNode.position.y
						y2 = thisNode.nextNode.position.y
						deltaY = int(round(y1-y2))
						text = str(deltaX)+ ", " + str(deltaY)
						self.drawText( text, (x1, y1), fontSize, fontColor2, 'bottomleft' )

					if thisNode.type == "offcurve" and thisNode.prevNode.type !="offcurve":
						x1 = thisNode.position.x
						x2 = thisNode.prevNode.position.x
						deltaX = int(round(x1-x2))
						y1 = thisNode.position.y
						y2 = thisNode.prevNode.position.y
						deltaY = int(round(y1-y2))
						text = str(deltaX)+ ", " + str(deltaY)
						self.drawText( text, (x1, y1), fontSize, fontColor2, 'bottomleft' )
		except Exception as e:
			import traceback
			print(traceback.format_exc())
	
	@objc.python_method
	def drawText(self, text, textPosition, fontSize, fontColor, textAlign):
		try:
			string = NSString.alloc().initWithString_(text)
			drawPos = (textPosition[0] * self._scale + self._pos.x + 1 , textPosition[1] * self._scale + self._pos.y + 1)
			string.drawAtPoint_color_alignment_handleSize_(drawPos, fontColor, 0, -1)
		except Exception as e:
			print (e)
			pass

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
