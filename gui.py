#! python3

from tkinter import Tk, Canvas

class Gui:
   def __init__(self, width=500, height=500, cells_x=4, cells_y=4):
      self.width = width
      self.height = height
      self.cells_x = cells_x
      self.cells_y = cells_y

      self.cell_height = height // cells_x
      self.cell_width = width // cells_y

      self.window = Tk()
      self.canvas = Canvas(self.window, bg='white', width=width, height=height)

      self.draw_grid()

      self.canvas.pack()

   def draw_grid(self):
      # Creates all vertical lines at intevals of cell width
      for i in range(0, self.width, self.cell_width):
         self.canvas.create_line([(i, 0), (i, self.width)])

      # Creates all horizontal lines at intevals of cell height
      for i in range(0, self.width, self.cell_height):
         self.canvas.create_line([(0, i), (self.width, i)])

# ------------------------------------------------------------------------------

   def start(self, callback):
      self.loop(callback)
      self.window.mainloop()

   def loop(self, callback):
      callback()
      self.window.after(1000, self.loop, callback)
      
# ------------------------------------------------------------------------------

   def get_width(self):
      return self.cells_x

   def get_height(self):
      return self.cells_y

# ------------------------------------------------------------------------------

   def draw_shape(self, x, y, outline="black", fill="white", area=.5, shape="circle"):

      spawn_x = x * self.cell_width + self.cell_width // 2
      spawn_y = self.height - y * self.cell_height - self.cell_height//2

      coords = [spawn_x - (self.cell_width * area) // 2, 
                spawn_y - (self.cell_width * area) // 2,
                spawn_x + (self.cell_width * area) // 2, 
                spawn_y + (self.cell_width * area) // 2]

      if shape == "square":
         new_shape = self.canvas.create_rectangle(coords, outline=outline, fill=fill)
      elif shape == "circle":
         new_shape = self.canvas.create_oval(coords, outline=outline, fill=fill)
      elif shape == "star":

         star_dip = 7

         points = [spawn_x, spawn_y - self.cell_height * area // 2,
                   spawn_x + self.cell_height * area // star_dip, spawn_y - self.cell_width * area // star_dip, 
                   spawn_x + self.cell_width * area // 2, spawn_y ,
                   spawn_x + self.cell_height * area // star_dip, spawn_y + self.cell_width * area // star_dip, 
                   spawn_x, spawn_y + self.cell_height * area // 2,
                   spawn_x - self.cell_height * area // star_dip, spawn_y + self.cell_width * area // star_dip, 
                   spawn_x - self.cell_width * area // 2, spawn_y,
                   spawn_x - self.cell_height * area // star_dip, spawn_y - self.cell_width * area // star_dip]

         new_shape = self.canvas.create_polygon(points, outline=outline, fill=fill)
      else:
         new_shape = self.canvas.create_oval(coords, outline=outline, fill=fill)
      
      return new_shape

   def move_shape(self, shape, direction):

      x_vel = 0
      y_vel = 0

      if direction == "left":
         x_vel = -1
      elif direction == "right":
         x_vel = 1
      elif direction == "up":
         y_vel = -1
      elif direction == "down":
         y_vel = 1
      else:
         raise ValueError("unknown direction")

      self.canvas.move(shape, x_vel * self.cell_width, y_vel * self.cell_height)
      
   def jump_shape(self, shape, x_vel, y_vel):
      self.canvas.move(shape, x_vel * self.cell_width, y_vel * self.cell_height)
