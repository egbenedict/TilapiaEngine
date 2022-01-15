import sys
from Engine import *
import cProfile

sys.setrecursionlimit(10**6)

startingFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

engine = Engine("8/4N3/1B1pb3/1p5k/8/P2p4/1P5P/6K1 w - - 0 60")
# print(engine.official_board)
# print(engine.generate_legal_moves(engine.official_board))
# print(engine.official_board.zobrist())

def play_itself(engine):
    while not engine.is_it_over(engine.official_board):
        print(engine.official_board)
        start = time.time()
        move_tuple = engine.alpha_beta_search(engine.official_board, 4, 8, True, True)[1]
        end = time.time()
        engine.move(move_tuple)
        print(move_tuple[0])
        print(str(engine.current_node_count) + " nodes in " + str(end - start) + " seconds\n")
        if engine.just_syzygied:
            print("Move taken from Syzygy Tablebases")
        if engine.just_booked:
            print("Move taken from Book")
        engine.current_node_count = 0
        # print(engine.official_board.white_piece_count)
        # print(engine.official_board.black_piece_count)
    print(engine.official_board)
    print(engine.get_pgn())

def play_human(engine):
    print("Loading Tilapia Chess Engine ...")
    time.sleep(3)
    print("Tilapia Loaded!")

    print("Select a color: White [w] or Black [b]")
    color = ""
    while color != "w" and color != "b":
        color = input().strip()
    print("")
    print("Select Difficulty:")
    print("Easy [e]")
    print("Medium [m]")
    print("Hard [h]")
    difficulty = ""
    while difficulty != "e" and difficulty != "m" and difficulty != "h":
        difficulty = input().strip()

    print("")

    if difficulty == "e":
        depth = 2
        quies = 2
        tablebases = False
        book = False
    elif difficulty == "m":
        depth = 3
        quies = 3
        tablebases = False
        book = False
    else:
        depth = 4
        quies = 4
        tablebases = True
        book = True

    while not engine.is_it_over(engine.official_board):
        print(engine.official_board)
        if color == "w":
            possible_moves = engine.generate_legal_moves(engine.official_board)
            display_list = ""
            for i in range(len(possible_moves)):
                display_list += str(possible_moves[i][0]) + " : [" + str(i) + "], "
            print(display_list)
            print("Select move:")
            move = "-1"
            while int(move) not in [i for i in range(len(possible_moves))]:
                move = input()
                if move == "q":
                    print("Quitting Game")
                    quit()
                if move == "h":
                    display_list = ""
                    for i in range(len(possible_moves)):
                        display_list += str(possible_moves[i][:2]) + " : [" + str(i) + "], "
                    print("")
                    print(display_list)
                    move = "-1"
            engine.move(possible_moves[int(move)])
            if engine.is_it_over(engine.official_board):
                if engine.is_it_checkmate(engine.official_board):
                    print("Checkmate!")
                elif engine.is_it_stalemate(engine.official_board):
                    print("Stalemate!")
                elif engine.official_board.threefold:
                    print("Draw by Threefold Repetition!")
                else:
                    print("Draw by 50 Move Rule!")
                break
            print(engine.official_board)
            comp_move = engine.alpha_beta_search(engine.official_board, depth, quies, book, tablebases)[1]
            print("Tilapia's Move: " + comp_move[0])
            engine.move(comp_move)
        else:
            comp_move = engine.alpha_beta_search(engine.official_board, depth, quies, book, tablebases)[1]
            print("Tilapia's Move: " + comp_move[0])
            engine.move(comp_move)
            print(engine.official_board)
            if engine.is_it_over(engine.official_board):
                if engine.is_it_checkmate(engine.official_board):
                    print("Checkmate!")
                elif engine.is_it_stalemate(engine.official_board):
                    print("Stalemate!")
                elif engine.official_board.threefold:
                    print("Draw by Threefold Repetition!")
                else:
                    print("Draw by 50 Move Rule!")
                break
            possible_moves = engine.generate_legal_moves(engine.official_board)
            display_list = ""
            for i in range(len(possible_moves)):
                display_list += str(possible_moves[i][0]) + " : [" + str(i) + "], "
            print(display_list)
            print("Select move:")
            move = "-1"
            while int(move) not in [i for i in range(len(possible_moves))]:
                move = input()
                if move == "q":
                    print("Quitting Game")
                    quit()
                if move == "h":
                    display_list = ""
                    for i in range(len(possible_moves)):
                        display_list += str(possible_moves[i][:2]) + " : [" + str(i) + "], "
                    print("")
                    print(display_list)
                    move = "-1"
            engine.move(possible_moves[int(move)])
    if engine.is_it_checkmate(engine.official_board):
        print("Checkmate!")
    elif engine.is_it_stalemate(engine.official_board):
        print("Stalemate!")
    elif engine.official_board.threefold:
        print("Draw by Threefold Repetition!")
    else:
        print("Draw by 50 Move Rule!")
    print("")
    print(engine.official_board)
    print("")
    print(engine.get_pgn())

# print(engine.generate_legal_moves(engine.official_board))
# print(engine.alpha_beta(engine.official_board, -float("inf"), float("inf"), 3))
# start = time.time()
print(engine.alpha_beta_search(engine.official_board, 3, 4, True, True))
# print(engine.current_node_count)
# end = time.time()
# print(end - start)
# print(engine.book_move(engine.official_board))
# play_itself(engine)
# print(engine.evaluate(engine.official_board))
# print(engine.syzygy_move(engine.official_board))
# cProfile.run('engine.alpha_beta_search(engine.official_board, 4, 4)')
# cProfile.run('play_itself(engine)')
# print(engine.current_node_count)
# print(engine.official_board.white_piece_count)
# print(engine.official_board.black_piece_count)
# print(engine.generate_pawn_moves(engine.official_board))
