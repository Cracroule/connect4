import random


class Connect4(object):

    def __init__(self, n_large=7, n_high=6):
        # 7 large, 6 high
        self.n_large, self.n_high = n_large, n_high
        self.board = [["-" for y_i in range(n_high)] for x_i in range(n_large)]

    def display(self):
        for y_i in range(self.n_high)[::-1]:
            print(" | ".join([self.board[x_i][y_i] for x_i in range(self.n_large)]))
        print("-|-".join([str(x_i) for x_i in range(self.n_large)]))
        print()

    @staticmethod
    def play(board, x_i, player_symbol):
        n_high = len(board[0])
        for y_i in range(n_high):
            if board[x_i][y_i] == "-":
                board[x_i][y_i] = player_symbol
                return board

    @staticmethod
    def check_win(board):
        n_large, n_high = len(board), len(board[0])
        # vertical win
        for x_i in range(n_large):
            for i in range(n_high-3):
                if board[x_i][i] == board[x_i][i+1] == board[x_i][i+2] == board[x_i][i+3] != "-":
                    return board[x_i][i]

        # horizontal_win
        for y_i in range(n_high):
            for i in range(n_large-3):
                if board[i][y_i] == board[i+1][y_i] == board[i+2][y_i] == board[i+3][y_i] != "-":
                    return board[i][y_i]

        for y_j in range(n_high - 3):
            for x_i in range(n_large-3):  # diagonal_win /
                if board[x_i][y_j] == board[x_i+1][y_j+1] == board[x_i+2][y_j+2] == \
                        board[x_i+3][y_j+3] != "-":
                    return board[x_i][y_j]
            for x_i in range(3, n_large):  # diagonal_win \
                if board[x_i][y_j] == board[x_i-1][y_j+1] == board[x_i-2][y_j+2] == \
                        board[x_i-3][y_j+3] != "-":
                    return board[x_i][y_j]

        if all([board[x_j][n_high-1] != "-" for x_j in range(n_large)]):
            return "tie"

        return None


class AbstractPlayer(object):
    def __init__(self, connect4_game: Connect4, own_symbol: str, op_symbol: str):
        self.connect4_game = connect4_game
        self.own_symbol = own_symbol
        self.op_symbol = op_symbol

    def play(self, board):
        raise NotImplementedError("This is a pure interface, you need to create a player and to implement 'play'")


class HumanPlayer(AbstractPlayer):
    def play(self, board):
        self.connect4_game.display()
        x_i = None
        while True:
            try:
                x_i = int(input(f"'{self.own_symbol}' chose a column to play (and press enter):"))
                assert x_i in range(7)
            except Exception:
                print("invalid entry; please proceed again")
                continue
            break
        return x_i


def run_match(game, player1, player2, starting_player=None, display_p1: bool = False, display_p2: bool = False):
    starting_player = random.choice([0, 1]) if starting_player is None else starting_player
    turn = 0
    while True:
        playing_player = player1 if turn % 2 == starting_player else player2

        if turn % 2 == starting_player:
            x_i = player1.play(game.board)
            game.play(game.board, x_i, player_symbol=playing_player.own_symbol)
            if display_p1:
                game.display()
        else:
            x_i = player2.play(game.board)
            game.play(game.board, x_i, player_symbol=playing_player.own_symbol)
            if display_p2:
                game.display()
        victory = game.check_win(game.board)
        if victory is not None:
            print(f"{victory} wins!")
            game.display()
            print("###############################################")
            break
        turn += 1
    return victory


# human vs human below
if __name__ == "__main__":
    connect4 = Connect4()
    p1_symbol, p2_symbol = "x", "o"
    p1 = HumanPlayer(connect4, p1_symbol, p2_symbol)
    p2 = HumanPlayer(connect4, p2_symbol, p1_symbol)
    run_match(connect4, p1, p2)
