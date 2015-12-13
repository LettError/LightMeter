# -*- coding: utf-8 -*-

from AppKit import NSColor, NSFont, NSFontAttributeName, NSForegroundColorAttributeName, NSCursor
from mojo.events import installTool, EditingTool, BaseEventTool, setActiveEventTool
from mojo.drawingTools import *
from mojo.UI import UpdateCurrentGlyphView
from defconAppKit.windows.baseWindow import BaseWindowController

from gaussTools import *
import vanilla

"""


    LightMeterTool 02
    
    This is a sort of a light meter for the glyph window. 
    Running this script will install a tool in the toolbar. 
        
    When selected, the tool draws trails of gray rectangles.
    The gray level of a pixel corresponds to the light 
    contributed by the white and black areas around the cursor.
    The blue number indicates the percentage. 

        100    = white + dot
        n      = some level of gray
        0      = black + dot
    
    Keys:
    arrowkey up: increase the measuring diameter.
    arrowkey down: decrease the measuring diameter.
    
    Command + arrowkey up: increase the sampling size
    Command + arrowkey down: decrease the sampling size
    
    Command + click: clear all the samples.
    
    t        show tail
    p        fit to grid
    c        clear tail
    i         invert
    
    Theory:
    When the light passes through the optical system of the eye,
    it is diffracted a little bit. This is noticable on the edges.
    The amount of diffraction is small, but so are the letters.
    The diameter of the measurement can be related to the 
    pupil size, the typesize and the reading distance.
    
    8 pt type, at 40 cm = 24.26' arcminutes

    Pupilsize, Airy disc diameter, em units
    8.2 mm: 0.658' arcminutes, 27.13 units
    1 mm: 4.494' arcminutes, 185.28 units
    
    See pupilSizeToAiryDiscRadius() in scaleTools.py
    
    So it's all scientific and precise?
    No. This is a simple interpretation of the math and basic physics
    that are relevant for all this. This code does not simulate actual
    light reflecting on actual paper, while being held in shaky hands,
    and viewed with teary eyes.
    
    So why bother?
    Because trying to find the right values is better than applying a blur until it looks good.    
    
    To Do:
        - invent some UI to incorporate sliders for pupil size and distance
        - 
"""


