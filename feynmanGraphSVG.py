#!/usr/bin/env python

import numpy
import svgwrite
from math import sqrt,pi

def subtractVertexDistance(p1,p2,width):
  p1 = numpy.array(p1,dtype=numpy.dtype(float))
  p2 = numpy.array(p2,dtype=numpy.dtype(float))
  propVec = p2-p1
  distance = sqrt(numpy.dot(propVec,propVec))
  normedPropVec = propVec/distance
  normedPerpVec = numpy.array([-normedPropVec[1],normedPropVec[0]])
  return p1+width*normedPropVec,p2-width*normedPropVec

def rotate(p1,angle):
  p1 = numpy.array(p1,dtype=numpy.dtype(float))
  angle *= numpy.pi/180.
  rotMatrix = numpy.array([[numpy.cos(angle), -numpy.sin(angle)], 
                   [numpy.sin(angle),  numpy.cos(angle)]])
  result =  rotMatrix.dot(p1)
  return result

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

def wavyLine(path,p1,p2,capped1=True,capped2=True,amp=7.,period=23.0,width=5.0):
  p1,p2 = subtractVertexDistance(p1,p2,width)
  width2 = 1.5*width
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
    path.push(['l']+list(normedPerpVec*width2/2.))
  else:
    path.push(['m']+list(normedPerpVec*width2/2.))
  for iOsc in range(nOsc):
    path.push(['q']+list(propVec+ampVec+quartWidthPropVec)+list(2*propVec+ampVec+2*quartWidthPropVec))
    path.push(['q']+list(propVec+quartWidthPropVec)+list(2*propVec-ampVec+2*quartWidthPropVec))
    nExtra+=4
    path.push(['q']+list(propVec-ampVec)+list(2*propVec-ampVec))
    path.push(['q']+list(propVec)+list(2*propVec+ampVec))
  path.push(['l']+list(2*quartWidthPropVec))
  nExtra+=2
  if capped2:
    path.push(['l']+list(-normedPerpVec*width2))
  else:
    path.push(['m']+list(-normedPerpVec*width2))
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
    path.push(['l']+list(normedPerpVec*width2/2.))
  else:
    path.push(['m']+list(normedPerpVec*width2/2.))
  #print "nExtra",nExtra
  return makeEndPoints(p1,p2,width2)

def spiralLine(path,p1,p2,capped1=True,capped2=True,amp=23.0,period=23.0,width=5.):
  width2 = width
  widthSF = 0.97
  width = widthSF*width2
  p1,p2 = subtractVertexDistance(p1,p2,width)
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
  path.push(['M']+list(p1))
  if capped1:
    path.push(['l']+list(normedPerpVec*width2/2.))
  else:
    path.push(['m']+list(normedPerpVec*width2/2.))
  for iCrossings in range(nLoops):
    path.push(['q']+list(0.25*propVec)+list(0.5*propVec-0.2*ampVec))
    path.push(['q']+list(0.25*propVec+0.2*ampVec)+list(0.5*propVec+0.2*ampVec))
  if capped2:
    path.push(['l']+list(-normedPerpVec*width2))
  else:
    path.push(['m']+list(-normedPerpVec*width2))
  propVec *= -1
  for iCrossings in range(nLoops):
    path.push(['q']+list(-0.25*(loopDistance-2*width)*normedPropVec)+list(-0.5*(loopDistance-2*width)*normedPropVec-0.16*ampVec))
    path.push(['c']+list(2*normedPropVec*width-0.5*ampVec)+list(2*normedPropVec*width-ampVec)+list(-normedPropVec*width-ampVec))
    path.push(['c']+list(-3*normedPropVec*width)+list(-3*normedPropVec*width+0.5*ampVec)+list(-normedPropVec*width+ampVec))
    path.push(['m']+list(normedPropVec*width-normedPerpVec*width))
    path.push(['c']+list(2*normedPropVec*width-0.5*((amp-2*width)*normedPerpVec))+list(normedPropVec*width-((amp-2*width)*normedPerpVec))+list(-(amp-2*width)*normedPerpVec))
    path.push(['m']+list((amp-2*width)*normedPerpVec))
    path.push(['c']+list(-2*normedPropVec*width-0.5*((amp-2*width)*normedPerpVec))+list(-normedPropVec*width-((amp-2*width)*normedPerpVec))+list(-(amp-2*width)*normedPerpVec))
    path.push(['m']+list(-normedPropVec*width+normedPerpVec*width+(amp-2*width)*normedPerpVec))
    path.push(['q']+list(-0.25*(loopDistance-2*width)*normedPropVec+0.16*ampVec)+list(-0.5*(loopDistance-2*width)*normedPropVec+0.16*ampVec))
  if capped1:
    path.push(['l']+list(normedPerpVec*width2/2.))
  else:
    path.push(['m']+list(normedPerpVec*width2/2.))
  return makeEndPoints(p1,p2,width2)

