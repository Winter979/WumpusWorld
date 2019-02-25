#! python3

# from minion import Minion
from gui import Gui 

import random
import time 

class World:

   pit_ratio = .15

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

      print(self.grid)

      random.seed()
   
   def start(self):
      self.gui.start(self)

   def trigger_event(self):
      pass

   def is_smelly(self):
      smelly = False

      if self.grid[self.minion_x +1][self.minion_y] == "pit":
         smelly = True

      return smelly

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

   def move_minion(self):
      self.gui.move_shape(self.minion, "right")

   def spawn_minion(self):

      self.minion_x = 0
      self.minion_y = 0

      self.minion = self.add_to_world(0,0, "minion")

   def spawn_gold(self):
      x,y = self.emptyCell()
      self.add_to_world(x,y,"gold")

   def spawn_wumpus(self):
      x,y = self.emptyCell()
      self.add_to_world(x,y,"wumpus")

   def spawn_pits(self):
      cell_count = self.width * self.height

      pit_count = int(cell_count * self.pit_ratio)

      for _ in range(pit_count):
         x,y = self.emptyCell()
         self.add_to_world(x,y,"pit")

   def add_to_world(self, x,y,item):
      shape = "circle"
      fill = "white"
      area = .5
      if item == "minion":
         fill = "blue"
         shape = "square"
         area = .5
         key = 1
      elif item == "gold":
         fill = "yellow"
         area = .7
         shape = "star"
         key = 2
      elif item == "wumpus":
         shape = "square"
         area = .6
         key = 3
      else : # elif item == "pit":
         fill = "grey"
         area = .8
         key = 4
         
      self.grid[x][y] = key
      return self.gui.draw_shape(x,y, shape=shape, fill=fill, area=area)
