from Engine import *

e = Engine("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

# print(e.get_board())
# print(e.generate_legal_moves())
# print(e.get_board())

# Play random moves against itself
def random_move_game(): 
    while e.generate_legal_moves():
        if e.board.half_move_count == 100:
            print("Draw by 50 Move Rule")
            break
        if e.board.threefold:
            print("Draw by threefold repetition")
            break
        e.make_random_move()
        
    print(e.get_board())
    print(e.move_log)
        

# random_move_game()

print(e.evaluate(e.board))