def straightLine(path,p1,p2,capped1=True,capped2=True,width=5.0):
  p1,p2 = subtractVertexDistance(p1,p2,width)
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
  p1,p2 = subtractVertexDistance(p1,p2,width)
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
  radiusList = []
  for obj in endList:
    for end in obj:
      otherPointNearVertex = False
      for point in end:
        propVec = p1-point
        distance = sqrt(numpy.dot(propVec,propVec))
        if abs(distance-radius) < 1.5:
          if otherPointNearVertex:
            thisVertexEnds.append(end)
            radiusList.append(distance)
          else:
            otherPointNearVertex = True
  newRad = numpy.mean(radiusList)
  #print "nEnds: ",len(thisVertexEnds)
  endsList = []
  for end in thisVertexEnds:
    vec0 = end[0]-p1
    vec1 = end[1]-p1
    vecCenter = vec1+vec0
    angleCenter = numpy.arctan2(vecCenter[1],vecCenter[0])
    #print vec0
    #print vec1
    angle0 =  numpy.arctan2(vec0[1],vec0[0])
    angle1 =  numpy.arctan2(vec1[1],vec1[0])
    crossesBoundary = abs(angle0)<numpy.pi/2.
    crossesBoundary = crossesBoundary and angle0/abs(angle0) != angle1/abs(angle1)
    if angle0 < 0.:
      angle0 += 2*numpy.pi
    if angle1 < 0.:
      angle1 += 2*numpy.pi
    if angleCenter < 0.:
      angleCenter += 2*numpy.pi
    firstAngle = angle0
    secondAngle = angle1
    firstPoint = end[0]
    secondPoint = end[1]
    advanceAngle = secondAngle-firstAngle
    if (advanceAngle<0. and advanceAngle> -1.5*numpy.pi) or advanceAngle> 1.5*numpy.pi:
      firstAngle = angle1
      secondAngle = angle0
      firstPoint = end[1]
      secondPoint = end[0]
    dataDict = {'first':firstPoint,'second':secondPoint,'firstAngle':firstAngle,'secondAngle':secondAngle,'crossesBoundary':crossesBoundary,'angleCenter':angleCenter}
    endsList.append(dataDict)
  endsList.sort(key=lambda x: x['angleCenter'])
  #print "******************"
  #print "circle coords: ",p1
  #for i,end in enumerate(endsList):
  #  print i
  #  print end
  #print "###################"
  #path.push(['M']+list(p1))
  #path.push(['l']+[newRad,0.])
  #path.push(['M']+list(p1))
  #path.push(['l']+[0.,newRad])
  for i,end in enumerate(endsList):
    #if i != 0:
    #    continue
    #print list(endsList[i-1]['second'])
    #print list(end['first'])
    path.push(['M']+list(endsList[i-1]['second']))
    advanceAngle = end['firstAngle'] - endsList[i-1]['secondAngle']
    #print end['firstAngle']*180/numpy.pi , endsList[i-1]['secondAngle']*180/numpy.pi
    #print advanceAngle*180/numpy.pi
    isSame = endsList[i] is endsList[i-1]
    #print "isSame: ",isSame
    sweepFlag = None
    largeArc = None
    if advanceAngle <= 0 and abs(advanceAngle) > numpy.pi:
      sweepFlag = 1
      largeArc = 0
      if isSame:
        sweepFlag = 0
        largeArc = 1
      elif end['crossesBoundary']:
        sweepFlag = 1
        largeArc = 1
    elif advanceAngle > 0 and abs(advanceAngle) > numpy.pi:
      sweepFlag = 1
      largeArc = 0
      if isSame:
        sweepFlag = 1
        largeArc = 1
    elif advanceAngle <= 0 and abs(advanceAngle) <= numpy.pi:
      sweepFlag = 1
      largeArc = 1
    elif advanceAngle > 0 and abs(advanceAngle) <= numpy.pi:
      sweepFlag = 1
      largeArc = 0
    #print sweepFlag,largeArc
    path.push(['A']+[newRad,newRad,0,largeArc,sweepFlag]+list(end['first']))

#dwg = svgwrite.Drawing('test.svg',size=("181mm","181mm"),viewBox="0 0 181 181")
#dwg = svgwrite.Drawing('test.svg',size=("384mm","384mm"),viewBox="0 0 384 384")
#dwg = svgwrite.Drawing('test.svg',size=("790mm","384mm"),viewBox="0 0 790 384")
color = svgwrite.rgb(0, 0, 255) # for cutting
colorEngrave = svgwrite.rgb(255, 0, 0) # for engraving
#color = colorEngrave
suffix = ""
if color == colorEngrave:
  suffix = "_engrave"
