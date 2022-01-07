from Engine import *

engine = Engine("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")


def play_itself(engine):
    while not engine.is_it_over(engine.official_board):
        print(engine.official_board)
        move_tuple = engine.search(engine.official_board, 2)[1]
        engine.move(move_tuple)
        print(move_tuple[0])
    print(engine.official_board)
    print(engine.move_log)

play_itself(engine)