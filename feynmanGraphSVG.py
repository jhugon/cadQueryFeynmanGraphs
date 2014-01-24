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
q1pEnds = straightLineArrow(path,q1p,q1B,forward=True,capped2=False)
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

