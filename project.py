import libs 
import struct
import math
import os 
from libs import Bitmap
from libs import word

#Objet to draw 
img = None

#Constructor 
def glInit():
    return None

#Init FrameBuffer
def glCreateWindow(width, height):
    global img 
    img = Bitmap(width,height) 

#Delete actual image 
def glClear(): 
    img.clear()
#Image area can draw
def glViewPort(x,y,widht, height):
    img.viewPort(x,y,widht, height)

#Get Color 
def glColor(r,g,b):
    img.color(r,g,b)

#Init canvas with new color 
def glClearColor(r,g,b):
    img.clearColor(0,0,0) 

#Get new x,y points 
def glVertex(x,y):
    img.vertex(x,y)

#Show new image 
def glFinish():
    img.display("materials.bmp")

glCreateWindow(800,600)
glViewPort(0,0,799,599)
glClear()
img.load( 'chip.obj', 'chip.mtl', (0.5, 0.5, 0.5), (500, 500, 500)) 
glFinish()