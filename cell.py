#! python3

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
      return self.status == WorldCell.PIT

# ------------------------------------------------------------------------------