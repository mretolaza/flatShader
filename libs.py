import struct
import math
from obj import Obj
from utils import * 
from constants import * 

def color(r, g, b):
    return bytes([b, g, r])

class Bitmap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.framebuffer = []
        self.zbuffer = []
        self.newGlColor = color(255, 255, 255)
        self.clear()
       

    #structure image file 
    def writeFile(self, filename):
        f = open(filename, "wb")
        # estandar
        f.write(char('B'))
        f.write(char('M'))
        # file size
        f.write(dword(14 + 40 + self.width * self.height * 3))
        # reserved
        f.write(dword(0))
        # data offset
        f.write(dword(54))
        # header size
        f.write(dword(40))
        # width
        f.write(dword(self.width))
        # height
        f.write(dword(self.height))
        # planes
        f.write(word(1))
        # bits per pixel
        f.write(word(24))
        # compression
        f.write(dword(0))
        # image size
        f.write(dword(self.width * self.height * 3))
        # x pixels per meter
        f.write(dword(0))
        # y pixels per meter
        f.write(dword(0))
        # number of colors
        f.write(dword(0))
        # important colors
        f.write(dword(0))
        # image data
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])
        # close file
        f.close()
    
    def display(self, filename="img.bmp"): 
        self.writeFile(filename)

        try:
            from wand.image import Image 
            from wand.display import display 

            with Image(filename=filename) as image: 
                display(image)

        except ImportError: 
            pass
    
    #clear the canvas with a new color 
    def clearColor(self, r, g, b): 
        newR = math.floor(r*255)
        newG = math.floor(g*255)
        newB = math.floor(b*255)

        self.framebuffer = [
            [color(newR, newG, newB) for x in range(self.width)]
            for y in range(self.height)
        ]
    
    # Clear image 
    def clear(self):
        self.framebuffer = [
            [
                #show background color 
                self.color(0,0,0) for x in range(self.width)
            ]
            for y in range(self.height)
        ]
        self.zbuffer = [ 
            [ -float('inf') for x in range (self.width)]
            for y in range(self.height)
        ]
        
    # get dimension image (begin of glViewPort)
    def viewPort(self, x, y, width, height):
        self.viewPortWidth = width
        self.viewPortHeight = height
        self.xViewPort = x
        self.yViewPort = y
    
    def getRXCoord(self, x):
        dx = x * (self.viewPortWidth / 2)
        realXVP = (self.viewPortWidth / 2) + dx
        realX = realXVP + self.xViewPort
        return realX

    def getRYCoord(self, y):
        dy = y * (self.viewPortHeight / 2)
        realYVP = (self.viewPortHeight / 2) + dy
        realY = realYVP + self.yViewPort
        return realY

    def getNormXCoord(self, realX):
        realXVP = realX - self.xViewPort
        dx = realXVP - (self.viewPortWidth / 2)
        x = dx / (self.viewPortWidth / 2)
        return x

    def getNormYCoord(self, realY):
        realYVP = realY - self.yViewPort
        dy = realYVP - (self.viewPortHeight / 2)
        y = dy / (self.viewPortHeight / 2)
        return y

    # create new canvas to draw image 
    def vertex(self, x, y):
        if ((x >= -1 and x <= 1) and (y >= -1 and y <= 1)):
            # x           
            dx = x * (self.viewPortWidth / 2)
            realXVP = (self.viewPortWidth / 2) + dx

            # y
            dy = y * (self.viewPortHeight / 2)
            realYVP = (self.viewPortHeight / 2) + dy

            # Add new viewports 
            realX = realXVP + self.xViewPort
            realY = realYVP + self.yViewPort       

            # draw inside dimensions 
            if ((realX <= self.width) and (realY <= self.height)):
                if (realX == self.width):
                    realX = self.width - 1
                if (realY == self.height): 
                    realY = self.height - 1
                self.framebuffer[math.floor(realY)][math.floor(realX)] = self.newGlColor

    def color(self, r, g, b):
        newR = math.floor(r*255)
        newG = math.floor(g*255)
        newB = math.floor(b*255)

        self.newGlColor = color(newR, newG, newB)
        return self.newGlColor

    def point(self, x, y, color= None):
        try: 
            self.framebuffer[int(y)][int(x)] = color or self.newGlColor
        except: 
            pass 

    def line (self, x1, y1, x2, y2, color = None): 
        x1 = math.floor(self.getRXCoord(x1))
        x2 = math.floor(self.getRXCoord(x2))
        y1 = math.floor(self.getRYCoord(y1))
        y2 = math.floor(self.getRYCoord(y2))

        dy = abs(y2 - y1) 
        dx = abs(x2 - x1) 

        steep = dy > dx 

        if steep: 
            x1, y1 = y1 , x1 
            x2, y2  = y2, x2 

        if  x1 > x2: 
            x1,x2 = x2, x1 
            y1, y2 = y2, y1

        dy = abs(y2 - y1)  
        dx = abs(x2 - x1)  

        offset = 0 
        threshold = dx

        y = y1 

        for x in range (x1,x2 +1): 
            if steep:    
                self.point(y, x, color)
            else: 
                self.point(x, y, color)

            offset += dy * 2
            if offset >= threshold: 
                y += 1 if y1 < y2 else -1 
                threshold += dx * 2

    def triangleF(self, A, B, C, color=None): #Primer algoritmo enseñado para pintar los triangulos 
        if A.y > B.y:
            A, B = B , A 
        if A.y > C.y: 
            A, C = C, A
        if B.y > C.y: 
            B , C = C, B 
        
        dxAc = C.x - A.x 
        dyAc = C.y - A.y 
        if dyAc == 0: 
            return 
        miAc = dxAc/dyAc

        dxAb  = B.x - A.x 
        dyAb = B.y - A.y 

        if dyAb != 0: 
            miAb = dxAb/dyAb
        
            for y in range(A.y, B.y + 1):
                xi = round(A.x - miAc * (A.y -y))
                xf = round(A.x - miAb * (A.y - y))

                if xi > xf: 
                    xi, xf = xf, xi 
                for x in range(xi, xf + 1): 
                    self.point(x,y, color) 
        
        dxBc = C.x - B.x 
        dyBc = C.y - B.y 
        if dyBc: 
            miBc = dxBc/dyBc

            for y in range(B.y, C.y + 1): 
                xi = round(A.x - miAc * (A.y - y))
                xf = round(B.x - miBc * (B.y - y))

                if xi > xf: 
                    xi, xf = xf, xi 

                    for x in range(xi, xf + 1): 
                        self.point(x,y, color)

    #aplicando coordenadas baricentrícas 
    def triangleB(self, A, B, C, color=None,  texture=None, textureCoords=(), intensity=1):
        bboxMin, bboxMax = boundingBox(A, B, C)

        for x in range(bboxMin.x , bboxMax.x +1): 
            for y in range(bboxMin.y, bboxMax.y +1): 
                w,v,u = barycentric(A,B,C,vertex2(x,y))
                if w < 0 or v < 0 or u < 0: 
                    continue

                if texture: 
                    tA, tB, tC = textureCoords 
                    tx = tA.x * w + tB.x * v + tC.x * u
                    ty = tA.y * w + tB.y * v + tC.y * u

                    color = texture.get_color(tx, ty, intensity)
               
                z = A.z * w  + B.z * v + C.z * u 

                if x < 0 or y < 0: 
                    continue

                if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[x][y]:
                    self.point(x, y, color)
                    self.zbuffer[x][y] = z
        
    def load(self, filename, fileMaterials=None, translate=(0, 0, 0), scale=(1, 1, 1), texture=None): 
        model= Obj(filename, fileMaterials)
        light= vertex3(0,0,1)

        for face in model.vfaces: 
            vcount = len(face)

            if vcount == 4: 
                f1= face[0][0] - 1
                f2= face[1][0] - 1 
                f3= face[2][0] - 1 

                a= transform(model.vertices[f1], translate, scale)
                b= transform(model.vertices[f2], translate, scale)
                c= transform(model.vertices[f3], translate, scale)

                normal = normProduct(crossProduct(sub(b,a), sub(c,a)))
                intensity = dotProduct(normal, light)

                if fileMaterials: 
                    materialName = face[3]
                    indx = model.keyColor.index(materialName)
                    getKeyCl = model.colors[indx]
                    col1, col2, col3 = getKeyCl
                    if intensity < 0: 
                        continue
                    colorA = round(col1*255*intensity)
                    colorB =  round(col2*255*intensity)
                    colorC =  round(col3*255*intensity)
                    self.triangleB(a,b,c, color(colorA,colorB, colorC))
                    
                if not texture: 
                    grey = round(255 * intensity)
                    if grey < 0: 
                        continue
                    self.triangleB(a,b,c, color=color(grey,grey,grey))
                else: 
                    t1 = face[0][1] - 1 
                    t2 = face[1][1] - 1 
                    t3 = face[2][1] - 1
                    tA = vertex3(*model.tvertices[t1])
                    tB = vertex3(*model.tvertices[t2])
                    tC = vertex3(*model.tvertices[t3])

                    self.triangleB(a,b,c, texture=texture, textureCoords=(tA, tB, tC), intensity=intensity) 
            else: 
                f1 = face[0][0] - 1 
                f2 = face[1][0] - 1 
                f3 = face[2][0] - 1 
                f4 = face[3][0] - 1 

                vertices = [
                    transform(model.vertices[f1],  translate, scale), 
                    transform(model.vertices[f2],  translate, scale),
                    transform(model.vertices[f3],  translate, scale),
                    transform(model.vertices[f4],  translate, scale)
                ]  

                normal = normProduct(crossProduct(sub(vertices[0], vertices[1]), sub(vertices[1], vertices[2])))
                intensity = dotProduct(normal, light)
                grey = round(255 * intensity)

                A, B, C, D = vertices

                if not texture: 
                    grey = round(255 *intensity)
                    if grey < 0: 
                        continue
                    self.triangleB(A, B, C, color(grey,grey,grey))
                    self.triangleB(A, C, D, color(grey,grey,grey))

                else: 
                    t1 = face[0][1] - 1 
                    t2 = face[1][1] - 1
                    t3 = face[2][1] - 1
                    t4 = face[3][1] - 1 
                    tA = vertex3(*model.tvertices[t1])
                    tB = vertex3(*model.tvertices[t2])
                    tC = vertex3(*model.tvertices[t3])
                    tD = vertex3(*model.tvertices[t4])
                    
                    self.triangleB(A, B, C, texture=texture, textureCoords=(tA, tB, tC), intensity=intensity)
                    self.triangleB(A, C, D, texture=texture,  textureCoords=(tA, tC, tD), intensity=intensity)