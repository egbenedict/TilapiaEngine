import sys
from Engine import *
import cProfile

sys.setrecursionlimit(10**6)

startingFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

engine = Engine("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

def play_itself(engine):
    while not engine.is_it_over(engine.official_board):
        print(engine.official_board)
        move_tuple = engine.alpha_beta_search(engine.official_board, 2, 2)[1]
        engine.move(move_tuple)
        print(move_tuple[0])
        # print(engine.official_board.white_piece_count)
        # print(engine.official_board.black_piece_count)
    print(engine.official_board)
    print(engine.get_pgn())

def play_human(engine):
    print("Loading Tilapia Chess Engine ...")
    print("Copyright 2022, Uri Kreindler")
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
    elif difficulty == "m":
        depth = 3
        quies = 3
    else:
        depth = 4
        quies = 4

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
            comp_move = engine.alpha_beta_search(engine.official_board, depth, quies)[1]
            print("Tilapia's Move: " + comp_move[0])
            engine.move(comp_move)
        else:
            comp_move = engine.alpha_beta_search(engine.official_board, depth, quies)[1]
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

play_human(engine)