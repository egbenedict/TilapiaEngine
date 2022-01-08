import sys
from Engine import *

sys.setrecursionlimit(10**6)

engine = Engine("8/p1r1nk1p/4p3/2P1Kpp1/5P2/8/P2B1P1P/2R5 b - - 1 1")
print(engine.official_board)

def play_itself(engine):
    while not engine.is_it_over(engine.official_board):
        print(engine.official_board)
        move_tuple = engine.search(engine.official_board, 2)[1]
        engine.move(move_tuple)
        print(move_tuple[0])
    print(engine.official_board)
    print(engine.get_pgn())

# print(engine.generate_legal_moves(engine.official_board))
# print(engine.alpha_beta(engine.official_board, -float("inf"), float("inf"), 3))
# print(engine.search(engine.official_board, 3))
print(engine.alpha_beta_search(engine.official_board, 3))
# play_itself(engine)