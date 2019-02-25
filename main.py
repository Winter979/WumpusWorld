#! python3

from gui import Gui
from world import World

def main():
    
    print("Making Gui")
    gui = Gui(cells_x = 5, cells_y=5)
    print("Making World")
    world = World(gui)
    print("Starting Simulation")
    world.start()

if __name__ == "__main__":
    main()