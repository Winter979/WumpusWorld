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

   def start(self):
      self.window.mainloop()

   def get_width(self):
      return self.cells_x

   def get_height(self):
      return self.cells_y

   def draw_grid(self):
      # Creates all vertical lines at intevals of cell width
      for i in range(0, self.width, self.cell_width):
         self.canvas.create_line([(i, 0), (i, self.width)])

      # Creates all horizontal lines at intevals of cell height
      for i in range(0, self.width, self.cell_height):
         self.canvas.create_line([(0, i), (self.width, i)])

   def draw(self, x, y, outline="black", fill="white", area=.5):

      spawn_x = x * self.cell_width + self.cell_width // 2
      spawn_y = self.height - y * self.cell_height - self.cell_height//2

      coords = [spawn_x - (self.cell_width * area) // 2, 
                spawn_y - (self.cell_width * area) // 2,
                spawn_x + (self.cell_width * area) // 2, 
                spawn_y + (self.cell_width * area) // 2]

      self.canvas.create_oval(coords, outline=outline, fill=fill)
 