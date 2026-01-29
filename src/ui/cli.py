import sys
import re

import ui.utils as utils
from logic.board import Board
from logic.bfs import bfs

def run():
    try:
        rc = input("\n>> Enter number of rows and columns as (R,C): ")
        r, c = map(int, utils.clean_string(rc).split(","))

        ixy = input(">> Enter initial position as (x,y): ")
        ix, iy = map(int, utils.clean_string(ixy).split(","))
        if ix < 0 or ix >= r or iy < 0 or iy >= c:
            print("\n>> [ERROR] Initial position out of bounds.\n")
            return

        fxy = input(">> Enter final position as (p,q): ")
        fx, fy = map(int, utils.clean_string(fxy).split(","))
        if fx < 0 or fx >= r or fy < 0 or fy >= c:
            print("\n>> [ERROR] Final position out of bounds.\n")
            return
        if ix == fx and iy == fy:
            print("\n>> [ERROR] Initial and final positions cannot be the same.\n")
            return

        n = int(input(">> Enter number of obstacles N: "))
        if n < 0 or n > r * c - 2:
            print("\n>> [ERROR] Invalid number of obstacles.\n")
            return

        b = Board(r=r, c=c, ix=ix, iy=iy, fx=fx, fy=fy, n=n)

        b.info()
        b.display() # Initial state of the Board

        path = bfs(b.graph, (b.ix, b.iy), (b.fx, b.fy))

        if len(path) == 0:
            print("\n>> [ERROR] No path found from initial to final position.\n")
            return
        print(f"\nShortest path: {path}")

        print("\nBoard with Path:\n")
        final = b.draw_path(path) # Draw the path on the Board
        final.display()  # Final state of the Board with path

        m = input("\n>> Close program? (y/n): ")
        if m.lower() == 'y':
            return False
        print("\n>> [INFO] Restarting...")
        return True

    except KeyboardInterrupt:
        print("\n\nExiting program...\n")
        sys.exit(0)

    except Exception as e:
        print(f"[ERROR] -> {e}")
        return False

def start_cli():
    """
    Starts the command-line interface (CLI) for finding a path for a robot on a board.
    Returns: None
    """
    print("\n=================================================")
    print("\nWelcome to the CLI to find a path for a robot")
    print("Press Ctrl+C to exit at any time")
    t = True
    while t:
        t = run()

if __name__ == "__main__":
    start_cli()
