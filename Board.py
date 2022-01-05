from Rook import *
from Queen import *
from Knight import *
from Bishop import *
from King import *
from Pawn import *

class Board:

    coord_to_index = {
        "a1" : 0,
        "b1" : 1,
        "c1" : 2,
        "d1" : 3,
        "e1" : 4,
        "f1" : 5,
        "g1" : 6,
        "h1" : 7,
        "a2" : 8,
        "b2" : 9,
        "c2" : 10,
        "d2" : 11,
        "e2" : 12,
        "f2" : 13,
        "g2" : 14,
        "h2" : 15,
        "a3" : 16,
        "b3" : 17,
        "c3" : 18,
        "d3" : 19,
        "e3" : 20,
        "f3" : 21,
        "g3" : 22,
        "h3" : 23,
        "a4" : 24,
        "b4" : 25,
        "c4" : 26,
        "d4" : 27,
        "e4" : 28,
        "f4" : 29,
        "g4" : 30,
        "h4" : 31,
        "a5" : 32,
        "b5" : 33,
        "c5" : 34,
        "d5" : 35,
        "e5" : 36,
        "f5" : 37,
        "g5" : 38,
        "h5" : 39,
        "a6" : 40,
        "b6" : 41,
        "c6" : 42,
        "d6" : 43,
        "e6" : 44,
        "f6" : 45,
        "g6" : 46,
        "h6" : 47,
        "a7" : 48,
        "b7" : 49,
        "c7" : 50,
        "d7" : 51,
        "e7" : 52,
        "f7" : 53,
        "g7" : 54,
        "h7" : 55,
        "a8" : 56,
        "b8" : 57,
        "c8" : 58,
        "d8" : 59,
        "e8" : 60,
        "f8" : 61,
        "g8" : 62,
        "h8" : 63
    }

    index_to_coord = {
        0 : "a1",
        1 : "b1",
        2 : "c1",
        3 : "d1",
        4 : "e1",
        5 : "f1",
        6 : "g1",
        7 : "h1",
        8 : "a2",
        9 : "b2",
        10 : "c2",
        11 : "d2",
        12 : "e2",
        13 : "f2",
        14 : "g2",
        15 : "h2", 
        16 : "a3",
        17 : "b3",
        18 : "c3",
        19 : "d3",
        20 : "e3",
        21 : "f3",
        22 : "g3",
        23 : "h3",
        24 : "a4",
        25 : "b4",
        26 : "c4",
        27 : "d4",
        28 : "e4",
        29 : "f4",
        30 : "g4",
        31 : "h4",
        32 : "a5",
        33 : "b5",
        34 : "c5",
        35 : "d5",
        36 : "e5",
        37 : "f5",
        38 : "g5",
        39 : "h5",
        40 : "a6",
        41 : "b6",
        42 : "c6",
        43 : "d6",
        44 : "e6",
        45 : "f6",
        46 : "g6",
        47 : "h6",
        48 : "a7",
        49 : "b7",
        50 : "c7",
        51 : "d7",
        52 : "e7",
        53 : "f7",
        54 : "g7",
        55 : "h7",
        56 : "a8",
        57 : "b8",
        58 : "c8",
        59 : "d8",
        60 : "e8",
        61 : "f8",
        62 : "g8",
        63 : "h8",
    }

    def __init__(self, fen):
        fen_parts = fen.split(" ")

        self.side_to_move = 1 if fen_parts[1] == "w" else -1

        self.white_can_castle_kingside = True if "K" in fen_parts[2] else False
        self.white_can_castle_queenside = True if "Q" in fen_parts[2] else False
        self.black_can_castle_kingside = True if "k" in fen_parts[2] else False
        self.black_can_castle_queenside = True if "q" in fen_parts[2] else False

        self.en_passant_square = None if fen_parts[3] == "-" else fen_parts[3]

        self.half_move_count = int(fen_parts[4])

        self.full_move_count = int(fen_parts[5])

        self.BOARD = ["-" for i in range(64)]

        self.process_FEN(fen_parts[0])

    # Populate board squares
    def process_FEN(self, fen):
        index = 56
        for character in fen:
            # print(self.BOARD)
            if character == "R":
                self.set(index, Rook(1))
                index += 1
            if character == "r":
                self.set(index, Rook(-1))
                index += 1

            if character == "B":
                self.set(index, Bishop(1))
                index += 1
            if character == "b":
                self.set(index, Bishop(-1))
                index += 1

            if character == "N":
                self.set(index, Knight(1))
                index += 1
            if character == "n":
                self.set(index, Knight(-1))
                index += 1

            if character == "Q":
                self.set(index, Queen(1))
                index += 1
            if character == "q":
                self.set(index, Queen(-1))
                index += 1

            if character == "K":
                self.set(index, King(1))
                index += 1
            if character == "k":
                self.set(index, King(-1))
                index += 1

            if character == "P":
                self.set(index, Pawn(1))
                index += 1
            if character == "p":
                self.set(index, Pawn(-1))
                index += 1

            if character == "/":
                index -= 16

            if character.isdigit():
                index += int(character)
        
    # Return value located at specified board square by index
    def get(self, index):
        return None if index < 0 or index > 63 else self.BOARD[index]

    # Modify square on board
    def set(self, index, val):
        self.BOARD[index] = val

    def __str__(self):
        i = 56
        final_string = ""
        for row in range(8):
            row_string = ""
            for col in range(8):
                row_string += str(self.get(i)) + " "
                i += 1
            i -= 16
            row_string += "\n"
            final_string += row_string
        return final_string

    # Returns crude depiction of board state
    def get_state(self):
        return str(self)

    # Returns the associated index based on board index (algebraic notation)
    def coord_2_index(coord):
        return Board.coord_to_index[coord]

    # Returns the associated coordinate (algebraic notation) based on board index
    def index_2_coord(index):
        return Board.index_to_coord[index]