width = "0.01mm" # production value
width = "0.2mm" # testing value

## Test 1 w/o vertex
dwg = svgwrite.Drawing('test1'+suffix+'.svg',size=("181mm","181mm"),viewBox="0 0 181 181")
path = dwg.path(None,stroke=color,stroke_width=width,fill="none")
wlEnds = wavyLine(path,(10,70),(170,70),capped1=True,capped2=True)
sl1Ends = straightLineArrow(path,(10,100),(170,100),forward=True,capped1=True,capped2=True)
sl2Ends = straightLineArrow(path,(10,125),(170,125),forward=False,capped1=True,capped2=True)
sl3Ends = straightLine(path,(10,150),(170,160),capped1=True,capped2=True)
spEnds =  spiralLine(path,(10,40),(170,40),capped1=True,capped2=True)
dwg.add(path)
dwg.save()


## Test 2 with vertex
dwg = svgwrite.Drawing('test2'+suffix+'.svg',size=("181mm","181mm"),viewBox="0 0 181 181")
path = dwg.path(None,stroke=color,stroke_width=width,fill="none")
wlEnds = wavyLine(path,(20,70),(160,70),capped1=False,capped2=False)
vertexCircle(path,(160,70),[wlEnds])
vertexCircle(path,(20,70),[wlEnds])
sl1Ends = straightLineArrow(path,(20,100),(160,100),forward=False,capped1=False,capped2=False)
vertexCircle(path,(160,100),[sl1Ends])
vertexCircle(path,(20,100),[sl1Ends])
sl2Ends = straightLineArrow(path,(20,125),(160,125),forward=True,capped1=False,capped2=False)
vertexCircle(path,(160,125),[sl2Ends])
vertexCircle(path,(20,125),[sl2Ends])
sl3Ends = straightLine(path,(20,150),(160,160),capped1=False,capped2=False)
vertexCircle(path,(20,150),[sl3Ends])
vertexCircle(path,(160,160),[sl3Ends])
spEnds =  spiralLine(path,(20,40),(160,40),capped1=False,capped2=False)
vertexCircle(path,(160,40),[spEnds])
vertexCircle(path,(20,40),[spEnds])
dwg.add(path)
dwg.save()

## Test 3 Diagram
dwg = svgwrite.Drawing('test3'+suffix+'.svg',size=("181mm","181mm"),viewBox="0 0 181 181")
path = dwg.path(None,stroke=color,stroke_width=width,fill="none")
sl1Ends = straightLineArrow(path,(10,160),(100,120),forward=False,capped2=False)
sl2Ends = straightLineArrow(path,(100,120),(170,160),forward=False,capped1=False)
wgEnds = wavyLine(path,(100,55),(100,120),capped1=False,capped2=False)
vertexCircle(path,(100,120),[sl1Ends,sl2Ends,wgEnds])
sp1Ends = spiralLine(path,(15,25),(100,55),capped2=False)
sp2Ends = spiralLine(path,(165,15),(100,55),capped2=False)
vertexCircle(path,(100,55),[sp1Ends,sp2Ends,wgEnds])
tri1 = (10,40)
tri2 = (10,120)
tri3 = (80,80)
sl3Ends = straightLineArrow(path,tri1,tri2,forward=False,capped1=False,capped2=False)
sl4Ends = straightLineArrow(path,tri2,tri3,forward=False,capped1=False,capped2=False)
sl5Ends = straightLineArrow(path,tri3,tri1,forward=False,capped1=False,capped2=False)
vertexCircle(path,tri1,[sl3Ends,sl5Ends])
vertexCircle(path,tri2,[sl3Ends,sl4Ends])
vertexCircle(path,tri3,[sl4Ends,sl5Ends])
dwg.add(path)
dwg.save()


# Vertex Tests
dwg = svgwrite.Drawing('testVertex.svg',size=("181mm","181mm"),viewBox="0 0 181 181")
path = dwg.path(None,stroke=color,stroke_width=width,fill="none")
wlEnds = wavyLine(path,(20,20),(160,20),capped1=False,capped2=False)
vertexCircle(path,(160,20),[wlEnds])
vertexCircle(path,(20,20),[wlEnds])
sl1Ends = straightLineArrow(path,(20,50),(20,170),forward=False,capped1=False,capped2=False)
vertexCircle(path,(20,170),[sl1Ends])
vertexCircle(path,(20,50),[sl1Ends])
sl0Ends = straightLineArrow(path,(40,70),(90,40),forward=True,capped1=False,capped2=False)
sl4Ends = straightLineArrow(path,(170,100),(90,40),forward=True,capped1=False,capped2=False)
vertexCircle(path,(40,70),[sl0Ends])
vertexCircle(path,(170,100),[sl4Ends])
vertexCircle(path,(90,40),[sl0Ends,sl4Ends])
sl5Ends = straightLineArrow(path,(90,120),(90,40),forward=True,capped1=False,capped2=False)
sl6Ends = straightLineArrow(path,(90,120),(40,120),forward=True,capped1=False,capped2=False)
sl7Ends = straightLineArrow(path,(90,120),(170,120),forward=True,capped1=False,capped2=False)
sl8Ends = straightLineArrow(path,(90,120),(90,170),forward=True,capped1=False,capped2=False)
vertexCircle(path,(90,120),[sl5Ends,sl6Ends,sl7Ends,sl8Ends])
dwg.add(path)
dwg.save()

