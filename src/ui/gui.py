import tkinter as tk
from dataclasses import field

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.colors import ListedColormap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        self._cmap = ListedColormap(['black', 'lightgray', 'green', 'red', 'orange'])
        self.vcmd = (root.register(validate_int_only), '%P')

        self._fields()
        self._buttons()

        # Bottom area for two matplotlib canvases
        self._create_display_area()

        self.board = None
        self.final = None
        self.path = None

        # prepare colormap: map values (-1,0,1,2,3) -> indices (0..4)
        # colors: obstacle (black), empty (lightgray), initial (green), final (red), path (orange)


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

    def _create_display_area(self):
        """
        Creates the bottom area with two matplotlib canvases: initial and final.
        """
        # parent frame for both canvases
        display_frame = tk.Frame(self.root)
        display_frame.grid(row=4, column=0, columnspan=6, sticky='nsew', padx=5, pady=5)
        # left and right subframes
        left_frame = tk.LabelFrame(display_frame, text="Initial Board")
        right_frame = tk.LabelFrame(display_frame, text="Final Board (with path)")
        left_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        right_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)

        # create figure/canvas for initial
        self.initial_fig = Figure(figsize=(4, 4), dpi=100)
        self.initial_ax = self.initial_fig.add_subplot(111)
        self.initial_canvas = FigureCanvasTkAgg(self.initial_fig, master=left_frame)
        self.initial_canvas.get_tk_widget().pack(fill='both', expand=True)

        # create figure/canvas for final
        self.final_fig = Figure(figsize=(4, 4), dpi=100)
        self.final_ax = self.final_fig.add_subplot(111)
        self.final_canvas = FigureCanvasTkAgg(self.final_fig, master=right_frame)
        self.final_canvas.get_tk_widget().pack(fill='both', expand=True)

        # initialize empty displays
        self._clear_ax(self.initial_ax, "Initial Board")
        self._clear_ax(self.final_ax, "Final Board")

    def _clear_ax(self, ax, title):
        ax.clear()
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.imshow([[0]], cmap=self._cmap, vmin=0, vmax=4, interpolation='nearest')
        ax.figure.canvas.draw_idle()

    def _plot_board_on_axes(self, ax, canvas, board_df, title):
        """
        Plot a DataFrame board on the given axes and draw the Tk canvas.
        Values expected: -1 obstacles, 0 empty, 1 initial, 2 final, 3 path.
        Each cell is rendered as a unit square so every square represents a position.
        """
        ax.clear()
        if board_df is None:
            ax.set_title(title)
            ax.figure.canvas.draw_idle()
            return
        arr = board_df.values.astype(int)
        # shift by +1 to map -1..3 -> 0..4 for ListedColormap
        display_arr = arr + 1
        nrows, ncols = display_arr.shape

        # show each cell as a unit square: extent sets the image to span [0..ncols] x [0..nrows]
        # use origin='upper' so (0,0) corresponds to top-left like array indices
        ax.imshow(display_arr, cmap=self._cmap, vmin=0, vmax=4, interpolation='nearest',
                  extent=(0, ncols, nrows, 0), aspect='equal', origin='upper')

        ax.set_title(title)

        # major ticks at cell centers (hidden labels), minor ticks at integer boundaries for grid lines
        ax.set_xticks([i + 0.5 for i in range(ncols)])
        ax.set_yticks([i + 0.5 for i in range(nrows)])
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        ax.set_xticks(list(range(ncols + 1)), minor=True)
        ax.set_yticks(list(range(nrows + 1)), minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=1)

        canvas.draw_idle()

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

        self.path = bfs(self.board.graph, (self.board.ix, self.board.iy), (self.board.fx, self.board.fy))

        if len(self.path) == 0:
            print("\n>> [ERROR] No path found from initial to final position.\n")
            # still update initial board display
            self._plot_board_on_axes(self.initial_ax, self.initial_canvas, self.board.board, "Initial Board")
            # clear final display
            self._clear_ax(self.final_ax, "Final Board (no path)")
            return
        print(f"\nShortest path: {self.path}")

        print("\nBoard with Path:\n")
        self.final = self.board.draw_path(self.path)

        # update both canvases
        self._plot_board_on_axes(self.initial_ax, self.initial_canvas, self.board.board, "Initial Board")
        self._plot_board_on_axes(self.final_ax, self.final_canvas, self.final.board, "Final Board (with path)")

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