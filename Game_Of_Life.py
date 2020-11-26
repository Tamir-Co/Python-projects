import numpy as np
import time
import matplotlib.pyplot as plot


class GameOfLife:
    def __init__(self, size_of_board, starting_position, rules):
        """ init method for class GameOfLife.
        Input size_of_board donates the size of the board, is an integer bigger than 9 and smaller than 1000.
        starting_position donates the starting position options, please refer to the added PDF file. Is an integer.
        rules donates the rules of the game. Is a string
        Output None.
        """
        self.size_of_board = size_of_board
        self.rules = rules
        self.starting_pos = starting_position

        self.B = np.asarray([n for n in rules.split("/")[0][1::]])
        self.S = np.asarray([n for n in rules.split("/")[1][1::]])

        self.dict_of_pos = {1: 0.5, 2: 0.8, 3: 0.2, 4: self.Gosper_Glider_Gun, 5: self.Pulsar, 6: self.Grin}

        if 4 <= self.starting_pos <= 6:
            self.board = np.zeros(shape=(size_of_board, size_of_board), dtype=bool)
            self.dict_of_pos[self.starting_pos]()
        elif 1 <= self.starting_pos <= 3:
            probability = self.dict_of_pos[self.starting_pos]
            self.board = np.random.choice([False, True], size_of_board**2, p=[1-probability, probability])\
                .reshape(size_of_board, size_of_board)
        else:
            self.board = np.random.choice([False, True], size_of_board**2, p=[0.5, 0.5])\
                .reshape(size_of_board, size_of_board)


    def update(self):
        """ This method updates the board game by the rules of the game.
        Input None.
        Output None.
        """
        size = self.size_of_board
        neighbors_board = np.zeros(shape=(size+2, size+2), dtype=object)
        neighbors_board[0:0 + size, 0:0 + size] += self.board
        neighbors_board[0:0 + size, 1:1 + size] += self.board
        neighbors_board[0:0 + size, 2:2 + size] += self.board
        neighbors_board[1:1 + size, 0:0 + size] += self.board
        neighbors_board[1:1 + size, 2:2 + size] += self.board
        neighbors_board[2:2 + size, 0:0 + size] += self.board
        neighbors_board[2:2 + size, 1:1 + size] += self.board
        neighbors_board[2:2 + size, 2:2 + size] += self.board

        neighbors_board = neighbors_board[1:1 + size, 1:1 + size].astype(str)

        neighbors_board = (self.board.astype(str).astype(np.object) + neighbors_board).astype(str)

        self.board = np.zeros(shape=(size, size), dtype=bool)
        for cond in self.B:
            self.board += np.where(neighbors_board == 'False' + cond, True, False)

        for cond in self.S:
            self.board += np.where(neighbors_board == 'True' + cond, True, False)

    def save_board_to_file(self, file_name):
        """ This method saves the current state of the game to a file. You should use Matplotlib for this.
        Input img_name donates the file name. Is a string, for example file_name = '1000.png'
        Output a file with the name that donates filename.
        """
        plot.imsave(file_name, self.board)

    def display_board(self):
        """ This method displays the current state of the game to the screen. You can use Matplotlib for this.
        Input None.
        Output a figure should be opened and display the board.
        """
        plot.imshow(self.board)
        plot.show()

    def return_board(self):
        """ This method returns a list of the board position. The board is a two-dimensional list that every
        cell donates if the cell is dead or alive. Dead will be donated with 0 while alive will be donated with 255.
        Input None.
        Output a list that holds the board with a size of size_of_board*size_of_board.
        """
        return (self.board * 255).tolist()

# ----------------- # ----------------- # ----------------- # ----------------- #

    def Gosper_Glider_Gun(self):
        shape = np.zeros(shape=(11, 38), dtype=bool)
        shape[1][25] = shape[2][23] = shape[2][25] = shape[6][25] = True
        shape[3][13] = shape[3][14] = shape[3][21] = shape[3][22] = shape[3][35] = shape[3][36] = True
        shape[4][12] = shape[4][16] = shape[4][21] = shape[4][22] = shape[4][35] = shape[4][36] = True
        shape[5][1] = shape[5][2] = shape[5][11] = shape[5][17] = shape[5][21] = shape[5][22] = True
        shape[6][1] = shape[6][2] = shape[6][11] = shape[6][15] = shape[6][17] = shape[6][18] = shape[6][23] = True
        shape[7][11] = shape[7][17] = shape[7][25] = shape[8][12] = shape[8][16] = shape[9][13] = shape[9][14] = True
        self.board[9:9 + 11, 9:9 + 38] = shape

    def Pulsar(self):  # assuming the size is odd
        i = self.size_of_board // 2
        self.board[i - 6, i - 4: i - 1] = True
        self.board[i - 6, i + 2: i + 5] = True
        self.board[i - 1, i - 4: i - 1] = True
        self.board[i - 1, i + 2: i + 5] = True
        self.board[i + 1, i - 4: i - 1] = True
        self.board[i + 1, i + 2: i + 5] = True
        self.board[i + 6, i - 4: i - 1] = True
        self.board[i + 6, i + 2: i + 5] = True
        self.board[i - 4: i - 1, i - 6] = True
        self.board[i + 2: i + 5, i - 6] = True
        self.board[i - 4: i - 1, i - 1] = True
        self.board[i + 2: i + 5, i - 1] = True
        self.board[i - 4: i - 1, i + 1] = True
        self.board[i + 2: i + 5, i + 1] = True
        self.board[i - 4: i - 1, i + 6] = True
        self.board[i + 2: i + 5, i + 6] = True

    def Grin(self):
        shape = np.zeros(shape=(4, 4), dtype=bool)
        shape[0][0] = shape[0][3] = True
        shape[1][1] = shape[1][2] = True
        self.board[5:5 + 4, 5:5 + 4] = shape


# ----------------- # ----------------- # ----------------- # ----------------- #
# ----------------- # ----------------- # ----------------- # ----------------- #

if __name__ == '__main__':
    start = time.time()
    game = GameOfLife(60, 1, "B3/S23")
    for iteration in range(20):
        game.update()

    print("\n\n\n")
    print("time : ", time.time() - start)
    print("\n\n\n")
    print(str(game.return_board()).replace(", [", "\n [").replace("0", " ").replace(" 1", "00"))
