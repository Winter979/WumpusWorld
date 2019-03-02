#! python3

from cell import WorldCell
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
 
      self.setup_grid()

      random.seed()

      self.spawn_minion()
      self.spawn_pits()
      self.spawn_gold()
      self.spawn_wumpus()

   def setup_grid(self):
      self.grid = [[WorldCell() for ii in range(self.height)] for jj in range(self.width)]

      for x in range(self.width):
         for y in range(self.height):
            cell = self.grid[x][y]

            if y < self.max_y:
               cell.set_up(self.grid[x][y+1])
            if y > 0:
               cell.set_down(self.grid[x][y-1])
            if x > 0:
               cell.set_left(self.grid[x-1][y])
            if x < self.max_x:
               cell.set_right(self.grid[x+1][y])

# ------------------------------------------------------------------------------

   def start(self):
      self.gui.move_to_front(self.minion_gui)
      self.gui.start(self.trigger_event)


   def trigger_event(self):
      self.minion.next_action()
      pass

# ------------------------------------------------------------------------------

   def is_safe(self, x, y):
      return not self.grid[x][y].is_wumpus() and not self.grid[x][y].is_pit()

   def is_breezy(self, x, y):
      return self.grid[x][y].is_breezy()

   def is_smelly(self, x, y):
      return self.grid[x][y].is_smelly()

   def is_shiny(self,x,y):
      return self.grid[x][y].is_shiny()

# ------------------------------------------------------------------------------

   def get_minion_xy(self):
      return self.minion_x, self.minion_y

   def get_max_xy(self):
      return self.max_x, self.max_y

   def isEmpty(self, x, y):
      return self.grid[x][y].is_empty()

   def findEmptyCell(self):
      found = False
      while not found:
         x = random.randint(0, self.max_x)
         y = random.randint(0, self.max_y)
         if self.isEmpty(x,y):
            found = True

      return x,y

   def move_minion(self, x, y):

      direction = None

      if self.minion_y - y == -1:
         direction = "up"
      elif self.minion_y - y == +1:
         direction = "down"
      elif self.minion_x - x == +1:
         direction = "left"
      elif self.minion_x - x == -1:
         direction = "right"
      
      if direction != None:
         self.gui.move_shape(self.minion_gui, direction)

         self.minion_x = x
         self.minion_y = y
      else:
         print("no where to move")

   def jump_minion(self, x, y):
      self.gui.jump_shape(self.minion_gui, x - self.minion_x , self.minion_y -y )
      self.minion_x = x
      self.minion_y = y

   def shoot_wumpus(self, x, y):
      cell = self.grid[x][y]

      dead = False

      if cell.is_wumpus():
         dead = True
         cell.status = cell.EMPTY
         self.gui.remove_item(self.wumpus_gui)

      
      return dead

# ------------------------------------------------------------------------------

   def spawn_minion(self):

      self.minion_x = 0
      self.minion_y = 0

      self.minion = Minion(self)
      self.minion_gui = self.add_to_world(0,0, "minion")

   def spawn_gold(self):
      x,y = self.findEmptyCell()
      self.add_to_world(x,y,"gold")

   def spawn_wumpus(self):
      x,y = self.findEmptyCell()
      self.wumpus_gui = self.add_to_world(x,y,"wumpus")

   def spawn_pits(self):
      cell_count = self.width * self.height

      pit_count = int(cell_count * self.PIT_RATIO)

      for _ in range(pit_count):
         x,y = self.findEmptyCell()
         self.add_to_world(x,y,"pit")

   def add_to_world(self, x,y,item):

      cell = self.grid[x][y]

      shape = "circle"
      fill = "white"
      area = .5
      if item == "minion":
         fill = "blue"
         shape = "square"
         area = .5
         cell.status = cell.MINION
      elif item == "gold":
         fill = "yellow"
         area = .7
         shape = "star"
         cell.status = cell.GOLD
      elif item == "wumpus":
         shape = "square"
         area = .6
         cell.status = cell.WUMPUS
      else : # elif item == "pit":
         fill = "grey"
         area = .8
         cell.status = cell.PIT

      return self.gui.draw_shape(x,y, shape=shape, fill=fill, area=area)
