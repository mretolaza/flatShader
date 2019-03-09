import numpy
from collections import namedtuple

vertex2 = namedtuple('Point2', ['x', 'y'])
vertex3 = namedtuple('Point3', ['x', 'y', 'z'])

def sum(v0, v1):
  return vertex3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
  return vertex3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def scalarMul(v0, k):
  return vertex3(v0.x * k, v0.y * k, v0.z *k)

def dotProduct(v0, v1):
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def crossProduct(v0, v1):
  return vertex3(
    v0.y * v1.z - v0.z * v1.y,
    v0.z * v1.x - v0.x * v1.z,
    v0.x * v1.y - v0.y * v1.x,
  )

def length(v0):
  return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def normProduct(v0):
  v0length = length(v0)

  if not v0length:
    return vertex3(0, 0, 0)

  return vertex3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

#Ingreso de A , B , C en formato de vertices 
def boundingBox(*vertices):
  xCoords = [ v.x for v in vertices ]
  yCoords = [ v.y for v in vertices ]
  xCoords.sort()
  yCoords.sort()

  return vertex2(xCoords[0], yCoords[0]), vertex2(xCoords[-1], yCoords[-1])

# vertex = v 
# translate = t 
# scale = s 
def transform(v, t=(0,0,0), s=(1,1,1)):
# retorna el vertex 3 trasladado y transformado 
  partA = round((v[0] + t[0]) * s[0])
  partB = round((v[1] + t[1]) * s[1])
  partC = round((v[2] + t[2]) * s[2])
  
  return vertex3(partA, partB , partC)

def barycentric(A, B, C, P): 
  bary = crossProduct(
    vertex3(C.x - A.x, B.x - A.x, A.x - P.x), 
    vertex3(C.y - A.y, B.y - A.y, A.y - P.y)
  )

  if abs(bary[2]) < 1:
    return -1, -1, -1
  
  return (
    1 - (bary[0] + bary[1]) / bary[2], 
    bary[1] / bary[2], 
    bary[0] / bary[2]
  )
