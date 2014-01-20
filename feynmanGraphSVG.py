#!/usr/bin/env python

import numpy
import svgwrite
from math import sqrt,pi

def wavyLine(path,p1,p2,capped1=True,capped2=True,amp=5,period=50,width=10):
  p1 = numpy.array(p1)
  p2 = numpy.array(p2)
  propVec = p2-p1
  #print "fullPropVec: ",propVec
  distance = sqrt(numpy.dot(propVec,propVec))
  nCrossings = int(distance/period*2)
  period = distance/nCrossings*2
  normedPropVec = propVec/distance
  normedPerpVec = numpy.array([-normedPropVec[1],normedPropVec[0]])
  ampVec = amp*normedPerpVec
  propVec /= (nCrossings*4)
  #print "propVec: ",propVec
  #print "ampVec: ",ampVec
  #print "normedPropVec",normedPropVec
  #print "normedPerpVec",normedPerpVec
  #print "distance: ",distance
  #print "nCrossings: ",nCrossings
  #print "period: ",period
  path.push(['M']+list(p1))
  if capped1:
    path.push(['l']+list(normedPerpVec*width/2.))
  else:
    path.push(['m']+list(normedPerpVec*width/2.))
  for iCrossings in range(nCrossings/2):
    path.push(['q']+list(propVec+ampVec)+list(2*propVec+ampVec))
    path.push(['q']+list(propVec)+list(2*propVec-ampVec))
    path.push(['q']+list(propVec-ampVec)+list(2*propVec-ampVec))
    path.push(['q']+list(propVec)+list(2*propVec+ampVec))
  if capped2:
    path.push(['l']+list(-normedPerpVec*width))
  else:
    path.push(['m']+list(-normedPerpVec*width))
  propVec *= -1
  ampVec *= -1
  for iCrossings in range(nCrossings/2):
    path.push(['q']+list(propVec+ampVec)+list(2*propVec+ampVec))
    path.push(['q']+list(propVec)+list(2*propVec-ampVec))
    path.push(['q']+list(propVec-ampVec)+list(2*propVec-ampVec))
    path.push(['q']+list(propVec)+list(2*propVec+ampVec))
  if capped1:
    path.push(['l']+list(normedPerpVec*width/2.))
  else:
    path.push(['m']+list(normedPerpVec*width/2.))
  return path

def spiralLine(path,p1,p2,capped1=True,capped2=True,amp=60,period=50,width=10):
  p1 = numpy.array(p1)
  p2 = numpy.array(p2)
  propVec = p2-p1
  print "fullPropVec: ",propVec
  distance = sqrt(numpy.dot(propVec,propVec))
  nLoops = int(distance/period)
  period = distance/nLoops
  normedPropVec = propVec/distance
  normedPerpVec = numpy.array([-normedPropVec[1],normedPropVec[0]])
  ampVec = amp*normedPerpVec
  propVec /= nLoops
  loopDistance = distance/nLoops
  print "propVec: ",propVec
  print "ampVec: ",ampVec
  print "normedPropVec",normedPropVec
  print "normedPerpVec",normedPerpVec
  print "distance: ",distance
  print "nLoops: ",nLoops
  print "period: ",period
  width *= 2
  path.push(['M']+list(p1))
  if capped1:
    path.push(['l']+list(normedPerpVec*width/4.))
  else:
    path.push(['m']+list(normedPerpVec*width/4.))
  for iCrossings in range(nLoops):
    path.push(['q']+list(propVec/2+ampVec/4.)+list(propVec))
  if capped2:
    path.push(['l']+list(-normedPerpVec*width/2.))
  else:
    path.push(['m']+list(-normedPerpVec*width/2.))
  propVec *= -1
  path.push(['l']+list(-(width/2.)*normedPropVec))
  for iCrossings in range(nLoops):
    path.push(['q']+list(-0.5*(loopDistance-width)*normedPropVec+ampVec/4.)+list(-(loopDistance-width)*normedPropVec))
    if iCrossings != nLoops-1:
      path.push(['c']+list(normedPropVec*width-0.5*ampVec)+list(normedPropVec*width-ampVec)+list(-0.5*normedPropVec*width-ampVec))
      path.push(['c']+list(-1.5*normedPropVec*width)+list(-1.5*normedPropVec*width+0.5*ampVec)+list(-0.5*normedPropVec*width+ampVec))
      path.push(['m']+list(normedPropVec*width/2.-normedPerpVec*width/2.))
      path.push(['c']+list(normedPropVec*width-0.5*((amp-width)*normedPerpVec))+list(0.5*normedPropVec*width-((amp-width)*normedPerpVec))+list(-(amp-width)*normedPerpVec))
      path.push(['m']+list((amp-width)*normedPerpVec))
      path.push(['c']+list(-normedPropVec*width-0.5*((amp-width)*normedPerpVec))+list(-0.5*normedPropVec*width-((amp-width)*normedPerpVec))+list(-(amp-width)*normedPerpVec))
      path.push(['m']+list(-normedPropVec*width/2.+normedPerpVec*width/2.+(amp-width)*normedPerpVec))
  path.push(['l']+list(-(width/2.)*normedPropVec))
  if capped1:
    path.push(['l']+list(normedPerpVec*width/4.))
  else:
    path.push(['m']+list(normedPerpVec*width/4.))
  return path

