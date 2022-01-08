import sys
from Engine import *
import cProfile

sys.setrecursionlimit(10**6)

startingFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

engine = Engine("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
# print(engine.official_board)

def play_itself(engine):
    while not engine.is_it_over(engine.official_board):
        print(engine.official_board)
        move_tuple = engine.alpha_beta_search(engine.official_board, 2)[1]
        engine.move(move_tuple)
        print(move_tuple[0])
    print(engine.official_board)
    print(engine.get_pgn())

# print(engine.generate_legal_moves(engine.official_board))
# print(engine.alpha_beta(engine.official_board, -float("inf"), float("inf"), 3))
# start = time.time()
# print(engine.negamax(engine.official_board, 2))
# print(engine.alpha_beta_search(engine.official_board, 3))
# end = time.time()
# print(engine.current_node_count)
# print(end - start)
# print(engine.evaluate(engine.official_board))
# play_itself(engine)
cProfile.run('engine.alpha_beta_search(engine.official_board, 3)')