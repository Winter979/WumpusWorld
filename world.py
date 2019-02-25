#! python3

# from minion import Minion
from gui import Gui 

import random

class World:

   PIT_RATIO = .2

   def __init__(self, gui):

      self.gui = gui

      self.width = gui.get_width()
      self.height = gui.get_height()

      # Create and initialize a 2d array (width*height)
      self.grid = [[0]*self.width for i in range(self.height)]

      self.spawn_minion()
      self.spawn_gold()
      self.spawn_pits()
      self.spawn_wumpus()
   
   def start(self):
      self.gui.start()

   def isEmpty(self, x, y):
      return self.grid[x][y] == 0

   def emptyCell(self):
      found = False
      while not found:
         x = random.randint(0, self.width-1)
         y = random.randint(0, self.height-1)
         if self.isEmpty(x,y):
            found = True

      return x,y

   def spawn_minion(self):
      x = 0
      y = 0

      self.minion = self.gui.draw(x,y) 
      self.grid[x][y] = 1

   def spawn_gold(self):
      pass

   def spawn_wumpus(self):

      x,y = self.emptyCell()

      self.wumpus = self.gui.draw(2,3, fill="red")
      self.grid[x][y] = 2

   def spawn_pits(self):
      cell_count = self.width * self.height

      pit_count = int(cell_count * self.PIT_RATIO)

      for _ in range(pit_count):
         x,y = self.emptyCell()
         self.gui.draw(x,y)
         self.grid[x][y] = 3

   def add_to_world(x,y,item):
      if item == "minion":
      
      elif item == "pit":

      elif item == "gold":

      elif item == "wumpus"

      else:
         # TODO better error handling here
         print("Error adding")
