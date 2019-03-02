#! python3

class Minion:
   def __init__(self, world):
      self.world = world
      self.x, self.y = world.get_minion_xy()
      self.max_x, self.max_y = world.get_max_xy()

      self.setup_grid()

      self.grid[self.x][self.y].discovered = True

      # Heap to determine which cell to go to next
      self.new_cells = []

   def setup_grid(self):
      self.grid = [[Cell(ii, jj) for jj in range(self.max_y+1)] for ii in range(self.max_x+1)]

      for x in range(self.max_x+1):
         for y in range(self.max_y+1):
            cell = self.grid[x][y]

            # print("*"*80)

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

      if not self.grid[x][y].been_to:
         self.grid[x][y].been_to = True

         if self.world.is_safe(x,y):

            self.update_dangers()
            new_x, new_y = self.find_next()

            self.move_to_dest(new_x, new_y)

            self.x = new_x
            self.y = new_y
         else:
            print("im dead") 
      else:
         print("You have been here before")

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

# ------------------------------------------------------------------------------
            
   def find_next(self):
      x = self.x
      y = self.y

      current = self.grid[x][y]

      adj = current.get_adjacent()

      print("Currently at:", x,y)

      for cell in adj:
         if cell != None and not cell.discovered:
            print("discoverd: ", cell.x, cell.y)
            self.new_cells.insert(0,cell)
            cell.discovered = True

      list.sort(self.new_cells)

      dest_cell = self.new_cells.pop(0)

      print("Going to:", dest_cell.x, dest_cell.y)

      print("="*80)

      return dest_cell.x, dest_cell.y

# ------------------------------------------------------------------------------

   def move_to_dest(self, dest_x, dest_y):

      curr_x = self.x
      curr_y = self.y

      # Check if you only need to move 1 square. No need for searching if so
      if abs(dest_x - curr_x) + abs(dest_y - curr_y) == 1:
         self.world.move_minion(dest_x, dest_y)
      else:
         self.world.jump_minion(dest_x, dest_y)

         # visited = [[False for ii in range(self.max_x+1)] for jj in range(self.max_y+1)]
         # for x in range(self.max_x+1):
         #    for y in range(self.max_y):
         #       # You cant visit a cell you havent discovered yet
         #       if self.grid[x][y].discovered:
         #          visited[x][y] = True

         # queue = [] 
         # queue.append([curr_x, curr_y]) 
         # visited[curr_x][curr_y] = True 
         # while len(queue) > 0 :            

         #    cell = queue.pop(0)

         #    # Destination found 
         #    if [cell[0]] == dest_x and cell[1] == dest_y  :
         #       print("YAY YOU MADE IT")
         #       return
      
         #    # moving up 
         #    if cell[1] - 1 >= 0 and visited[cell[0]][cell[1]-1] == False: 
         #       queue.append([cell[0], cell[1]-1])
         #       self.world.move_minion(cell[0], cell[1]-1)
         #       visited[cell[0]][cell[1]-1] = True 

         #    # moving down 
         #    if cell[1] + 1 < self.max_y+1 and visited[cell[0]][cell[1]+1] == False: 
         #       queue.append([cell[0], cell[1]+1])
         #       self.world.move_minion(cell[0], cell[1]+1)
         #       visited[cell[0]][cell[1]+1] = True 

         #    # moving left 
         #    if cell[0] - 1 >= 0 and visited[cell[0]- 1][cell[1]] == False: 
         #       queue.append([cell[0]- 1, cell[1]])
         #       self.world.move_minion(cell[0]- 1, cell[1])
         #       visited[cell[0]- 1][cell[1]] = True 
            
         #    # moving right 
         #    if cell[0] + 1 < self.max_x+1 and visited[cell[0] + 1][cell[1]] == False: 
         #       queue.append([cell[0] + 1, cell[1]])
         #       self.world.move_minion(cell[0] + 1, cell[1])
         #       visited[cell[0] + 1][cell[1]] = True  


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
      if self.status == Cell.SAFE:
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