## test4 Toward 2 2->2 Diagrams
dwg = svgwrite.Drawing('test4.svg',size=("384mm","384mm"),viewBox="0 0 384 384")
path = dwg.path(None,stroke=color,stroke_width=width,fill="none")
q1 = (10,10)
q1p = (182,10)
q1B = (96,268/3.+10)
q2 = (10,278)
q2p = (182,278)
q2B = (96,2*268/3.+10)
q1Ends = straightLineArrow(path,q1,q1B,forward=True,capped2=False)
q1pEnds = straightLineArrow(path,q1p,q1B,forward=False,capped2=False)
q2Ends = straightLineArrow(path,q2,q2B,forward=True,capped2=False)
q2pEnds = straightLineArrow(path,q2p,q2B,forward=False,capped2=False)
BEnds = wavyLine(path,q1B,q2B,capped1=False,capped2=False)
vertexCircle(path,q1B,[q1Ends,q1pEnds,BEnds])
vertexCircle(path,q2B,[q2Ends,q2pEnds,BEnds])
q1 = numpy.array(q1)+numpy.array([192,0])
q1p = numpy.array(q1p)+numpy.array([192,0])
q1B = numpy.array(q1B)+numpy.array([192,0])
q2 = numpy.array(q2)+numpy.array([192,0])
q2p = numpy.array(q2p)+numpy.array([192,0])
q2B = numpy.array(q2B)+numpy.array([192,0])
q1Ends = spiralLine(path,q1,q1B,capped2=False)
q1pEnds = straightLineArrow(path,q1p,q1B,forward=False,capped2=False)
q2Ends = straightLineArrow(path,q2,q2B,forward=True,capped2=False)
q2pEnds = spiralLine(path,q2p,q2B,capped2=False)
BEnds = straightLineArrow(path,q1B,q2B,forward=False,capped1=False,capped2=False)
vertexCircle(path,q1B,[q1Ends,q1pEnds,BEnds])
vertexCircle(path,q2B,[q2Ends,q2pEnds,BEnds])
tri1 = (152,140)
tri2 = (232,140)
tri3 = (192,75)
g1 = (132,220)
g2 = (252,220)
h1 = (192,5)
sl3Ends = straightLineArrow(path,tri1,tri2,forward=False,capped1=False,capped2=False)
sl4Ends = straightLineArrow(path,tri2,tri3,forward=False,capped1=False,capped2=False)
sl5Ends = straightLineArrow(path,tri3,tri1,forward=False,capped1=False,capped2=False)
g1Ends = spiralLine(path,tri1,g1,capped1=False)
g2Ends = spiralLine(path,g2,tri2,capped2=False)
h1Ends = straightLine(path,tri3,h1,capped1=False)
#h1Ends = wavyLine(path,tri3,h1,capped1=False)
vertexCircle(path,tri1,[sl3Ends,sl5Ends,g1Ends])
vertexCircle(path,tri2,[sl3Ends,sl4Ends,g2Ends])
vertexCircle(path,tri3,[sl4Ends,sl5Ends,h1Ends])
q1 = (33,380)
q1p = (159,380)
q1B = (96,320)
B = (96,225)
q1Ends = straightLineArrow(path,q1,q1B,forward=True,capped2=False)
q1pEnds = straightLineArrow(path,q1p,q1B,forward=False,capped2=False)
BEnds = spiralLine(path,q1B,B,capped1=False,capped2=True)
vertexCircle(path,q1B,[q1Ends,q1pEnds,BEnds])
q1 = numpy.array(q1)+numpy.array([192,0])
q1p = numpy.array(q1p)+numpy.array([192,0])
q1B = numpy.array(q1B)+numpy.array([192,0])
B = numpy.array(B)+numpy.array([192,0])
B[1] += 20.
q1Ends = straightLineArrow(path,q1,q1B,forward=True,capped2=False)
q1pEnds = straightLineArrow(path,q1p,q1B,forward=False,capped2=False)
BEnds = wavyLine(path,q1B,B,capped1=False,capped2=True)
vertexCircle(path,q1B,[q1Ends,q1pEnds,BEnds])
dwg.add(path)
dwg.save()


