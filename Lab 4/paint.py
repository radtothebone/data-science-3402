import math

class Canvas:
  def __init__(self, width, height):
    self.width=width
    self.height=height
    # Empty canvas is a matrix with element being the "space" character.
    self.data=[[' ']*width for i in range(height)]

  def set_pixel(self, row, col, char="*"):
    self.data[row][col]=char

  def get_pixel(self,row,col):
    return self.data[row][col]

  def clear_canvas(self):
    self.data=[[' ']*self.width for i in range(self.height)]

  def v_line(self, x, y, w, **kargs):
    for i in range(x,x+w):
      self.set_pixel(i, y, **kargs)

  def h_line(self, x, y, h, **kargs):
    for i in range(y,y+h):
      self.set_pixel(x, i, **kargs)

  def line(self, x1,y1,x2,y2, **kargs):
    slope=(y2-y1)/(x2-x1)
    for y in range(y1, y2):
      x=int(slope*y)
      self.set_pixel(x,y, **kargs)

  def display(self):
    print("\n".join(["".join(row) for row in self.data]))

class Shape:
  def calculate_area(self):
    raise NotImplementedError

  def calculate_perimeter(self):
    raise NotImplementedError

  def generate_coords(self):
    raise NotImplementedError

  def coord_check(self, x, y):
    raise NotImplementedError

  def overlaps(self, other):
    for x, y in self.generate_coords():
      if other.coord_check(x, y):
        return True
    for x, y in other.generate_coords():
      if self.coord_check(x, y):
        return True
    return False

  def paint(self, canvas, char="*"):
    for x, y in self.generate_coords():
      canvas.set_pixel(round(x), round(y), char=char)

class CompoundShape(Shape):
  def __init__(self, shapes):
    self.__shapes = shapes

  def get_shapes(self):
    return self.__shapes

  def calculate_area(self):
    return sum(shape.calculate_area() for shape in self.__shapes)

  def calculate_perimeter(self):
    return sum(shape.calculate_perimeter() for shape in self.__shapes)

  def generate_coords(self):
    points = []
    for shape in self.__shapes:
      points.extend(shape.generate_coords())
    return points

  def coord_check(self, x, y):
    return any(shape.coord_check(x, y) for shape in self.__shapes)

class Triangle(Shape):
  def __init__(self, leg_1, leg_2, x_coord, y_coord):
      self.__leg_1 = leg_1
      self.__leg_2 = leg_2
      self.__hyp = (leg_1 ** 2 + leg_2 ** 2) ** 0.5
      self.__x_coord = x_coord
      self.__y_coord = y_coord

  def calculate_area(self):
      return 0.5 * self.__leg_1 * self.__leg_2

  def calculate_perimeter(self):
      return self.__leg_1 + self.__leg_2 + self.__hyp

  def get_leg_1(self):
      return self.__leg_1

  def get_leg_2(self):
      return self.__leg_2

  def get_hyp(self):
      return self.__hyp

  def get_x(self):
      return self.__x_coord

  def get_y(self):
      return self.__y_coord

  def generate_coords(self):
      points = []
      for i in range(5):
          points.append((round(self.__x_coord + self.__leg_1 * i/5, 2), round(self.__y_coord, 2)))
      for i in range(5):
          points.append((round(self.__x_coord + self.__leg_1 * (1 - i/5), 2), round(self.__y_coord + self.__leg_2 * i/5, 2)))
      for i in range(5):
          points.append((round(self.__x_coord, 2), round(self.__y_coord + self.__leg_2 * (1 - i/5), 2)))
      return points

  def coord_check(self, x, y):
      in_bounding_box = self.__x_coord <= x <= self.__x_coord + self.__leg_1 and \
                        self.__y_coord <= y <= self.__y_coord + self.__leg_2
      below_hyp = (x - self.__x_coord) / self.__leg_1 + (y - self.__y_coord) / self.__leg_2 <= 1
      return in_bounding_box and below_hyp

  def __repr__(self):
      return f"Triangle({self.__leg_1}, {self.__leg_2}, {self.__x_coord}, {self.__y_coord})"


class Circle(Shape):
  def __init__(self, radius, x_coord, y_coord):
    self.__radius = radius
    self.__x_coord = x_coord
    self.__y_coord = y_coord

  def calculate_area(self):
    return 3.14159 * self.__radius ** 2

  def calculate_perimeter(self):
    return 2 * 3.14159 * self.__radius

  def get_radius(self):
    return self.__radius

  def get_x_coord(self):
    return self.__x_coord

  def get_y_coord(self):
    return self.__y_coord

  def generate_coords(self):
    theta_vals = [i * math.pi / 8 for i in range(16)]
    x_y_coords = [(round(self.__radius * math.cos(i) + self.__x_coord, 2),
                   round(self.__radius * math.sin(i) + self.__y_coord, 2)) for i in theta_vals]
    return x_y_coords

  def coord_check(self, x, y):
    return (x - self.__x_coord) ** 2 + (y - self.__y_coord) ** 2 <= self.__radius ** 2

  def __repr__(self):
    return f"Circle({self.__radius}, {self.__x_coord}, {self.__y_coord})"

class Rectangle(Shape):
  def __init__(self, length, width, x_coord, y_coord):
    self.__length = length
    self.__width = width
    self.__x_coord = x_coord
    self.__y_coord = y_coord

  def calculate_area(self):
    return self.__length * self.__width

  def calculate_perimeter(self):
    return 2 * self.__length + 2 * self.__width

  def get_length(self):
    return self.__length

  def get_width(self):
    return self.__width

  def get_x(self):
    return self.__x_coord

  def get_y(self):
    return self.__y_coord

  def generate_coords(self):
    points = []
    # bottom side (left to right)
    for i in range(4):
      points.append((round(self.__x_coord + self.__length * i / 4, 2), round(self.__y_coord, 2)))
    # right side (bottom to top)
    for i in range(4):
      points.append((round(self.__x_coord + self.__length, 2), round(self.__y_coord + self.__width * i / 4, 2)))
    # top side (right to left)
    for i in range(4):
      points.append((round(self.__x_coord + self.__length * (1 - i / 4), 2), round(self.__y_coord + self.__width, 2)))
    # left side (top to bottom)
    for i in range(4):
      points.append((round(self.__x_coord, 2), round(self.__y_coord + self.__width * (1 - i / 4), 2)))
    return points

  def coord_check(self, x, y):
    return self.__x_coord <= x <= self.__x_coord + self.__length and \
      self.__y_coord <= y <= self.__y_coord + self.__width

  def __repr__(self):
    return f"Rectangle({self.__length}, {self.__width}, {self.__x_coord}, {self.__y_coord})"

class RasterDrawing:
  def __init__(self, shapes=None):
    self.__shapes = shapes if shapes is not None else []

  def add_shape(self, shape):
    self.__shapes.append(shape)

  def remove_shape(self, shape):
    self.__shapes.remove(shape)

  def get_shapes(self):
    return self.__shapes

  def paint(self, canvas):
    for shape in self.__shapes:
      shape.paint(canvas)

  def __repr__(self):
    return "RasterDrawing([" + ", ".join(repr(shape) for shape in self.__shapes) + "])"

  def save(self, filename):
    f = open(filename, "w")
    f.write(repr(self))
    f.close()

def raster_drawing_loader(filename):
  f = open(filename, "r")
  tmp = eval(f.read())
  f.close()
  return tmp