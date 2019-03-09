import struct 

def color(r, g, b):
  return bytes([b, g, r])

def try_int(s, base=10, val=None):
  try:
    return int(s, base)
  except ValueError:
    return val
class Obj(object):
    def __init__(self, filename, fileMaterial=None):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        with open(fileMaterial) as g: 
            self.material = g.read().splitlines()
            
        self.vertices = []
        self.tvertices = []
        self.vfaces = []
        self.keyColor = []
        self.colors = []
        self.read()
        self.getColorToDraw = ''
        self.material = '' 

    def read(self):
        self.getMaterial()
        for line in self.lines:
            if line:
                try:
                    prefix, value = line.split(' ', 1)
                except:
                    prefix = ''
                if prefix == 'v':
                    self.vertices.append(list(map(float, value.split(' '))))
                if prefix == 'vt':
                    self.tvertices.append(list(map(float, value.split(' '))))                    
                elif prefix == 'f':
                    objToList = [list(map(try_int, face.split('/'))) for face in value.split(' ')]
                    objToList.append(self.getColorToDraw)
                    self.vfaces.append(objToList)
                elif prefix == 'usemtl': 
                    self.getColorToDraw = value

    def getMaterial(self):
        for line in self.material:
            if line:
                try: 
                    prefix, value = line.split( ' ', 1)
                except: 
                    prefix = ''
                if prefix == 'newmtl': 
                    self.keyColor.append(value)
                elif prefix == 'Kd':
                    self.colors.append(list(map(float, value.split( ' '))))
# agrega la textura 
class Texture(object):
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        image = open(self.path, "rb")
        image.seek(2 + 4 + 4)
        header_size = struct.unpack("=l", image.read(4))[0]
        image.seek(2 + 4 + 4 + 4 + 4)
        
        self.width = struct.unpack("=l", image.read(4))[0]
        self.height = struct.unpack("=l", image.read(4))[0]
        self.framebuffer = []
        image.seek(header_size)
        for y in range(self.height):
            self.framebuffer.append([])
            for x in range(self.width):
                b = ord(image.read(1))
                g = ord(image.read(1))
                r = ord(image.read(1))
                self.framebuffer[y].append(color(r,g,b))
        image.close()

    def get_color(self, tx, ty, intensity=1):
        x = int(tx * self.width)
        y = int(ty * self.height)
        try:
            return bytes(map(lambda b: round(b*intensity) if b*intensity > 0 else 0, self.framebuffer[y][x]))
        except:
            pass