## H->ff 384x384
dwg = svgwrite.Drawing('Hff.svg',size=("384mm","384mm"),viewBox="0 0 384 384")
path = dwg.path(None,stroke=color,stroke_width=width,fill="none")
q1 = (5,85)
q1p = (5,384)
q1B = (40,212)
q2 = (229,85)
q2p = (229,384)
q2B = (194,212)
BB = (117,212)
Hff = (117,284)
f1 = (71,384)
f2 = (172,384)
q1Ends = straightLineArrow(path,q1,q1B,forward=True,capped2=False)
q2Ends = straightLineArrow(path,q2,q2B,forward=True,capped2=False)
q1pEnds = straightLineArrow(path,q1p,q1B,forward=False,capped2=False)
q2pEnds = straightLineArrow(path,q2p,q2B,forward=False,capped2=False)
B1Ends = wavyLine(path,q1B,BB,capped1=False,capped2=False)
B2Ends = wavyLine(path,q2B,BB,capped1=False,capped2=False)
HEnds = straightLine(path,Hff,BB,capped1=False,capped2=False)
f1Ends = straightLineArrow(path,Hff,f1,forward=False,capped1=False)
f2Ends = straightLineArrow(path,Hff,f2,forward=True,capped1=False)
vertexCircle(path,q1B,[q1Ends,q1pEnds,B1Ends])
vertexCircle(path,q2B,[q2Ends,q2pEnds,B2Ends])
vertexCircle(path,BB,[HEnds,B1Ends,B2Ends])
vertexCircle(path,Hff,[HEnds,f1Ends,f2Ends])
tri1 = (275,290)
tri2 = (355,290)
tri3 = (315,225)
g1 = (255,385)
g2 = (375,385)
Hff = (315,160)
f1 = (260,85)
f2 = (370,85)
sl3Ends = straightLineArrow(path,tri1,tri2,forward=False,capped1=False,capped2=False)
sl4Ends = straightLineArrow(path,tri2,tri3,forward=False,capped1=False,capped2=False)
sl5Ends = straightLineArrow(path,tri3,tri1,forward=False,capped1=False,capped2=False)
g1Ends = spiralLine(path,tri1,g1,capped1=False)
g2Ends = spiralLine(path,g2,tri2,capped2=False)
HEnds = straightLine(path,tri3,Hff,capped1=False,capped2=False)
f1Ends = straightLineArrow(path,Hff,f1,forward=False,capped1=False)
f2Ends = straightLineArrow(path,Hff,f2,forward=True,capped1=False)
vertexCircle(path,tri1,[sl3Ends,sl5Ends,g1Ends])
vertexCircle(path,tri2,[sl3Ends,sl4Ends,g2Ends])
vertexCircle(path,tri3,[sl4Ends,sl5Ends,HEnds])
vertexCircle(path,Hff,[HEnds,f1Ends,f2Ends])
q1 = (320,5)
q1p = (320,125)
q1B = (255,60)
BH = numpy.array((170.,60.))
B2 = rotate(numpy.array((0.,-80.)),-45.)+BH
Hff = rotate(numpy.array((0.,60.)),45.)+BH
f1 = rotate(numpy.array((60.,70.)),45.)+Hff
f2 = rotate(numpy.array((-60.,70.)),45.)+Hff
q1Ends = straightLineArrow(path,q1,q1B,forward=True,capped2=False)
q1pEnds = straightLineArrow(path,q1p,q1B,forward=False,capped2=False)
BEnds = wavyLine(path,q1B,BH,capped1=False,capped2=False)
B2Ends = wavyLine(path,BH,B2,capped1=False,capped2=True)
HEnds = straightLine(path,BH,Hff,capped1=False,capped2=False)
f1Ends = straightLineArrow(path,Hff,f1,forward=False,capped1=False)
f2Ends = straightLineArrow(path,Hff,f2,forward=True,capped1=False)
vertexCircle(path,q1B,[q1Ends,q1pEnds,BEnds])
vertexCircle(path,BH,[HEnds,BEnds,B2Ends])
vertexCircle(path,Hff,[HEnds,f1Ends,f2Ends])
dwg.add(path)
dwg.save()

