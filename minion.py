#! python3

class Minion:
   def __init__(self, world):
      self.world = world
      self.x, self.y = world.get_minion_xy()
      self.max_x, self.max_y = world.get_max_xy()

      self.setup_grid()


      # The path that the minion has performed (reverse to head back
      # to the home)
      self.path = []

      self.path.append([self.x, self.y])

   def setup_grid(self):
      self.grid = [[Cell() for ii in range(self.max_x+1)] for jj in range(self.max_y+1)]

      for x in range(self.max_x+1):
         for y in range(self.max_y+1):
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

   def next_action(self):
      x = self.x
      y = self.y

      if self.grid[x][y].is_new():
         if self.world.is_safe(x,y):

            self.update_dangers()
            new_x, new_y = self.find_next()

            self.grid[x][y].travelled_to()

            self.world.move_minion(new_x, new_y)

            self.x = new_x
            self.y = new_y




   def update_dangers(self):

      x = self.x
      y = self.y

      breezy = self.world.is_breezy(x,y)
      smelly = self.world.is_smelly(x,y)
      shiny = self.world.is_shiny(x,y)

      cell = self.grid[x][y]

      if breezy:
         cell.add_danger(danger=cell.BREEZY)

      if smelly:
         cell.add_danger(danger=cell.SMELLY)
      
      if not breezy and not smelly:
         cell.remove_danger()

      if shiny:
         cell.set_status(cell.GOLD)

            
   def find_next(self):
      x = self.x
      y = self.y

      current = self.grid[x][y]

      adj = current.get_adjacent()

      ii = 0
      found = False

      new_x = x
      new_y = y

      dangers = []

      danger_up = self.determine_danger(adj[0])
      danger_down = self.determine_danger(adj[1])
      danger_left = self.determine_danger(adj[2])
      danger_right = self.determine_danger(adj[3])

      

      return new_x, new_y

   def determine_danger(self, cell):
      if cell == None:
         return -1

      if cell.is_new():
         danger = cell.get_danger()
      else:
         danger = 0

      return danger

class Cell:

   # Error codes to add dangers of the surroundings cells
   BREEZY = -1
   SMELLY = -2

   # Status of the the current cell
   UNKNOWN = 0
   SAFE = 1
   GOLD = 2
   PIT = 3
   WUMPUS = 4

   def __init__(self):
      
      self.new_cell = True
      self.status = self.UNKNOWN

      self.breezes = 0
      self.smells = 0

      self.cell_up = None
      self.cell_down = None
      self.cell_left = None
      self.cell_right = None

# ------------------------------------------------------------------------------

   def is_new(self):
      return self.new_cell

   def travelled_to(self):
      self.new_cell = False

# ------------------------------------------------------------------------------

   def set_up(self, cell):
      self.cell_up = cell

   def set_down(self, cell):
      self.cell_down = cell

   def set_left(self, cell):
      self.cell_left = cell

   def set_right(self, cell):
      self.cell_right = cell

   def set_status(self, status):
      self.status = status

# ------------------------------------------------------------------------------

   def get_danger(self):
      return self.breezes + self.smells

   def get_adjacent(self):
      return [self.cell_up, self.cell_down, self.cell_left, self.cell_right]

   def is_breezy(self):
      return self.breezes > 0

   def is_smelly(self):
      return self.smells > 0   

   def is_safe(self):
      return not self.is_smelly() and not self.is_breezy()

# ------------------------------------------------------------------------------

   def remove_danger(self):
      if self.cell_up != None:
         self.cell_up.set_status(Cell.SAFE)
         
      if self.cell_down != None:
         self.cell_down.set_status(Cell.SAFE)
         
      if self.cell_left != None:
         self.cell_left.set_status(Cell.SAFE)
         
      if self.cell_right != None:
         self.cell_right.set_status(Cell.SAFE)

   def add_danger(self, danger=None):

      if danger == Cell.BREEZY:
         danger_func = Cell.add_breeze
      elif danger == Cell.SMELLY:
         danger_func = Cell.add_smell
      else:
         raise ValueError("Unknown danger")

      if self.cell_up != None:
         danger_func(self.cell_up)
         
      if self.cell_down != None:
         danger_func(self.cell_down)
         
      if self.cell_left != None:
         danger_func(self.cell_left)
         
      if self.cell_right != None:
         danger_func(self.cell_right)
         
# ------------------------------------------------------------------------------

   def add_breeze(self):
      self.breezes += 1

   def add_smell(self):
      self.smells += 1

