#! python3

class Minion:

   # definate state of a cell
   CELL_NEW = 0
   CELL_SAFE = -1
   CELL_BEEN_TO = -1

   # possibility of dange
   CELL_CHANCE_PIT = 1
   CELL_CHANCE_WUMPUS = 10

   # definite danger (requires upto 4 posibilities to be sure)
   CELL_PIT = 4
   CELL_WUMPUS = 40

   # signs that appeared
   CELL_BREEZY = 1
   CELL_SMELLY = 2

   def __init__(self, world):
      self.world = world
      self.x, self.y = world.get_minion_xy()
      self.max_x, self.max_y = world.get_max_xy()

      self.grid = [[self.CELL_NEW] * world.width for i in range(world.height)] 

      self.grid[self.x][self.y] = self.CELL_BEEN_TO

      # The path that the minion has performed (reverse to head back
      # to the home)
      self.path = []

      self.path.append([self.x, self.y])

   def next_action(self):
      x = self.x
      y = self.y

      # Only check the surrounding
      if self.grid[x][y] == self.CELL_NEW:
         breezy = self.world.is_breezy(x,y)
         smelly = self.world.is_smelly(x,y)
         shiny = self.world.is_shiny(x,y)

         # update surrounding dangers if present
         if breezy:
            self.add_world_danger(x,y, self.CELL_CHANCE_PIT)

         if smelly:
            self.add_world_danger(x,y, self.CELL_CHANCE_WUMPUS)

   def add_world_danger(self, x, y, danger_level):
      self.add_cell_danger(x+1,y, danger_level)
      self.add_cell_danger(x,y+1, danger_level)
      self.add_cell_danger(x-1,y, danger_level)
      self.add_cell_danger(x,y-1, danger_level)

   def add_cell_danger(self, x, y, danger_level):
      if 0 <= x <= self.max_x and 0 <= y <= self.max_y:
         danger = self.grid[x][y]

         if danger != self.CELL_WUMPUS and danger != self.CELL_PIT:
            self.grid[x][y] += danger_level




      