## H->gamma gamma 384x384
dwg = svgwrite.Drawing('Hgamgam.svg',size=("384mm","384mm"),viewBox="0 0 384 384")
path = dwg.path(None,stroke=color,stroke_width=width,fill="none")
tri1 = numpy.array((275,290))
tri2 = numpy.array((355,290))
tri3 = numpy.array((315,225))
tri21 = tri1*numpy.array([1.,-1.])+numpy.array([0.,2*225.-70])
tri22 = tri2*numpy.array([1.,-1.])+numpy.array([0.,2*225.-70])
tri23 = tri3*numpy.array([1.,-1.])+numpy.array([0.,2*225.-70])
g1 = (255,385)
g2 = (375,385)
B1 = (255,3)
B2 = (375,3)
sl3Ends = straightLineArrow(path,tri1,tri2,forward=False,capped1=False,capped2=False)
sl4Ends = straightLineArrow(path,tri2,tri3,forward=False,capped1=False,capped2=False)
sl5Ends = straightLineArrow(path,tri3,tri1,forward=False,capped1=False,capped2=False)
g1Ends = spiralLine(path,tri1,g1,capped1=False)
g2Ends = spiralLine(path,g2,tri2,capped2=False)
HEnds = straightLine(path,tri3,tri23,capped1=False,capped2=False)
sl6Ends = straightLineArrow(path,tri21,tri22,forward=False,capped1=False,capped2=False)
sl7Ends = straightLineArrow(path,tri22,tri23,forward=False,capped1=False,capped2=False)
sl8Ends = straightLineArrow(path,tri23,tri21,forward=False,capped1=False,capped2=False)
B1Ends = wavyLine(path,tri21,B1,capped1=False,capped2=True)
B2Ends = wavyLine(path,tri22,B2,capped1=False,capped2=True)
vertexCircle(path,tri1,[sl3Ends,sl5Ends,g1Ends])
vertexCircle(path,tri2,[sl3Ends,sl4Ends,g2Ends])
vertexCircle(path,tri3,[sl4Ends,sl5Ends,HEnds])
vertexCircle(path,tri21,[sl6Ends,sl8Ends,B1Ends])
vertexCircle(path,tri22,[sl6Ends,sl7Ends,B2Ends])
vertexCircle(path,tri23,[sl7Ends,sl8Ends,HEnds])
q1 = (5,5)
q1p = (5,304)
q1B = (40,132)
q2 = (229,5)
q2p = (229,304)
q2B = (194,132)
BB = (117,132)
f1 = (52,375)  #(71,304)
f2 = (182,375) #(172,304)
tri1 = numpy.array((77,269))  #numpy.array((275,290))
tri2 = numpy.array((157,269))  #numpy.array((355,290))
tri3 = numpy.array((117,204))  #numpy.array((315,225))
q1Ends = straightLineArrow(path,q1,q1B,forward=True,capped2=False)
q2Ends = straightLineArrow(path,q2,q2B,forward=True,capped2=False)
q1pEnds = straightLineArrow(path,q1p,q1B,forward=False,capped2=False)
q2pEnds = straightLineArrow(path,q2p,q2B,forward=False,capped2=False)
B1Ends = wavyLine(path,q1B,BB,capped1=False,capped2=False)
B2Ends = wavyLine(path,q2B,BB,capped1=False,capped2=False)
HEnds = straightLine(path,tri3,BB,capped1=False,capped2=False)
f1Ends = wavyLine(path,tri1,f1,capped1=False)
f2Ends = wavyLine(path,tri2,f2,capped1=False)
sl3Ends = straightLineArrow(path,tri1,tri2,forward=False,capped1=False,capped2=False)
sl4Ends = straightLineArrow(path,tri2,tri3,forward=False,capped1=False,capped2=False)
sl5Ends = straightLineArrow(path,tri3,tri1,forward=False,capped1=False,capped2=False)
vertexCircle(path,q1B,[q1Ends,q1pEnds,B1Ends])
vertexCircle(path,q2B,[q2Ends,q2pEnds,B2Ends])
vertexCircle(path,BB,[HEnds,B1Ends,B2Ends])
vertexCircle(path,tri3,[sl4Ends,sl5Ends,HEnds])
vertexCircle(path,tri1,[sl3Ends,sl5Ends,f1Ends])
vertexCircle(path,tri2,[sl3Ends,sl4Ends,f2Ends])
dwg.add(path)
dwg.save()

