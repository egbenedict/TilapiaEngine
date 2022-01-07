from Engine import *

e = Engine("8/8/8/8/7K/8/8/8 w - - 0 1")

# print(e.get_board())
print(e.generate_legal_moves(e.official_board))
print(e.get_board())

# Play random moves against itself
def random_move_game(): 
    while e.generate_legal_moves(e.official_board):
        if e.official_board.half_move_count == 100:
            print("Draw by 50 Move Rule")
            break
        if e.official_board.threefold:
            print("Draw by threefold repetition")
            break
        e.make_random_move(e.official_board)
        
    print(e.get_board())
    # print(e.move_log)
        

# random_move_game()

# print("Evaluation: " + str(e.evaluate(e.official_board)))
# print(e.official_board.is_endgame())
