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
    slop=(y2-y1)/(x2-x1)
    for y in range(y1, y2):
      x=int(slop*y)
      self.set_pixel(x,y, **kargs)

  def display(self):
    print("\n".join(["".join(row) for row in self.data]))
