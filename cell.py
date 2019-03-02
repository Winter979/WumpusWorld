#! python3

class MinionCell:

   # Error codes to add dangers of the surroundings cells
   BREEZY = -1
   SMELLY = -2

   # Status of the the current cell
   UNKNOWN = 0
   SAFE = 1

   def __init__(self, x, y):
      
      self.x = x
      self.y = y

      self.discovered = False
      self.been_to = False
      self.status = self.UNKNOWN

      self.breezes = 0
      self.smells = 0

      self.cell_up = None
      self.cell_down = None
      self.cell_left = None
      self.cell_right = None

   def __lt__(self, other):
      return self.get_danger() < other.get_danger()

# ------------------------------------------------------------------------------

   # def discovered(self):
   #    return self.new_cell

   def travelled_to(self):
      self.been_to = True

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
      if self.status == MinionCell.SAFE:
         return 0
      else:
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
         self.cell_up.set_status(MinionCell.SAFE)
         
      if self.cell_down != None:
         self.cell_down.set_status(MinionCell.SAFE)
         
      if self.cell_left != None:
         self.cell_left.set_status(MinionCell.SAFE)
         
      if self.cell_right != None:
         self.cell_right.set_status(MinionCell.SAFE)

   def add_danger(self, danger=None):

      if danger == MinionCell.BREEZY:
         danger_func = MinionCell.add_breeze
      elif danger == MinionCell.SMELLY:
         danger_func = MinionCell.add_smell
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

# ==============================================================================
# ==============================================================================

class WorldCell:

   EMPTY = 0
   MINION = 1
   GOLD = 2
   PIT = 3
   WUMPUS = 4

   def __init__(self):

      self.status = self.EMPTY
      self.cell_up = None
      self.cell_down = None
      self.cell_left = None
      self.cell_right = None

# ------------------------------------------------------------------------------

   def set_up(self, cell):
      self.cell_up = cell

   def set_down(self, cell):
      self.cell_down = cell

   def set_left(self, cell):
      self.cell_left = cell

   def set_right(self, cell):
      self.cell_right = cell

# ------------------------------------------------------------------------------

   def is_unknown(self):
      return self.status ==WorldCell.EMPTY

   def is_empty(self):
      return self.status == WorldCell.EMPTY

   def is_minion(self):
      return self.status == WorldCell.MINION

   def is_gold(self):
      return self.status == WorldCell.GOLD

   def is_wumpus(self):
      return self.status == WorldCell.WUMPUS

   def is_pit(self):
      return self.status == WorldCell.PIT

# ------------------------------------------------------------------------------

   def is_breezy(self):
      if self.cell_up != None:
         if self.cell_up.status == WorldCell.PIT:
            return True
      
      if self.cell_down != None:
         if self.cell_down.status == WorldCell.PIT:
            return True

      if self.cell_left != None:
         if self.cell_left.status == WorldCell.PIT:
            return True
      
      if self.cell_right != None:
         if self.cell_right.status == WorldCell.PIT:
            return True

   def is_smelly(self):
      if self.cell_up != None:
         if self.cell_up.status == WorldCell.WUMPUS:
            return True
      
      if self.cell_down != None:
         if self.cell_down.status == WorldCell.WUMPUS:
            return True

      if self.cell_left != None:
         if self.cell_left.status == WorldCell.WUMPUS:
            return True
      
      if self.cell_right != None:
         if self.cell_right.status == WorldCell.WUMPUS:
            return True

   def is_shiny(self):
      return self.status == WorldCell.GOLD

# ------------------------------------------------------------------------------