## H->VV 384x384
dwg = svgwrite.Drawing('HVV.svg',size=("384mm","384mm"),viewBox="0 0 384 384")
path = dwg.path(None,stroke=color,stroke_width=width,fill="none")
tri1 = (152,290)
tri2 = (232,290)
tri3 = (192,225)
g1 = (132,385)
g2 = (252,385)
Hvv = numpy.array((192,160))
v1 = numpy.array((137,92))
v2 = numpy.array((247,92))
f1 = v1+numpy.array((-89,-25))
f2 = v1+numpy.array((-7,-92))
f3 = v2+numpy.array((7,-92))
f4 = v2+numpy.array((89,-25))
sl3Ends = straightLineArrow(path,tri1,tri2,forward=False,capped1=False,capped2=False)
sl4Ends = straightLineArrow(path,tri2,tri3,forward=False,capped1=False,capped2=False)
sl5Ends = straightLineArrow(path,tri3,tri1,forward=False,capped1=False,capped2=False)
g1Ends = spiralLine(path,tri1,g1,capped1=False)
g2Ends = spiralLine(path,g2,tri2,capped2=False)
HEnds = straightLine(path,tri3,Hvv,capped1=False,capped2=False)
v1Ends = wavyLine(path,Hvv,v1,capped1=False,capped2=False)
v2Ends = wavyLine(path,Hvv,v2,capped1=False,capped2=False)
f1Ends = straightLineArrow(path,v1,f1,capped1=False)
f2Ends = straightLineArrow(path,v1,f2,forward=False,capped1=False)
f3Ends = straightLineArrow(path,v2,f3,capped1=False)
f4Ends = straightLineArrow(path,v2,f4,forward=False,capped1=False)
vertexCircle(path,tri1,[sl3Ends,sl5Ends,g1Ends])
vertexCircle(path,tri2,[sl3Ends,sl4Ends,g2Ends])
vertexCircle(path,tri3,[sl4Ends,sl5Ends,HEnds])
vertexCircle(path,Hvv,[HEnds,v1Ends,v2Ends])
vertexCircle(path,v1,[v1Ends,f1Ends,f2Ends])
vertexCircle(path,v2,[v2Ends,f3Ends,f4Ends])
# gg->gam gam Box diagram
goVec = numpy.array((0,-97))
g1 = numpy.array((270,385))
g2 = g1+numpy.array((97,0))
box1 = g1+goVec
box2 = g2+goVec
box3 = box1+goVec
box4 = box2+goVec
B1 = box3+goVec
B2 = box4+goVec
sl1Ends = straightLineArrow(path,box2,box1,forward=False,capped1=False,capped2=False)
sl2Ends = straightLineArrow(path,box1,box3,forward=False,capped1=False,capped2=False)
sl3Ends = straightLineArrow(path,box3,box4,forward=False,capped1=False,capped2=False)
sl4Ends = straightLineArrow(path,box4,box2,forward=False,capped1=False,capped2=False)
g1Ends = spiralLine(path,box1,g1,capped1=False)
g2Ends = spiralLine(path,g2,box2,capped2=False)
B1Ends = wavyLine(path,box3,B1,capped1=False,capped2=True)
B2Ends = wavyLine(path,box4,B2,capped1=False,capped2=True)
vertexCircle(path,box1,[sl1Ends,sl2Ends,g1Ends])
vertexCircle(path,box2,[sl1Ends,sl4Ends,g2Ends])
vertexCircle(path,box3,[sl2Ends,sl3Ends,B1Ends])
vertexCircle(path,box4,[sl3Ends,sl4Ends,B2Ends])
## qqbar->4f background
q1In = numpy.array((42,383))
q2In = q1In+numpy.array((79,0))
v1 = q1In+numpy.array((0,-80))
v2 = q2In+numpy.array((0,-80))
v3 = v1+numpy.array((0,-80))
v4 = v2+numpy.array((0,-80))
f1Out = v3+numpy.array((-37,-70))
f2Out = v3+numpy.array((+37,-70))
f3Out = v4+numpy.array((-37,-70))
f4Out = v4+numpy.array((+37,-70))
q1Ends = straightLineArrow(path,q1In,v1,forward=True,capped1=True,capped2=False)
q2Ends = straightLineArrow(path,q2In,v2,forward=False,capped1=True,capped2=False)
qTEnds = straightLineArrow(path,v1,v2,forward=True,capped1=False,capped2=False)
v1Ends = wavyLine(path,v1,v3,capped1=False,capped2=False)
v2Ends = wavyLine(path,v2,v4,capped1=False,capped2=False)
f1Ends = straightLineArrow(path,f1Out,v3,forward=False,capped1=True,capped2=False)
f2Ends = straightLineArrow(path,f2Out,v3,forward=True,capped1=True,capped2=False)
f3Ends = straightLineArrow(path,f3Out,v4,forward=False,capped1=True,capped2=False)
f4Ends = straightLineArrow(path,f4Out,v4,forward=True,capped1=True,capped2=False)
vertexCircle(path,v1,[q1Ends,qTEnds,v1Ends])
vertexCircle(path,v2,[q2Ends,qTEnds,v2Ends])
vertexCircle(path,v3,[f1Ends,f2Ends,v1Ends])
vertexCircle(path,v4,[f3Ends,f4Ends,v2Ends])
dwg.add(path)
dwg.save()

