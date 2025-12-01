import sys
import os

# Add the 'src' directory to the Python system path so Python can find your code package
# This line assumes main.py is in the root directory and src is a sibling folder.
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Import the Game class from the 'platformer' package (specifically the game module inside it)
from platformer.game import Game


def main():
    g = Game()
    g.play()


if __name__ == "__main__":
    main()
