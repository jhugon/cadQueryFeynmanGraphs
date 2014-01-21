#!/usr/bin/env python

import numpy
import svgwrite
from math import sqrt,pi

def makeEndPoints(p1,p2,width):
  """
  Returns the points that a vertex should connect to as a pair of pairs of points.
  """
  p1 = numpy.array(p1,dtype=numpy.dtype(float))
  p2 = numpy.array(p2,dtype=numpy.dtype(float))
  propVec = p2-p1
  distance = sqrt(numpy.dot(propVec,propVec))
  normedPropVec = propVec/distance
  normedPerpVec = numpy.array([-normedPropVec[1],normedPropVec[0]])
  return (p1+normedPerpVec*width/2.,p1-normedPerpVec*width/2.),(p2+normedPerpVec*width/2.,p2-normedPerpVec*width/2.)

def wavyLine(path,p1,p2,capped1=True,capped2=True,amp=10.,period=30.0,width=5.0):
  width *= 1.5
  p1 = numpy.array(p1,dtype=numpy.dtype(float))
  p2 = numpy.array(p2,dtype=numpy.dtype(float))
  propVec = p2-p1
  #print "fullPropVec: ",propVec
  distance = sqrt(numpy.dot(propVec,propVec))
  nOsc = int(distance/period)
  period = distance/nOsc
  normedPropVec = propVec/distance
  normedPerpVec = numpy.array([-normedPropVec[1],normedPropVec[0]])
  ampVec = amp*normedPerpVec
  propVec /= (nOsc*8)  # propVec is sopposed to be an 8th-wave
  propVec -= normedPropVec*(width/8. + width/16./nOsc)
  #print "propVec: ",propVec
  #print "ampVec: ",ampVec
  #print "normedPropVec",normedPropVec
  #print "normedPerpVec",normedPerpVec
  #print "distance: ",distance
  #print "nOsc: ",nOsc
  #print "period: ",period
  nExtra = 0
  quartWidthPropVec = 0.25*width*normedPropVec
  path.push(['M']+list(p1))
  if capped1:
    path.push(['l']+list(normedPerpVec*width/2.))
  else:
    path.push(['m']+list(normedPerpVec*width/2.))
  for iOsc in range(nOsc):
    path.push(['q']+list(propVec+ampVec+quartWidthPropVec)+list(2*propVec+ampVec+2*quartWidthPropVec))
    path.push(['q']+list(propVec+quartWidthPropVec)+list(2*propVec-ampVec+2*quartWidthPropVec))
    nExtra+=4
    path.push(['q']+list(propVec-ampVec)+list(2*propVec-ampVec))
    path.push(['q']+list(propVec)+list(2*propVec+ampVec))
  path.push(['l']+list(2*quartWidthPropVec))
  nExtra+=2
  if capped2:
    path.push(['l']+list(-normedPerpVec*width))
  else:
    path.push(['m']+list(-normedPerpVec*width))
  propVec *= -1
  ampVec *= -1
  for iOsc in range(nOsc):
    path.push(['q']+list(propVec+ampVec-quartWidthPropVec)+list(2*propVec+ampVec-2*quartWidthPropVec))
    path.push(['q']+list(propVec-quartWidthPropVec)+list(2*propVec-ampVec-2*quartWidthPropVec))
    nExtra+=4
    path.push(['q']+list(propVec-ampVec)+list(2*propVec-ampVec))
    path.push(['q']+list(propVec)+list(2*propVec+ampVec))
  path.push(['l']+list(-2*quartWidthPropVec))
  nExtra+=2
  if capped1:
    path.push(['l']+list(normedPerpVec*width/2.))
  else:
    path.push(['m']+list(normedPerpVec*width/2.))
  #print "nExtra",nExtra
  return makeEndPoints(p1,p2,width)

def spiralLine(path,p1,p2,capped1=True,capped2=True,amp=25.0,period=25.0,width=5.0):
  p1 = numpy.array(p1,dtype=numpy.dtype(float))
  p2 = numpy.array(p2,dtype=numpy.dtype(float))
  propVec = p2-p1
  #print "fullPropVec: ",propVec
  distance = sqrt(numpy.dot(propVec,propVec))
  nLoops = int(distance/period)
  period = distance/nLoops
  normedPropVec = propVec/distance
  normedPerpVec = numpy.array([-normedPropVec[1],normedPropVec[0]])
  ampVec = amp*normedPerpVec
  propVec /= nLoops
  loopDistance = distance/nLoops
  #print "propVec: ",propVec
  #print "ampVec: ",ampVec
  #print "normedPropVec",normedPropVec
  #print "normedPerpVec",normedPerpVec
  #print "distance: ",distance
  #print "nLoops: ",nLoops
  #print "period: ",period
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
  return makeEndPoints(p1,p2,width)

def straightLine(path,p1,p2,capped1=True,capped2=True,width=5.0):
  p1 = numpy.array(p1,dtype=numpy.dtype(float))
  p2 = numpy.array(p2,dtype=numpy.dtype(float))
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
  return makeEndPoints(p1,p2,width)

