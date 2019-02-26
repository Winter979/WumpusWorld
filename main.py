#! python3

from gui import Gui
from world import World

def main():
    
    gui = Gui(cells_x = 5, cells_y=5)
    world = World(gui)
    world.start()

if __name__ == "__main__":
    main()  