### Penguin 384x384  ## Need curves to do correctly!!
#dwg = svgwrite.Drawing('Penguin.svg',size=("384mm","384mm"),viewBox="0 0 384 384")
#path = dwg.path(None,stroke=color,stroke_width=width,fill="none")
#armL = numpy.array((2,70))
#neckL = armL+numpy.array((80,-20))
#neckR = neckL + numpy.array((150,0))
#armR = neckR+numpy.array((80,20))
#gluT = (neckL+neckR)/2+numpy.array((0,170))
#gluB = gluT+numpy.array((0,50))
#legL = gluB+numpy.array((-55,70))
#legR = gluB+numpy.array((55,70))
#armLEnds = straightLineArrow(path,armL,neckL,forward=True,capped1=True,capped2=False)
#armREnds = straightLineArrow(path,armR,neckR,forward=False,capped1=True,capped2=False)
#neckEnds = wavyLine(path,neckL,neckR,capped1=False,capped2=False)
#bodyLEnds = straightLineArrow(path,neckL,gluT,capped1=False,capped2=False)
#bodyREnds = straightLineArrow(path,neckR,gluT,forward=False,capped1=False,capped2=False)
#gluEnds = wavyLine(path,gluB,gluT,capped1=False,capped2=False)
#legLEnds = straightLineArrow(path,legL,gluB,forward=True,capped1=True,capped2=False)
#legREnds = straightLineArrow(path,legR,gluB,forward=False,capped1=True,capped2=False)
#vertexCircle(path,neckL,[armLEnds,neckEnds,bodyLEnds])
#vertexCircle(path,neckR,[armREnds,neckEnds,bodyREnds])
#vertexCircle(path,gluT,[gluEnds,bodyLEnds,bodyREnds])
#vertexCircle(path,gluB,[gluEnds,legLEnds,legREnds])
#dwg.add(path)
#dwg.save()

## Backgrounds
dwg = svgwrite.Drawing('Backgrounds.svg',size=("384mm","384mm"),viewBox="0 0 384 384")
path = dwg.path(None,stroke=color,stroke_width=width,fill="none")
q1 = (10,10)
q1p = (182,10)
q1B = (96,268/3.+10)
q2 = (10,278)
q2p = (182,278)
q2B = (96,2*268/3.+10)
q1Ends = straightLineArrow(path,q1,q1B,forward=True,capped2=False)
q1pEnds = straightLineArrow(path,q1p,q1B,forward=False,capped2=False)
q2Ends = straightLineArrow(path,q2,q2B,forward=True,capped2=False)
q2pEnds = straightLineArrow(path,q2p,q2B,forward=False,capped2=False)
BEnds = wavyLine(path,q1B,q2B,capped1=False,capped2=False)
vertexCircle(path,q1B,[q1Ends,q1pEnds,BEnds])
vertexCircle(path,q2B,[q2Ends,q2pEnds,BEnds])
q1 = numpy.array(q1)+numpy.array([192,5])
q1p = numpy.array(q1p)+numpy.array([192,5])
q1B = numpy.array(q1B)+numpy.array([192,5])
q2 = numpy.array(q2)+numpy.array([192,5])
q2p = numpy.array(q2p)+numpy.array([192,5])
q2B = numpy.array(q2B)+numpy.array([192,5])
q1Ends = spiralLine(path,q1,q1B,capped2=False)
q1pEnds = straightLineArrow(path,q1p,q1B,forward=False,capped2=False)
q2Ends = straightLineArrow(path,q2,q2B,forward=True,capped2=False)
q2pEnds = spiralLine(path,q2p,q2B,capped2=False)
BEnds = straightLineArrow(path,q1B,q2B,forward=False,capped1=False,capped2=False)
vertexCircle(path,q1B,[q1Ends,q1pEnds,BEnds])
vertexCircle(path,q2B,[q2Ends,q2pEnds,BEnds])
gIn = numpy.array((30,373))
qIn = gIn + numpy.array((0,-80))
qV = qIn + numpy.array((100,0))
gV = gIn + numpy.array((100,0))
qOut = gV + numpy.array((100,0))
ffV = qV + numpy.array((100,0))
f1Out = ffV + numpy.array((60,60))
f2Out = ffV + numpy.array((60,-60))
gEnds = spiralLine(path,gIn,gV,capped1=True,capped2=False)
q1Ends = straightLineArrow(path,qIn,qV,forward=True,capped2=False)
vvEnds = straightLineArrow(path,qV,gV,forward=True,capped1=False,capped2=False)
qOutEnds = straightLineArrow(path,gV,qOut,forward=True,capped1=False,capped2=True)
BEnds = wavyLine(path,qV,ffV,capped1=False,capped2=False)
f1Ends = straightLineArrow(path,ffV,f1Out,forward=True,capped1=False,capped2=True)
f2Ends = straightLineArrow(path,ffV,f2Out,forward=False,capped1=False,capped2=True)
vertexCircle(path,qV,[q1Ends,vvEnds,BEnds])
vertexCircle(path,gV,[gEnds,vvEnds,qOutEnds])
vertexCircle(path,ffV,[BEnds,f1Ends,f2Ends])
dwg.add(path)
dwg.save()
