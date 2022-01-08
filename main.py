from Engine import *

engine = Engine("8/7Q/8/8/8/5K2/7k/8 b - - 0 1")


def play_itself(engine):
    while not engine.is_it_over(engine.official_board):
        print(engine.official_board)
        move_tuple = engine.search(engine.official_board, 2)[1]
        engine.move(move_tuple)
        print(move_tuple[0])
    print(engine.official_board)
    print(engine.get_pgn())

# print(engine.generate_legal_moves(engine.official_board))
play_itself(engine)