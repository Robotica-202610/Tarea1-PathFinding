class Graph:
    """
    Class representing a Graph structure.
    Attributes:
        nodes (list): List of nodes in the Graph.
        edges (dict): Dictionary mapping each node to its list of connected nodes.
    """

    def __init__(self):
        self.nodes = []
        self.edges = {}

    def display_graph(self):
        """
        Displays the current state of the Graph.
        :return: None
        """
        for node in self.nodes:
            print(f"Node {node}: Edges -> {self.edges.get(node, [])}")

    def build_from_board(self, board):
        """
        Builds the Graph from a given Board.
        :param board: 2D array representing the Board.
        :return: None
        """
        r, c = board.shape
        for i in range(r):
            for j in range(c):
                if board[i][j] == -1: # Occupied position
                    pass
                else:
                    self.nodes.append( (i, j) ) # Add node
                    self.edges[ (i, j) ] = [] # Init. edges for the node
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < r and 0 <= nj < c and board[ni][nj] != -1: # If the positions are valid
                            self.edges[(i, j)].append((ni, nj))
