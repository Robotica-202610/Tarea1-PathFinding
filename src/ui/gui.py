import re
import tkinter as tk
from dataclasses import field

import matplotlib.pyplot as plt

import ui.utils as utils
from logic.board import Board
from logic.bfs import bfs

class SimpleGUI:
    """
    A simple graphical user interface (GUI) for the PathFinder application.
    Allows users to input parameters for the board and run the pathfinding algorithm.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("PathFinder GUI")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.vcmd = (root.register(validate_int_only), '%P')

        self._fields()
        self._buttons()

        self.board = None
        self.final = None
        self.path = None


    def _fields(self):
        """
        Creates input fields for the GUI.
        Returns: None
        """
        # ======================== Grid Column 1
        tk.Label(self.root, text="Rows").grid(row=0, column=0)
        tk.Label(self.root, text="Columns").grid(row=1, column=0)
        self.r = tk.Entry(self.root, validate='key', vcmd=self.vcmd)
        self.c = tk.Entry(self.root, validate='key', vcmd=self.vcmd)
        self.r.grid(row=0, column=1)
        self.c.grid(row=1, column=1)
        # ======================== Grid Column 2
        tk.Label(self.root, text="Initial X Coordinate").grid(row=0, column=2)
        tk.Label(self.root, text="Initial Y Coordinate").grid(row=1, column=2)
        tk.Label(self.root, text="Number of Obstacles").grid(row=2, column=2)
        self.ix = tk.Entry(self.root, validate='key', vcmd=self.vcmd)
        self.iy = tk.Entry(self.root, validate='key', vcmd=self.vcmd)
        self.n = tk.Entry(self.root, validate='key', vcmd=self.vcmd)
        self.ix.grid(row=0, column=3)
        self.iy.grid(row=1, column=3)
        self.n.grid(row=2, column=3)
        # ======================== Grid Column 3
        tk.Label(self.root, text="Final X Coordinate").grid(row=0, column=4)
        tk.Label(self.root, text="Final Y Coordinate").grid(row=1, column=4)
        self.fx = tk.Entry(self.root, validate='key', vcmd=self.vcmd)
        self.fy = tk.Entry(self.root, validate='key', vcmd=self.vcmd)
        self.fx.grid(row=0, column=5)
        self.fy.grid(row=1, column=5)

    def _buttons(self):
        """
        Creates buttons for the GUI.
        Returns: None
        """
        run_button = tk.Button(self.root, text="Run", command=self._run)
        quit_button = tk.Button(self.root, text="Quit", command=self.quit)
        run_button.grid(row=3, column=2)
        quit_button.grid(row=3, column=3)

    def _info_popup(self, info):
        """
        Displays information in a message box.
        :param info: The information to display.
        :return: None
        """
        self.root.bell()
        info_box = tk.Toplevel(self.root)
        info_box.title("Alert")
        info_box.geometry("300x300")
        info_box.resizable(False, False)

        info_label = tk.Label(info_box, text=info, wraplength=200, justify=tk.CENTER)
        info_label.pack(pady=10, padx=10)

        close_button = tk.Button(info_box, text="Close", command=info_box.destroy)
        close_button.pack(pady=10)

    def _run(self):
        """
        Run the pathfinding algorithm based on user input.
        :return: None
        """
        validated = self._validate_inputs()
        if validated is None:
            return
        r, c, ix, iy, fx, fy, n = validated

        self.board = Board(r=r, c=c, ix=ix, iy=iy, fx=fx, fy=fy, n=n)

        self.board.info()

        self.path = bfs( self.board.graph, ( self.board.ix, self.board.iy), ( self.board.fx, self.board.fy))

        if len(self.path) == 0:
            print("\n>> [ERROR] No path found from initial to final position.\n")
            return
        print(f"\nShortest path: {self.path}")

        print("\nBoard with Path:\n")
        self.final = self.board.draw_path(self.path)


    def _display_board_in_GUI(self, board, title="Board"):
        """
        Displays the board in a matplotlib window.
        :param board: The board to display.
        :param title: The title of the window.
        :return: None
        """
        plt.figure(title)
        plt.imshow(board.grid, cmap='Greys', interpolation='nearest')
        plt.title(title)
        plt.xticks(range(board.c))
        plt.yticks(range(board.r))
        plt.grid(which='both', color='black', linestyle='-', linewidth=2)
        plt.show()

    def _validate_inputs(self):
        """
        Validates the user inputs.
        :return: A tuple of validated inputs or None if validation fails.
        """
        try:
            r = int(self.r.get())
            if r <= 0:
                self._info_popup("Invalid row number")
                return None
            c = int(self.c.get())
            if c <= 0:
                self._info_popup("Invalid column number")
                return None
            ix = int(self.ix.get())
            if ix < 0 or ix >= r:
                self._info_popup("Initial X coordinate out of bounds")
                return None
            iy = int(self.iy.get())
            if iy < 0 or iy >= c:
                self._info_popup("Initial Y coordinate out of bounds")
                return None
            fx = int(self.fx.get())
            if fx < 0 or fx >= r:
                self._info_popup("Final X coordinate out of bounds")
                return None
            fy = int(self.fy.get())
            if fy < 0 or fy >= c:
                self._info_popup("Final Y coordinate out of bounds")
                return None
            if ix == fx and iy == fy:
                self._info_popup("Initial and final positions cannot be the same")
                return None
            n = int(self.n.get())
            if n < 0 or n > r * c - 2:
                self._info_popup("Invalid number of obstacles")
                return None
        except ValueError as e:
            self._info_popup("Please enter valid integer values for all fields")
            return None
        return r, c, ix, iy, fx, fy, n

    def quit(self):
        """
        Quits the GUI application.
        :return: None
        """
        self.root.quit()

def validate_int_only(p):
    """
    Validates that the input is either empty or an integer.
    :param p: The input string to validate.
    :return: True if the input is valid, False otherwise.
    """
    if p == "":
        return True
    try:
        p = int(p)
        return True
    except ValueError:
        return False

def start_gui():
    """
    Starts the graphical user interface (GUI) for the application.
    Returns: None
    """
    root = tk.Tk()
    gui = SimpleGUI(root)
    root.lift()
    root.mainloop()

if __name__ == "__main__":
    start_gui()