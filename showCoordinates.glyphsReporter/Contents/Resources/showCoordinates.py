#!/usr/bin/env python
# encoding: utf-8




import objc
from Foundation import *
from AppKit import *
import sys, os, re
import math

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

from GlyphsApp import *

GlyphsReporterProtocol = objc.protocolNamed( "GlyphsReporter" )

class showCoordinates ( NSObject, GlyphsReporterProtocol ):
	
	def init( self ):
		try:
			#Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ));
			return self
		except Exception as e:
			self.logToConsole( "init: %s" % str(e) )
	
	def interfaceVersion( self ):
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )
	
	def title( self ):
		try:
			return "Coordinates"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
	
	def keyEquivalent( self ):
		try:
			return None
		except Exception as e:
			self.logToConsole( "keyEquivalent: %s" % str(e) )
	
	def modifierMask( self ):
		try:
			return 0
		except Exception as e:
			self.logToConsole( "modifierMask: %s" % str(e) )
	
	def drawForegroundForLayer_( self, Layer ):
		try:
			pass
		except Exception as e:
			self.logToConsole( "drawForegroundForLayer_: %s" % str(e) )
	
	
	def checkAnchors ( self, Layer ):
		
		thisFont = Glyphs.font # frontmost font
		thisLayer = Glyphs.font.selectedLayers[0] # current layer
		
		initPos = 5
		fontColor1 = NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.8, 0.2, 1, 1 )
		fontColor2 = NSColor.colorWithCalibratedRed_green_blue_alpha_( 0, 0, 0, 0.45 )
		fontColor3 = NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.5, 0.3, 0.8 )

		for thisPath in thisLayer.paths:
			nodes = thisPath.nodes
			for thisNode in nodes:
				if thisNode.type == GSCURVE or GSLINE and thisNode.type != GSOFFCURVE:
					x = int(round(thisNode.position.x))
					y = int(round(thisNode.position.y))

					self.drawTextAtPoint( str(x)+ ", " + str(y), (x, y), 10.0, fontColor1 )
				if thisNode.type == GSOFFCURVE and thisNode.nextNode.type !=GSOFFCURVE:
					x1 = thisNode.position.x
					x2 = thisNode.nextNode.position.x
					deltaX = int(round(x1-x2))
					y1 = thisNode.position.y
					y2 = thisNode.nextNode.position.y
					deltaY = int(round(y1-y2))
					self.drawTextAtPoint( str(deltaX)+ ", " + str(deltaY), (x1, y1), 10.0, fontColor2 )
				if thisNode.type == GSOFFCURVE and thisNode.prevNode.type !=GSOFFCURVE:
					x1 = thisNode.position.x
					x2 = thisNode.prevNode.position.x
					deltaX = int(round(x1-x2))
					y1 = thisNode.position.y
					y2 = thisNode.prevNode.position.y
					deltaY = int(round(y1-y2))
					self.drawTextAtPoint( str(deltaX)+ ", " + str(deltaY), (x1, y1), 10.0, fontColor2 )

	
	def drawBackgroundForLayer_( self, Layer ):
		try:
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.5, 0.3, 0.5 ).set()
			self.checkAnchors ( Layer )
		except Exception as e:
			self.logToConsole( "drawBackgroundForLayer_: %s" % str(e) )
	
	def drawBackgroundForInactiveLayer_( self, Layer ):
		try:
			pass
		except Exception as e:
			self.logToConsole( "drawBackgroundForInactiveLayer_: %s" % str(e) )
	
	def needsExtraMainOutlineDrawingForInactiveLayer_( self, Layer ):
		return True
	
	def drawTextAtPoint( self, text, textPosition, fontSize, fontColor):
		try:
			glyphEditView = self.controller.graphicView()
			currentZoom = self.getScale()
			fontAttributes = { 
				NSFontAttributeName: NSFont.labelFontOfSize_( fontSize/currentZoom ),
				NSForegroundColorAttributeName: fontColor }
			displayText = NSAttributedString.alloc().initWithString_attributes_( text, fontAttributes )
			textAlignment = 0 # top left: 6, top center: 7, top right: 8, center left: 3, center center: 4, center right: 5, bottom left: 0, bottom center: 1, bottom right: 2
			glyphEditView.drawText_atPoint_alignment_( displayText, textPosition, textAlignment )
		except Exception as e:
			self.logToConsole( "drawTextAtPoint: %s" % str(e) )
	
	def getHandleSize( self ):
		try:
			Selected = NSUserDefaults.standardUserDefaults().integerForKey_( "GSHandleSize" )
			if Selected == 0:
				return 5.0
			elif Selected == 2:
				return 10.0
			else:
				return 7.0 # Regular
		except Exception as e:
			self.logToConsole( "getHandleSize: HandleSize defaulting to 7.0. %s" % str(e) )
			return 7.0

	def getScale( self ):
		try:
			return self.controller.graphicView().scale()
		except:
			self.logToConsole( "Scale defaulting to 1.0" )
			return 1.0
	
	def setController_( self, Controller ):
		try:
			self.controller = Controller
		except Exception as e:
			self.logToConsole( "Could not set controller" )
	
	def logToConsole( self, message ):
		myLog = "Show %s plugin:\n%s" % ( self.title(), message )
		NSLog( myLog )
