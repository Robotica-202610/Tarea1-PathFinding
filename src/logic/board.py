import numpy as np
import pandas as pd
from logic.graph import Graph

class Board:
    """
    Class representing a game Board.
    Attributes:
        R (int): Number of rows in the Board.
        C (int): Number of columns in the Board.
        ix (int): Initial x-coordinate.
        iy (int): Initial y-coordinate.
        fx (int): Final x-coordinate.
        fy (int): Final y-coordinate.
        n (int): Some additional parameter (purpose can vary).
    """

    def __init__(self, r=5, c=5, ix=0, iy=0, fx=0, fy=0, n=0):
        self.board = None
        self.graph = None
        self.R = r
        self.C = c
        self.ix = ix
        self.iy = iy
        self.fx = fx
        self.fy = fy
        self.n = n
        self._build_board()

    def board_from_df(self, board: pd.DataFrame):
        """
        Initializes the Board from a given DataFrame.
        :param board: DataFrame representing the Board.
        :return: None
        """
        self.board = board
        self.R, self.C = board.shape
        self.ix, self.iy = map(int, np.argwhere(board.values == 1)[0])
        self.fx, self.fy = map(int, np.argwhere(board.values == 2)[0])
        self.n = np.sum(board.values == -1)
        self._build_graph()

    def _build_board(self) -> None:
        """
        Builds the game Board with initial and final positions marked.
        0 represents empty space,
        1 represents the initial position,
        2 represents the final position,
        -1 represents occupied positions.
        :return: None
        """
        temp_positions= [] # To track occupied positions
        temp_board = np.zeros((self.R, self.C))
        temp_board[self.ix, self.iy] = 1 # Initial position
        temp_board[self.fx, self.fy] = 2 # Final position
        for i in range( self.n ):
            rand_x = np.random.randint(0, self.R)
            rand_y = np.random.randint(0, self.C)
            # Ensure we don't overwrite initial or final positions or previously occupied positions
            while (rand_x, rand_y) in temp_positions or (rand_x == self.ix and rand_y == self.iy) or (rand_x == self.fx and rand_y == self.fy):
                rand_x = np.random.randint(0, self.R)
                rand_y = np.random.randint(0, self.C)
            temp_board[rand_x, rand_y] = -1  # Marking occupied position
            temp_positions.append(rand_x)
        self.board = pd.DataFrame(temp_board).astype(int) # Turn into DataFrame for better visualization
        self._build_graph()

    def info(self):
        """
        Prints the Board's attributes.
        :return: None
        """
        print(f"Board Size: {self.R} x {self.C}")
        print(f"Initial Position: ({self.ix}, {self.iy})")
        print(f"Final Position: ({self.fx}, {self.fy})")
        print(f"Number of Obstacles: {self.n}")

    def display(self):
        """
        Displays the current state of the Board.
        :return: None
        """
        print(self.board)

    def _build_graph(self):
        """
        Builds the Graph representation of the Board.
        :return: None
        """
        self.graph = Graph()
        self.graph.build_from_board(self.board.values)

    def draw_path(self, path):
        """
        Draws the given path on the Board.
        0 represents empty space,
        1 represents the initial position,
        2 represents the final position,
        -1 represents occupied positions.
        3 represents the path taken.
        :param path: List of tuples representing the path coordinates.
        :return: None
        """
        temp_board = self.board.copy()
        for (x, y) in path:
            if temp_board.iat[x, y] == 0:  # Only mark empty spaces
                temp_board.iat[x, y] = 3  # Mark the path with a distinct value
        temp = Board()
        temp.board_from_df(temp_board)
        return temp