#! python3

from gui import Gui
from world import World

def main():
    
    gui = Gui(cells_x = 4, cells_y=4)
    world = World(gui)
    world.start()

if __name__ == "__main__":
    main()  