class LightMeterTool(BaseEventTool):

    lightMeterToolPrefsLibKey = "com.letterror.lightMeter.prefs"
    textAttributes = {
        NSFontAttributeName : NSFont.systemFontOfSize_(10),
        NSForegroundColorAttributeName : NSColor.whiteColor(),
    }

    def setup(self):
        self.sliderWindow = None
        self.insides = {}
        self._hits = {}
        self._misses = {}
        self.kernel = None
        self.diameterStep = 5
        self.fullColorMarkerSize = 2
        self.diameterMarkerWidth = 0.4
        self.toolStep = 2
        self.isResizing = False
        self.pts = []
        self.dupes = set()
        self.samples = {}
        self.lastPoint = None
        self._insideColor = (35/255.0,60/255.0,29/255.0)    # photoshop
        self._outsideColor = (255/255.0,234/255.0,192/255.0)
        
        self.defaultPrefs = {
                'drawTail':      False,
                'toolStyle':     'fluid',    # grid
                'invert':        False,
                'diameter':      200,
                'toolDiameter':  30,
                'chunkSize':     5,
            }
        self.prefs = {}
        self.getPrefs()
        
    def getPrefs(self):
        # read the prefs from the font lib
        # so we have consistent tool prefs
        # between glyphs
        g = self.getGlyph()
        if g is None:
            # no font? no parent?
            self.prefs.update(self.defaultPrefs)
            return
        parentLib = g.getParent().lib
        if self.lightMeterToolPrefsLibKey in parentLib:
            self.prefs.update(parentLib[self.lightMeterToolPrefsLibKey])
        else:
            self.prefs.update(self.defaultPrefs)
    
    def storePrefs(self):
        # write the current tool preferences to the font.lib
        g = self.getGlyph()
        parentLib = g.getParent().lib
        if not self.lightMeterToolPrefsLibKey in parentLib:
            parentLib[self.lightMeterToolPrefsLibKey] = {}
        parentLib[self.lightMeterToolPrefsLibKey].update(self.prefs)

    def getKernel(self):
        kernelRadius = int(round((0.5*self.prefs['diameter'])/self.prefs['chunkSize']))
        self.kernel = getKernel(kernelRadius, angle=math.radians(30))
    
    def grid(self, pt):
        x, y = pt
        x = x - x%self.prefs['toolDiameter'] + 0.5*self.prefs['toolDiameter']
        y = y - y%self.prefs['toolDiameter'] + 0.5*self.prefs['toolDiameter']
        return x, y
        
    def draw(self, scale):
        # drawBackground(self
        s = self.prefs['toolDiameter']    # / scale
        last = None
        if not self.pts: return
        if self.prefs['drawTail']:
            drawThese = self.pts[:]
        else:
            drawThese = [self.pts[-1]]
        stroke(None)
        for (x,y), level, tdm in drawThese:
            key = (x,y),tdm
            if self.prefs['invert']:
                fill(1-level)
            else:
                fill(level)
            stroke(None)
            if self.prefs['toolStyle'] == "grid":
                rect(x-.5*tdm, y-0.5*tdm, tdm, tdm)
            else:
                oval(x-.5*tdm, y-0.5*tdm, tdm, tdm)
            if round(level, 3) == 0:
                stroke(None)
                fill(1)
                oval(x-.5*self.fullColorMarkerSize, y-.5*self.fullColorMarkerSize, self.fullColorMarkerSize, self.fullColorMarkerSize)
            elif round(level,3) == 1.0:
                stroke(None)
                fill(0)
                oval(x-.5*self.fullColorMarkerSize, y-.5*self.fullColorMarkerSize, self.fullColorMarkerSize, self.fullColorMarkerSize)
    
        self.drawDiameter(x, y, scale, showSize=self.isResizing)

        (x,y), level, tdm = drawThese[-1]
        if self.prefs['invert']:
            fill(1-level)
        else:
            fill(level)
        stroke(None)
        if self.prefs['toolStyle'] == "grid":
            rect(x-.5*tdm, y-0.5*tdm, tdm, tdm)
        else:
            oval(x-.5*tdm, y-0.5*tdm, tdm, tdm)
        
        tp, level, tdm = self.pts[-1]
        self.getNSView()._drawTextAtPoint(
            "%3.2f"%(100-100*level),
            self.textAttributes,
            tp,
            yOffset=-30,
            drawBackground=True,
            backgroundColor=NSColor.blueColor())

    def drawDiameter(self, x, y, scale=1, showSize=False):
        
        # draw points contributing to the level.
        s = self.prefs['chunkSize']
        stroke(None)
        for (px,py), v in self._hits.items():
            fill(self._outsideColor[0],self._outsideColor[1],self._outsideColor[2], v*80)
            oval(px-0.5*s, py-0.5*s, s, s)
        for (px,py), v in self._misses.items():
            fill(self._insideColor[0],self._insideColor[1],self._insideColor[2], v*80)
            oval(px-0.5*s, py-0.5*s, s, s)

        stroke(0.5)
        strokeWidth(self.diameterMarkerWidth*scale)
        fill(None)
        oval(x-0.5*self.prefs['diameter'], y-0.5*self.prefs['diameter'], self.prefs['diameter'], self.prefs['diameter'])

        if showSize:
            tp = x, y + 20*scale
            self.getNSView()._drawTextAtPoint(
                u"⌀ %3.2f"%(self.prefs['diameter']),
                self.textAttributes,
                tp,
                yOffset=(.5*self.prefs['diameter'])/scale,
                drawBackground=True,
                backgroundColor=NSColor.grayColor())

    def mouseDown(self, point, event):
        mods = self.getModifiers()
        cmd = mods['commandDown'] > 0
        self.isResizing = False
        if cmd:
            self.clear()
            
    def clear(self):
        self.pts = []
        self.dupes = set()
        self.samples = {}
    
    def drawMargins(self):
        # sample the whole box
        g = self.getGlyph()
        if g.box is None:
            return
        xMin, yMin, xMax, yMax = self.getGlyph().box
        for y in range(yMin, yMax+self.prefs['toolDiameter'], self.prefs['toolDiameter']):
                samplePoint = self.grid((xMin,y))
                self.processPoint(samplePoint)
                samplePoint = self.grid((0,y))
                self.processPoint(samplePoint)
                samplePoint = self.grid((xMax,y))
                self.processPoint(samplePoint)
                samplePoint = self.grid((g.width,y))
                self.processPoint(samplePoint)
            
    def keyDown(self, event):
        letter = event.characters()
        if letter == "i":
            # invert the paint color on drawing
            self.prefs['invert'] = not self.prefs['invert']
            self.storePrefs()
        elif letter == "M":
            # draw the whole bounds
            self.drawMargins()
        elif letter == "p":
            if self.prefs['toolStyle'] == "grid":
                self.prefs['toolStyle'] = "fluid"
            else:
                self.prefs['toolStyle'] = 'grid'
            self.storePrefs()
        elif letter == "t":
            self.prefs['drawTail'] = not self.prefs['drawTail']
            self.storePrefs()
        elif letter == "c":
            self.clear()

        mods = self.getModifiers()
        cmd = mods['commandDown'] > 0
        option = mods['optionDown'] > 0
        arrows = self.getArrowsKeys()
        if cmd:
            # change the grid size
            if arrows['up']:
                self.prefs['toolDiameter'] += self.toolStep
            elif arrows['down']:
                self.prefs['toolDiameter'] -= self.toolStep
                self.prefs['toolDiameter'] = abs(self.prefs['toolDiameter'])
            #self.clear()
            self.getKernel()
            self.calcSample(self.lastPoint)
            self.storePrefs()
        else:
            self.isResizing = True
            if arrows['up']:
                self.prefs['diameter'] += self.diameterStep
            elif arrows['down']:
                self.prefs['diameter'] -= self.diameterStep
                self.prefs['diameter'] = abs(self.prefs['diameter'])
            #self.clear()
            self.getKernel()
            self.calcSample(self.lastPoint)
            self.storePrefs()
        UpdateCurrentGlyphView()
        
    def mouseDragged(self, point, delta):
        """ Calculate the blurred gray level for this point. """
        self.isResizing = False
        self.lastPoint = samplePoint = point.x, point.y
        if self.prefs['toolStyle'] == "grid":
            self.lastPoint = samplePoint = self.grid(samplePoint)
        self.processPoint(samplePoint)
    
    def processPoint(self, samplePoint):
        if (self.prefs['toolDiameter'], samplePoint) in self.dupes:
            level = self.samples.get((samplePoint, self.prefs['toolDiameter']))['level']
            i = self.pts.index((samplePoint, level, self.prefs['toolDiameter']))
            del self.pts[i]
            self.pts.append((samplePoint, level, self.prefs['toolDiameter']))
        self.calcSample(samplePoint)
        
    def calcSample(self, samplePoint):
        if samplePoint is None:
            return
        if not self.kernel:
            self.getKernel()
        level = 0
        self._insides = {}
        self._hits = {}
        self._misses = {}
        
        nsPathObject =  self.getGlyph().getRepresentation("defconAppKit.NSBezierPath")
        for pos, val in self.kernel.items():
            thisPos = samplePoint[0]+pos[0]*self.prefs['chunkSize'], samplePoint[1]+pos[1]*self.prefs['chunkSize']
            a = math.atan2(pos[0], pos[1])
            if thisPos not in self._insides:
                self._insides[thisPos] = nsPathObject.containsPoint_(thisPos)
            if not self._insides[thisPos]:
                level += self.kernel.get(pos)
                self._hits[thisPos] = self.kernel.get(pos)
            else:
                self._misses[thisPos] = self.kernel.get(pos)
        self.pts.append((samplePoint, level, self.prefs['toolDiameter']))
        self.samples[(samplePoint, self.prefs['toolDiameter'])] = dict(level=level)
        self.dupes.add((self.prefs['toolDiameter'], samplePoint))
        return level
        
    def getToolbarTip(self):
        return 'LightMeter'
    
p = LightMeterTool()
installTool(p)
setActiveEventTool('LightMeterTool')
