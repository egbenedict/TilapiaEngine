from Engine import *

engine = Engine("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

def play_itself(engine):
    for _ in range(20):
        print(engine.official_board)
        move_tuple = engine.search(engine.official_board, 2)[1]
        engine.move(move_tuple)

play_itself(engine)