def straightLineArrow(path,p1,p2,capped1=True,capped2=True,forward=True,width=5.0,arrowLength=15.0,arrowWidth=None):
  if arrowWidth == None:
    arrowWidth = width
  p1 = numpy.array(p1,dtype=numpy.dtype(float))
  p2 = numpy.array(p2,dtype=numpy.dtype(float))
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
  return makeEndPoints(p1,p2,width)

def vertexCircle(path,p1,endList,radius=5.):
  p1 = numpy.array(p1,dtype=numpy.dtype(float))
  thisVertexEnds = []
  for obj in endList:
    for end in obj:
      tmpDist = -1.
      for point in end:
        propVec = p1-point
        distance = sqrt(numpy.dot(propVec,propVec))
        if abs(distance-radius) < 1.:
          if tmpDist > 0. and tmpDist -distance < 0.05:
            thisVertexEnds.append(end)
            newRad = distance
          else:
            tmpDist = distance
  #print "nEnds: ",len(thisVertexEnds)
  endsList = []
  for end in thisVertexEnds:
    vec0 = end[0]-p1
    vec1 = end[1]-p1
    #print vec0
    #print vec1
    angle0 =  numpy.arctan2(*list(vec0))
    angle1 =  numpy.arctan2(*list(vec1))
    #angleSwept  = numpy.arctan2(*list(vec1))-numpy.arctan2(*list(vec0))
    #print angleSwept
    #sweepFlag = 1
    #if angleSwept < 0.:
    #  sweepFlag = 0
    #path.push(['M']+list(end[0]))
    #largeArc = 1
    #path.push(['A']+[newRad,newRad,0,largeArc,sweepFlag]+list(end[1]))
    firstAngle = angle0
    secondAngle = angle1
    firstPoint = end[0]
    secondPoint = end[1]
    advanceAngle = secondAngle-firstAngle
    if advanceAngle > numpy.pi and  advanceAngle < 2*numpy.pi:
      advanceAngle -= 2*numpy.pi
    if advanceAngle < -numpy.pi and  advanceAngle > -2*numpy.pi:
      advanceAngle += 2*numpy.pi
    if advanceAngle<0.:
      firstAngle = angle1
      secondAngle = angle0
      firstPoint = end[1]
      secondPoint = end[0]
    dataDict = {'first':firstPoint,'second':secondPoint,'firstAngle':firstAngle,'secondAngle':secondAngle}
    endsList.append(dataDict)
  endsList.sort(key=lambda x: x['firstAngle'])
  #print "******************"
  #for i,end in enumerate(endsList):
  #  print i
  #  print end
  #print "###################"
  for i,end in enumerate(endsList):
    #print list(endsList[i-1]['second'])
    #print list(end['first'])
    path.push(['M']+list(endsList[i-1]['second']))
    advanceAngle = end['firstAngle'] - endsList[i-1]['secondAngle']
    #print end['firstAngle']*180/numpy.pi , endsList[i-1]['secondAngle']*180/numpy.pi
    #print advanceAngle*180/numpy.pi
    sweepFlag = 1
    if advanceAngle < 0.:
      sweepFlag = 0
    sweepFlag = 0
    if advanceAngle > numpy.pi and  advanceAngle < 2*numpy.pi:
      advanceAngle -= 2*numpy.pi
    if advanceAngle < -numpy.pi and  advanceAngle > -2*numpy.pi:
      advanceAngle += 2*numpy.pi
    largeArc = 1
    if abs(advanceAngle) < numpy.pi:
      largeArc = 0
    #print advanceAngle*180/numpy.pi
    #print sweepFlag,largeArc
    path.push(['A']+[newRad,newRad,0,largeArc,sweepFlag]+list(end['first']))

color = svgwrite.rgb(0, 0, 255) # for cutting
colorEngrave = svgwrite.rgb(255, 0, 0) # for engraving
#color = colorEngrave
width = "0.01mm" # production value
width = "0.2mm" # testing value

#dwg = svgwrite.Drawing('test.svg',size=("181mm","181mm"),viewBox="0 0 181 181")
#path = dwg.path(None,stroke=color,stroke_width=width,fill="none")
#wlEnds = wavyLine(path,(20,70),(160,70),capped2=False)
#vertexCircle(path,(165,70),[wlEnds])
#sl1Ends = straightLineArrow(path,(20,100),(160,100),forward=False)
#sl2Ends = straightLineArrow(path,(20,125),(160,125),forward=True,capped1=False)
#vertexCircle(path,(15,125),[sl2Ends])
#sl3Ends = straightLine(path,(20,150),(160,150),capped2=False)
#vertexCircle(path,(165,150),[sl3Ends])
#spEnds =  spiralLine(path,(20,40),(160,40))
#dwg.add(path)
#dwg.save()

dwg = svgwrite.Drawing('test.svg',size=("181mm","181mm"),viewBox="0 0 181 181")
path = dwg.path(None,stroke=color,stroke_width=width,fill="none")
sl1Ends = straightLineArrow(path,(10,160),(100,160),forward=False,capped2=False)
sl2Ends = straightLineArrow(path,(110,160),(170,160),forward=False,capped1=False)
sl3Ends = straightLineArrow(path,(105,155),(105,50),forward=True,capped1=False)
vertexCircle(path,(105,160),[sl1Ends,sl2Ends,sl3Ends])
dwg.add(path)
dwg.save()
