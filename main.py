import collections
import random
from connect4 import Connect4, HumanPlayer, run_match
from minimax_player import NaiveMinimaxPlayer, MinimaxPlayer

ai_display = True
random.seed(42)

# human vs human below
if __name__ == "__main__":

    n_games = 100
    tournament_results = collections.defaultdict(int)
    p1_symbol, p2_symbol = "x", "o"

    for i in range(n_games):
        power4 = Connect4()
        # p1 = HumanPlayer(power4, p1_symbol, p2_symbol)
        # p2 = HumanPlayer(power4, p2_symbol, p1_symbol)
        p1 = NaiveMinimaxPlayer(power4, p1_symbol, p2_symbol, depth=4, display=ai_display)
        p2 = MinimaxPlayer(power4, p2_symbol, p1_symbol, depth=4, display=ai_display)
        res = run_match(power4, p1, p2, display_p1=ai_display and p1.__class__.__name__ != "HumanPlayer",
                        display_p2=ai_display and p2.__class__.__name__ != "HumanPlayer")
        tournament_results[res] += 1
        print({**tournament_results})

    print({**tournament_results})

