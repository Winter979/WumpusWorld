#! python3

from cell import MinionCell

import time

class Minion:
   def __init__(self, world):
      self.world = world
      self.x, self.y = world.get_minion_xy()
      self.max_x, self.max_y = world.get_max_xy()

      # When the smelly count is greate than 1 we have found the wumpus
      self.smelly_count = 0

      self.has_arrow = True

      self.setup_grid()

      self.grid[self.x][self.y].discovered = True

      self.new_cells = []

      self.movements = []

   def setup_grid(self):
      self.grid = [[MinionCell(ii, jj) for jj in range(self.max_y+1)] for ii in range(self.max_x+1)]

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

      if len(self.movements) > 0:
         next_cell_xy = self.movements.pop(0)
         self.move_to_dest(next_cell_xy[0], next_cell_xy[1])
      else:
         x = self.x
         y = self.y

         if not self.grid[x][y].been_to:
            self.grid[x][y].been_to = True

            if self.world.is_safe(x,y):
               if self.world.is_shiny(x,y):
                  print("YOU HAVE FOUND THE GOLD")
               else:
                  self.update_dangers(x,y)
                  new_x, new_y = self.find_next(x, y)

                  self.move_to_dest(new_x, new_y)

                  self.x = new_x
                  self.y = new_y
            else:
               print("im dead") 
         else:
            print("You have been here before")

   def update_dangers(self, x, y):
      breezy = self.world.is_breezy(x,y)
      smelly = self.world.is_smelly(x,y)
      shiny = self.world.is_shiny(x,y)

      cell = self.grid[x][y]

      if breezy:
         cell.add_danger(danger=cell.BREEZY)

      if smelly:
         cell.add_danger(danger=cell.SMELLY)
         self.smelly_count += 1
         if self.has_arrow and self.smelly_count > 1:
            self.found_wumpus()
      
      if not breezy and not smelly:
         cell.remove_danger()

      if shiny:
         cell.set_status(cell.GOLD)

# ------------------------------------------------------------------------------
            
   def find_next(self, x, y):

      current = self.grid[x][y]

      adj = current.get_adjacent()

      for cell in adj:
         if cell != None and not cell.discovered:
            self.new_cells.insert(0,cell)
            cell.discovered = True

      list.sort(self.new_cells)

      dest_cell = self.new_cells.pop(0)

      return dest_cell.x, dest_cell.y

   def found_wumpus(self):
      curr_cell = self.grid[self.x][self.y]

      adj_cells = curr_cell.get_adjacent()

      wumpus_cell = None

      for cell in adj_cells:
         if cell != None and not cell.been_to and cell.smells > 1:
            print("YOU FOUND THE WUMPUS")
            wumpus_cell = cell

      wumpus_dead = self.world.shoot_wumpus(wumpus_cell.x, wumpus_cell.y)
      
      self.has_arrow = False

      if wumpus_dead:
         adj_cells = wumpus_cell.get_adjacent()
         for cell in adj_cells:
            if cell != None and cell.discovered:
               cell.smells = 0

# ------------------------------------------------------------------------------

   def move_to_dest(self, dest_x, dest_y):

      curr_x = self.x
      curr_y = self.y

      # Check if you only need to move 1 square. No need for searching if so
      if abs(dest_x - curr_x) + abs(dest_y - curr_y) == 1:
         self.world.move_minion(dest_x, dest_y)
      else:
         self.world.jump_minion(dest_x, dest_y)

         # print("CONSTUCTING MOVEMENT LIST")

         # visited = [[False for ii in range(self.max_x+1)] for jj in range(self.max_y+1)]
         # for x in range(self.max_x+1):
         #    for y in range(self.max_y):
         #       # You cant visit a cell you havent discovered yet
         #       if self.grid[x][y].discovered:
         #          visited[x][y] = True

         # self.movements = []

         # queue = [] 
         # queue.append([curr_x, curr_y]) 
         # visited[curr_x][curr_y] = True 
         # while len(queue) > 0 :            

         #    cell_xy = queue.pop(0)

         #    # Destination found 
         #    if [cell_xy[0]] == dest_x and cell_xy[1] == dest_y  :
         #       print("YAY YOU MADE IT")
         #       return
      
         #    # moving up 
         #    if cell_xy[1] - 1 >= 0 and visited[cell_xy[0]][cell_xy[1]-1] == False: 
         #       queue.append([cell_xy[0], cell_xy[1]-1])
         #       self.movements.append([cell_xy[0], cell_xy[1]-1])
         #       visited[cell_xy[0]][cell_xy[1]-1] = True 

         #    # moving down 
         #    if cell_xy[1] + 1 < self.max_y+1 and visited[cell_xy[0]][cell_xy[1]+1] == False: 
         #       queue.append([cell_xy[0], cell_xy[1]+1])
         #       self.movements.append([cell_xy[0], cell_xy[1]+1])
         #       visited[cell_xy[0]][cell_xy[1]+1] = True 

         #    # moving left 
         #    if cell_xy[0] - 1 >= 0 and visited[cell_xy[0]- 1][cell_xy[1]] == False: 
         #       queue.append([cell_xy[0]- 1, cell_xy[1]])
         #       self.movements.append([cell_xy[0]- 1, cell_xy[1]])
         #       visited[cell_xy[0]- 1][cell_xy[1]] = True 
            
         #    # moving right 
         #    if cell_xy[0] + 1 < self.max_x+1 and visited[cell_xy[0] + 1][cell_xy[1]] == False: 
         #       queue.append([cell_xy[0] + 1, cell_xy[1]])
         #       self.movements.append([cell_xy[0] + 1, cell_xy[1]])
         #       visited[cell_xy[0] + 1][cell_xy[1]] = True  


