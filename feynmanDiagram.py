
#
# Important MetaData
#
UOM = "mm"

def sqrt(x):
    return x**(0.5)
def distance2d(p1,p2):
    return sqrt((p1[1]-p2[1])**2+(p1[0]-p2[0])**2)
def getVector2d(p1,p2):
    return (p2[0]-p1[0],p2[1],p1[1])
def getnormVector2d(p1,p2):
    dist = distance2d(p1,p2)
    vec = getVector2d(p1,p2)
    return (vec[0]/dist,vec[1]/dist)
def scaleVector2d(p,sf):
    return (p[0]*sf,p[1]*sf)
def addVectors2d(p1,p2):
    return (p1[0]+p2[0],p1[1]+p2[1])

def makeWiggle(wp,endPoint,wigglePeriod=1.0,amplitude=0.25,width=0.25):
    firstLine = []
    secondLine = []
    currentPoint = (0,0)
    nPoints = int(distance2d(currentPoint,endPoint)/wigglePeriod)*4
    normVector = getnormVector2d(currentPoint,endPoint)
    perpVector = (-normVector[1],normVector[0])
    advanceVector = scaleVector2d(normVector,wigglePeriod/4.)
    ampVector = scaleVector2d(perpVector,amplitude)
    currentPoint = addVectors2d(currentPoint,scaleVector2d(perpVector,width/2.))
    wp = wp.lineTo(currentPoint[0],currentPoint[1])
    for i in range(nPoints/4):
        currentPoint = addVectors2d(addVectors2d(currentPoint,advanceVector),ampVector)
        firstLine.append(currentPoint)
        currentPoint = addVectors2d(addVectors2d(currentPoint,advanceVector),(-ampVector[0],-ampVector[1]))
        firstLine.append(currentPoint)
        currentPoint = addVectors2d(addVectors2d(currentPoint,advanceVector),(-ampVector[0],-ampVector[1]))
        firstLine.append(currentPoint)
        currentPoint = addVectors2d(addVectors2d(currentPoint,advanceVector),ampVector)
        firstLine.append(currentPoint)
    wp = wp.spline(firstLine)
    currentPoint = addVectors2d(currentPoint,scaleVector2d(perpVector,-width))
    wp = wp.lineTo(currentPoint[0],currentPoint[1])
    advanceVector = scaleVector2d(advanceVector,-1)
    ampVector = scaleVector2d(ampVector,-1)
    for i in range(nPoints/4):
        currentPoint = addVectors2d(addVectors2d(currentPoint,advanceVector),ampVector)
        secondLine.append(currentPoint)
        currentPoint = addVectors2d(addVectors2d(currentPoint,advanceVector),(-ampVector[0],-ampVector[1]))
        secondLine.append(currentPoint)
        currentPoint = addVectors2d(addVectors2d(currentPoint,advanceVector),(-ampVector[0],-ampVector[1]))
        secondLine.append(currentPoint)
        currentPoint = addVectors2d(addVectors2d(currentPoint,advanceVector),ampVector)
        secondLine.append(currentPoint)
    wp = wp.spline(secondLine)
    currentPoint = scaleVector2d(perpVector,-width/2.)
    wp = wp.lineTo(currentPoint[0],currentPoint[1])
    wp = wp.close()
    return wp
    
def makeLine(wp,endPoint,arrow=False,forward=True,width=0.25):
    normVector = getnormVector2d((0.0,0.0),endPoint)
    perpVector = (-normVector[1],normVector[0])
    listOfPoints = []
    listOfPoints.append(scaleVector2d(perpVector,-width/2.))
    listOfPoints.append(scaleVector2d(perpVector,width/2.))
    listOfPoints.append(addVectors2d(endPoint,scaleVector2d(perpVector,width/2.)))
    listOfPoints.append(addVectors2d(endPoint,scaleVector2d(perpVector,-width/2.)))
    listOfPoints.append(scaleVector2d(perpVector,-width))

    return wp.polyline(listOfPoints)
#
# PARAMETERS and PRESETS
# These parameters can be manipulated by end users
#
propagatorLength = FloatParam(min=1.0,max=100.0,presets={'default':5.0},group="Size", desc="Length of the propagator line")
externalLength = FloatParam(min=1.0,max=100.0,presets={'default':5.0},group="Size", desc="Length of the external legs")
bosonWidth = FloatParam(min=0.5,max=10.0,presets={'default':2.0},group="Size", desc="Width of the Boson lines")
fermionWidth = FloatParam(min=0.5,max=10.0,presets={'default':2.0},group="Size", desc="Width of the Fermion lines")
arrowWidth = FloatParam(min=0.5,max=20.0,presets={'default':4.0},group="Size", desc="Width of the arrows on Fermion lines")
arrowLength = FloatParam(min=1.0,max=20.0,presets={'default':10.0},group="Size", desc="Length of the arrows on Fermion lines")
thickness = FloatParam(min=0.5,max=20.0,presets={'default':3.0},group="Size", desc="Thickness of the feynman diagram model")
vertexDiameter = FloatParam(min=1.0,max=20.0,presets={'default':3.0},group="Size", desc="Diameter of the vertex circles")

#
# Other Variables.
# These are used in the script but not exposed to users to change with the GUI

#
# Your build method. It must return a solid object
#
def build():
    depth = 0.5
    world = Workplane(Plane.XY())
    world = makeWiggle(world,(0,6)).extrude(depth).faces(">Z").workplane(offset=-depth)
    world = world.rect(2,2).extrude(depth).faces(">Z").workplane(offset=-depth)
    world = makeWiggle(world,(6,0)).extrude(depth).faces(">Z").workplane(offset=-depth)
    result = makeLine(world,(-4.2,-4.2)).extrude(depth)
    return result
