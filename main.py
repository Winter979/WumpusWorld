#! python3

from gui import Gui
from world import World

def main():
    
    gui = Gui()
    world = World(gui)
    world.start()

if __name__ == "__main__":
    main()