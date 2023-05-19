import copy
import random
from connect4 import Connect4, AbstractPlayer


def naive_score_board(board, p1_symbol, p2_symbol):
    n_large, n_high = len(board), len(board[0])
    score = 0
    for x_i in range(n_large):
        for y_j in range(n_high):
            if board[x_i][y_j] == p1_symbol:
                score += 3 - abs(x_i - 3) + 2 - abs(y_j - 2)
            elif board[x_i][y_j] == p2_symbol:
                score -= 3 - abs(x_i - 3) + 2 - abs(y_j - 2)
    return score


def score_coordinates(board, coordinates, p1_symbol, p2_symbol, win_spots, lost_spots, score_win=100000,
                      score_three=13, score_two=4, score_one=1):
    assert len(coordinates) == 4
    t = [board[t[0]][t[1]] for t in coordinates]
    my_count, op_count = t.count(p1_symbol), t.count(p2_symbol)
    score = 0

    for p1_count, p2_count, sign in [(my_count, op_count, 1), (op_count, my_count, -1)]:
        if not p2_count:
            if p1_count == 4:
                score += sign * score_win
            elif p1_count == 3:
                score += sign * score_three
                for t in coordinates:
                    if board[t[0]][t[1]] != p1_symbol:
                        if sign == 1:
                            win_spots.append(t)
                        else:
                            lost_spots.append(t)
                        break
            elif p1_count == 2:
                score += sign * score_two
            elif p1_count == 1:
                score += sign * score_one
    return score


def advanced_score_board(board, p1_symbol, p2_symbol, score_win=100000, score_trap=10000, score_three=13,
                         score_two=4, score_one=1):
    n_large, n_high = len(board), len(board[0])
    score, win_spots, lost_spots = 0, list(), list()

    # vertical win
    for x_i in range(n_large):
        for y_j in range(n_high - 3):
            score += score_coordinates(board, [(x_i, y_j + i) for i in range(4)], p1_symbol, p2_symbol, win_spots,
                                       lost_spots, score_win, score_three, score_two, score_one)

    for x_i in range(n_large - 3):
        # horizontal_win
        for y_j in range(n_high):
            score += score_coordinates(board, [(x_i + i, y_j) for i in range(4)], p1_symbol, p2_symbol, win_spots,
                                       lost_spots, score_win, score_three, score_two, score_one)

        # diagonal_win /
        for y_j in range(n_high - 3):
            score += score_coordinates(board, [(x_i + i, y_j + i) for i in range(4)], p1_symbol, p2_symbol, win_spots,
                                       lost_spots, score_win, score_three, score_two, score_one)

        # diagonal_win \
        for y_j in range(3, n_high):
            score += score_coordinates(board, [(x_i + i, y_j - i) for i in range(4)], p1_symbol, p2_symbol, win_spots,
                                       lost_spots, score_win, score_three, score_two, score_one)

    for p1_spots, p2_spots, sign in [(win_spots, lost_spots, 1), (lost_spots, win_spots, -1)]:
        for t in p1_spots:
            if all([(t[0], t[1]-i) not in p2_spots for i in range(6)]) and (t[0], t[1] + 1) in p1_spots:
                score += sign * score_trap

    return score


def minimax_play(board, p1_symbol, p2_symbol, score_fct=naive_score_board, depth=5):
    n_large, n_high = len(board), len(board[0])
    plays = []
    possible_moves = list(range(n_large))
    random.shuffle(possible_moves)
    for x_i in possible_moves:
        if board[x_i][n_high - 1] != "-":
            continue

        cur_board = copy.deepcopy(board)
        res_board = Connect4.play(cur_board, x_i, p1_symbol)
        r = Connect4.check_win(res_board)
        if r == p1_symbol:
            score = 100000
            return score, x_i
        elif r == p2_symbol:
            score = -100000
        elif r == "tie":
            score = 0
        elif depth == 0 and r is None:
            score = score_fct(res_board, p1_symbol, p2_symbol)
        else:
            sc, _ = minimax_play(res_board, p2_symbol, p1_symbol, score_fct, depth - 1)
            score = -sc
        plays.append((score, x_i))

    if len(plays):
        # max always return the same value (move most on the right), we want a random good one
        return [p for p in plays if p[0] == max(plays)[0]][0]
    else:
        return 0, 0  # not moves to play, it's a forecasted tie, score 0, position irrelevant


class NaiveMinimaxPlayer(AbstractPlayer):

    def __init__(self, connect4_game: Connect4, own_symbol: str, op_symbol: str, depth: int = 5, display=True):
        self.depth = depth
        self.display = display
        super(NaiveMinimaxPlayer, self).__init__(connect4_game, own_symbol, op_symbol)

    def play(self, board):
        x_i = minimax_play(board, self.own_symbol, self.op_symbol, naive_score_board, self.depth)[1]
        if self.display:
            print(f"'{self.own_symbol}' ({self.__class__.__name__}) played: '{x_i}'")
        return x_i


class MinimaxPlayer(AbstractPlayer):

    def __init__(self, connect4_game: Connect4, own_symbol: str, op_symbol: str, depth: int = 5, display=True):
        self.depth = depth
        self.display = display
        super(MinimaxPlayer, self).__init__(connect4_game, own_symbol, op_symbol)

    def play(self, board):
        x_i = minimax_play(board, self.own_symbol, self.op_symbol, advanced_score_board, self.depth)[1]
        if self.display:
            print(f"'{self.own_symbol}' ({self.__class__.__name__}) played: '{x_i}'")
        return x_i