def straightLine(path,p1,p2,capped1=True,capped2=True,width=10):
  p1 = numpy.array(p1)
  p2 = numpy.array(p2)
  propVec = p2-p1
  distance = sqrt(numpy.dot(propVec,propVec))
  normedPropVec = propVec/distance
  normedPerpVec = numpy.array([-normedPropVec[1],normedPropVec[0]])
  path.push(['M']+list(p1))
  if capped1:
    path.push(['l']+list(normedPerpVec*width/2.))
  else:
    path.push(['m']+list(normedPerpVec*width/2.))
  path.push(['l']+list(propVec))
  if capped2:
    path.push(['l']+list(-normedPerpVec*width))
  else:
    path.push(['m']+list(-normedPerpVec*width))
  propVec *= -1
  path.push(['l']+list(propVec))
  if capped1:
    path.push(['l']+list(normedPerpVec*width/2.))
  else:
    path.push(['m']+list(normedPerpVec*width/2.))
  return path

def straightLineArrow(path,p1,p2,capped1=True,capped2=True,forward=True,width=10,arrowLength=30,arrowWidth=None):
  if arrowWidth == None:
    arrowWidth = width
  p1 = numpy.array(p1)
  p2 = numpy.array(p2)
  propVec = p2-p1
  distance = sqrt(numpy.dot(propVec,propVec))
  normedPropVec = propVec/distance
  normedPerpVec = numpy.array([-normedPropVec[1],normedPropVec[0]])
  path.push(['M']+list(p1))
  if capped1:
    path.push(['l']+list(normedPerpVec*width/2.))
  else:
    path.push(['m']+list(normedPerpVec*width/2.))
  path.push(['l']+list(normedPropVec*(distance/2.-arrowLength/2.)))
  if forward:
    path.push(['l']+list(normedPerpVec*arrowWidth))
    path.push(['l']+list(normedPropVec*arrowLength-normedPerpVec*arrowWidth))
  else:
    path.push(['l']+list(normedPropVec*arrowLength+normedPerpVec*arrowWidth))
    path.push(['l']+list(-normedPerpVec*arrowWidth))
  path.push(['l']+list(normedPropVec*(distance/2.-arrowLength/2.)))
  if capped2:
    path.push(['l']+list(-normedPerpVec*width))
  else:
    path.push(['m']+list(-normedPerpVec*width))
  # Back the other way
  path.push(['l']+list(-normedPropVec*(distance/2.-arrowLength/2.)))
  if forward:
    path.push(['l']+list(-normedPropVec*arrowLength-normedPerpVec*arrowWidth))
    path.push(['l']+list(normedPerpVec*arrowWidth))
  else:
    path.push(['l']+list(-normedPerpVec*arrowWidth))
    path.push(['l']+list(-normedPropVec*arrowLength+normedPerpVec*arrowWidth))
  path.push(['l']+list(-normedPropVec*(distance/2.-arrowLength/2.)))
  if capped1:
    path.push(['l']+list(normedPerpVec*width/2.))
  else:
    path.push(['m']+list(normedPerpVec*width/2.))
  return path

color = svgwrite.rgb(0, 0, 255)
width = "1mm"

dwg = svgwrite.Drawing('test.svg',size=("181mm","181mm"))
path = dwg.path(None,stroke=color,stroke_width=width,fill="none")
wavyLine(path,(100,200),(500,200))  # This thing isn't drawing the correct length
straightLine(path,(100,100),(500,150))
straightLineArrow(path,(100,50),(500,550),forward=False)
spiralLine(path,(100,400),(500,400))
dwg.add(path)
dwg.save()
