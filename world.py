#! python3

from minion import Minion
from gui import Gui 

import random
import time 

class World:

   PIT_RATIO = .15

   KEY_EMPTY = 0
   KEY_MINION = 1
   KEY_GOLD = 2
   KEY_WUMPUS = 3
   KEY_PIT = 4

   def __init__(self, gui):

      self.gui = gui

      self.width = gui.get_width()
      self.max_x = self.width -1

      self.height = gui.get_height()
      self.max_y = self.height -1
 
      # Create and initialize a 2d array (width*height)
      self.grid = [[self.KEY_EMPTY]*self.width for i in range(self.height)]

      random.seed()

      self.spawn_minion()
      self.spawn_gold()
      self.spawn_pits()
      self.spawn_wumpus()

# ------------------------------------------------------------------------------

   def start(self):
      self.gui.start(self.trigger_event)


   def trigger_event(self):
      self.minion.next_action()
      pass

# ------------------------------------------------------------------------------

   def is_breezy(self, x, y):
      """Checks all adjecent squares to see if any of them contain a pit"""
      breezy = False

      if x < self.max_x:
         if self.grid[x +1][y] == self.KEY_PIT:
            breezy = True
   
      if y < self.max_y:
         if self.grid[x][y +1] == self.KEY_PIT:
            breezy = True

      if x != 0:
         if self.grid[x -1][y] == self.KEY_PIT:
            breezy = True
   
      if y != 0:
         if self.grid[x][y -1] == self.KEY_PIT:
            breezy = True

      return breezy

   def is_smelly(self, x, y):
      """Checks all adjecent squares to see if any of them contain the wumpus"""
      smelly = False

      if x < self.max_x:
         if self.grid[x +1][y] == self.KEY_WUMPUS:
            smelly = True
   
      if y < self.max_y:
         if self.grid[x][y +1] == self.KEY_WUMPUS:
            smelly = True

      if x != 0:
         if self.grid[x -1][y] == self.KEY_WUMPUS:
            smelly = True
   
      if y != 0:
         if self.grid[x][y -1] == self.KEY_WUMPUS:
            smelly = True

      return smelly

   def is_shiny(self,x,y):
      return self.grid[x][y] == self.KEY_GOLD

# ------------------------------------------------------------------------------

   def get_minion_xy(self):
      return self.minion_x, self.minion_y

   def get_max_xy(self):
      return self.max_x, self.max_y

   def isEmpty(self, x, y):
      return self.grid[x][y] == 0

   def findEmptyCell(self):
      found = False
      while not found:
         x = random.randint(0, self.width-1)
         y = random.randint(0, self.height-1)
         if self.isEmpty(x,y):
            found = True

      return x,y

   def move_minion(self):
      self.gui.move_shape(self.minion, "right")

# ------------------------------------------------------------------------------

   def spawn_minion(self):

      self.minion_x = 0
      self.minion_y = 0

      self.minion_gui = self.add_to_world(0,0, "minion")

      self.minion = Minion(self)

   def spawn_gold(self):
      x,y = self.findEmptyCell()
      self.add_to_world(x,y,"gold")

   def spawn_wumpus(self):
      x,y = self.findEmptyCell()
      self.add_to_world(x,y,"wumpus")

   def spawn_pits(self):
      cell_count = self.width * self.height

      pit_count = int(cell_count * self.PIT_RATIO)

      for _ in range(pit_count):
         x,y = self.findEmptyCell()
         self.add_to_world(x,y,"pit")

   def add_to_world(self, x,y,item):
      shape = "circle"
      fill = "white"
      area = .5
      if item == "minion":
         fill = "blue"
         shape = "square"
         area = .5
         key = self.KEY_MINION
      elif item == "gold":
         fill = "yellow"
         area = .7
         shape = "star"
         key = self.KEY_GOLD
      elif item == "wumpus":
         shape = "square"
         area = .6
         key = self.KEY_WUMPUS
      else : # elif item == "pit":
         fill = "grey"
         area = .8
         key = self.KEY_PIT
         
      self.grid[x][y] = key
      return self.gui.draw_shape(x,y, shape=shape, fill=fill, area=area)
