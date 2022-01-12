from Rook import *
from Queen import *
from Knight import *
from Bishop import *
from King import *
from Pawn import *
import random
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

    piece_indices = {
        "wp" : 1,
        "bp" : 2,
        "wN" : 3,
        "bN" : 4,
        "wB": 5,
        "bB" : 6,
        "wR" : 7,
        "bR": 8,
        "wQ" : 9,
        "bQ" : 10,
        "wK" : 11,
        "bK" : 12
    }

    set_up = False
    table = []

    def __init__(self, fen, board = None):
        if board == None:
            fen_parts = fen.split(" ")

            self.side_to_move = 1 if fen_parts[1] == "w" else -1

            self.white_can_castle_kingside = True if "K" in fen_parts[2] else False
            self.white_can_castle_queenside = True if "Q" in fen_parts[2] else False
            self.black_can_castle_kingside = True if "k" in fen_parts[2] else False
            self.black_can_castle_queenside = True if "q" in fen_parts[2] else False

            self.en_passant_square = "-" if fen_parts[3] == "-" else fen_parts[3]

            self.half_move_count = int(fen_parts[4])

            self.full_move_count = int(fen_parts[5])

            self.BOARD = ["-" for _ in range(64)]
            self.BOARD.extend([None for _ in range(20)]) # Over/Underflow buffer

            self.process_FEN(fen_parts[0])
            # pieces = fen_parts[0]

            # self.white_piece_count = {
            #     "pawn" : pieces.count("P"),
            #     "knight" : pieces.count("N"),
            #     "bishop" : pieces.count("B"),
            #     "rook" : pieces.count("R"),
            #     "queen" : pieces.count("Q"),
            #     "king" : pieces.count("K")
            # }

            # self.black_piece_count = {
            #     "pawn" : pieces.count("p"),
            #     "knight" : pieces.count("n"),
            #     "bishop" : pieces.count("b"),
            #     "rook" : pieces.count("r"),
            #     "queen" : pieces.count("q"),
            #     "king" : pieces.count("k")
            # }

            self.history = {}

            self.threefold = False
            self.twofold = False

            self.legal_moves = None

            # Zobrist Initialization:
            if not Board.set_up:
                Board.table = [[Board.rand_bitstring(64) for _ in range(13)] for _ in range(64)]
                Board.set_up = True

        else:
            self.side_to_move = board.side_to_move
            self.white_can_castle_kingside = board.white_can_castle_kingside
            self.white_can_castle_queenside = board.white_can_castle_queenside
            self.black_can_castle_kingside = board.black_can_castle_kingside
            self.black_can_castle_queenside = board.black_can_castle_queenside
            self.en_passant_square = board.en_passant_square
            self.half_move_count = board.half_move_count
            self.full_move_count = board.full_move_count

            self.BOARD = board.BOARD[:]

            self.history = board.history.copy()

            # self.white_piece_count = board.white_piece_count.copy()
            # self.black_piece_count = board.black_piece_count.copy()

            self.threefold = board.threefold
            self.twofold = board.twofold

            self.legal_moves = board.legal_moves


    def rand_bitstring(p):
        key1 = random.randint(0, 1)
        for i in range(p - 1):
            key1 *= 10
            key1 += random.randint(0, 1)
        return key1
            


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

    # Return valu located at specifiec board square by algebraic notation
    def get_coord(self, coord):
        return None if Board.coord_to_index.get(coord, -1) == -1 else self.BOARD[Board.coord_to_index.get(coord, -1)]

    # Modify square on board
    def set(self, index, val):
        self.BOARD[index] = val

    # Modify square on board specified by coordinate
    def set_coord(self, coord, val):
        self.BOARD[Board.coord_to_index[coord]] = val

    def __str__(self):
        i = 56
        letters = "abcdefgh"
        final_string = ""
        for row in range(8):
            row_string = ""
            row_string += " " + str(8 - row) + " "
            for col in range(8):
                row_string += str(self.BOARD[i]) + " "
                i += 1
            i -= 16
            row_string += "\n"
            final_string += row_string
        final_string += "   a b c d e f g h\n"
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

    # Execute given move and update board metadata accordingly
    def move(self, move_tuple):
        if move_tuple[0] == "O-O" and self.side_to_move == 1:
            # self.set_coord("g1", self.get_coord("e1"))
            self.BOARD[Board.coord_to_index["g1"]] = self.BOARD[Board.coord_to_index["e1"]]
            # self.set_coord("f1", self.get_coord("h1"))
            self.BOARD[Board.coord_to_index["f1"]] = self.BOARD[Board.coord_to_index["h1"]]
            # self.set_coord("e1", "-")
            self.BOARD[Board.coord_to_index["e1"]] = "-"
            # self.set_coord("h1", "-")
            self.BOARD[Board.coord_to_index["h1"]] = "-"
            self.white_can_castle_kingside = False
            self.white_can_castle_queenside = False
        elif move_tuple[0] == "O-O-O" and self.side_to_move == 1:
            # self.set_coord("c1", self.get_coord("e1"))
            self.BOARD[Board.coord_to_index["c1"]] = self.BOARD[Board.coord_to_index["e1"]]
            # self.set_coord("d1", self.get_coord("a1"))
            self.BOARD[Board.coord_to_index["d1"]] = self.BOARD[Board.coord_to_index["a1"]]
            # self.set_coord("e1", "-")
            self.BOARD[Board.coord_to_index["e1"]] = "-"
            # self.set_coord("a1", "-")
            self.BOARD[Board.coord_to_index["a1"]] = "-"
            self.white_can_castle_queenside = False
            self.white_can_castle_kingside = False
        elif move_tuple[0] == "O-O" and self.side_to_move == -1:
            # self.set_coord("g8", self.get_coord("e8"))
            self.BOARD[Board.coord_to_index["g8"]] = self.BOARD[Board.coord_to_index["e8"]]
            # self.set_coord("f8", self.get_coord("h8"))
            self.BOARD[Board.coord_to_index["f8"]] = self.BOARD[Board.coord_to_index["h8"]]
            # self.set_coord("e8", "-")
            self.BOARD[Board.coord_to_index["e8"]] = "-"
            # self.set_coord("h8", "-")
            self.BOARD[Board.coord_to_index["h8"]] = "-"
            self.black_can_castle_kingside = False
            self.black_can_castle_queenside = False
        elif move_tuple[0] == "O-O-O" and self.side_to_move == -1:
            # self.set_coord("c8", self.get_coord("e8"))
            self.BOARD[Board.coord_to_index["c8"]] = self.BOARD[Board.coord_to_index["e8"]]
            # self.set_coord("d8", self.get_coord("a8"))
            self.BOARD[Board.coord_to_index["d8"]] = self.BOARD[Board.coord_to_index["a8"]]
            # self.set_coord("e8", "-")
            self.BOARD[Board.coord_to_index["e8"]] = "-"
            # self.set_coord("a8", "-")
            self.BOARD[Board.coord_to_index["a8"]] = "-"
            self.black_can_castle_queenside = False
            self.black_can_castle_kingside = False
        else: 
            # self.set(move_tuple[2], self.BOARD[move_tuple[1]])
            # id = None if self.BOARD[move_tuple[2]] == "-" else self.BOARD[move_tuple[2]].id
            self.BOARD[move_tuple[2]] = self.BOARD[move_tuple[1]]
            # if self.side_to_move == 1 and id != None:
            #     self.black_piece_count[id] -= 1
            # elif id != None:
            #     self.white_piece_count[id] -= 1
            # self.set(move_tuple[1], "-")
            self.BOARD[move_tuple[1]] = "-"
            if len(move_tuple) == 4:
                # self.set(move_tuple[3], "-")
                self.BOARD[move_tuple[3]] = "-"
                # if self.side_to_move == 1:
                #     self.black_piece_count["pawn"] -= 1
                # else:
                #     self.white_piece_count["pawn"] -= 1
            if move_tuple[1] == 0 and self.side_to_move == 1:
                self.white_can_castle_queenside = False
            if move_tuple[1] == 7 and self.side_to_move == 1:
                self.white_can_castle_kingside = False
            if move_tuple[1] == 4 and self.side_to_move == 1:
                self.white_can_castle_queenside = False
                self.white_can_castle_kingside = False
            if move_tuple[1] == 60 and self.side_to_move == -1:
                self.black_can_castle_queenside = False
            if move_tuple[1] == 63 and self.side_to_move == -1:
                self.black_can_castle_kingside = False
            if move_tuple[1] == 56 and self.side_to_move == -1:
                self.black_can_castle_queenside = False
                self.black_can_castle_kingside = False
        
            if "=Q" in move_tuple[0]:
                # self.set(move_tuple[2], Queen(self.side_to_move))
                self.BOARD[move_tuple[2]] = Queen(self.side_to_move)
                # if self.side_to_move == 1:
                #     self.white_piece_count["pawn"] -= 1
                #     self.white_piece_count["queen"] += 1
                # else:
                #     self.black_piece_count["pawn"] -= 1
                #     self.black_piece_count["queen"] += 1
            if "=R" in move_tuple[0]:
                # self.set(move_tuple[2], Rook(self.side_to_move))
                self.BOARD[move_tuple[2]] = Rook(self.side_to_move)
                # if self.side_to_move == 1:
                #     self.white_piece_count["pawn"] -= 1
                #     self.white_piece_count["rook"] += 1
                # else:
                #     self.black_piece_count["pawn"] -= 1
                #     self.black_piece_count["rook"] += 1
            if "=B" in move_tuple[0]:
                # self.set(move_tuple[2], Bishop(self.side_to_move))
                self.BOARD[move_tuple[2]] = Bishop(self.side_to_move)
                # if self.side_to_move == 1:
                #     self.white_piece_count["pawn"] -= 1
                #     self.white_piece_count["bishop"] += 1
                # else:
                #     self.black_piece_count["pawn"] -= 1
                #     self.black_piece_count["bishop"] += 1
            if "=N" in move_tuple[0]:
                # self.set(move_tuple[2], Knight(self.side_to_move))
                self.BOARD[move_tuple[2]] = Knight(self.side_to_move)
                # if self.side_to_move == 1:
                #     self.white_piece_count["pawn"] -= 1
                #     self.white_piece_count["knight"] += 1
                # else:
                #     self.black_piece_count["pawn"] -= 1
                #     self.black_piece_count["knight"] += 1

            if len(move_tuple) == 5:
                self.en_passant_square = Board.index_to_coord[move_tuple[4]]
            else:
                self.en_passant_square = "-"

        if self.side_to_move == -1:
            self.full_move_count += 1
        
        if (("N" in move_tuple[0] or "B" in move_tuple[0] or "Q" in move_tuple[0] or "R" in move_tuple[0] or "K" in move_tuple[0]) and "x" not in move_tuple[0]) or "O-O" in move_tuple[0]:
            self.half_move_count += 1
        else:
            self.half_move_count = 0

        self.side_to_move *= -1


        key = tuple(self.BOARD)
        self.history[key] = self.history.get(key, 0) + 1
        if self.history[key] == 3:
            self.threefold = True
        elif self.history[key] == 2:
            self.twofold = True

    # Check if current position includes any checks on the king of specified color
    def check_for_checks(self, color):
        
        # First find the king's location
        loc = -1
        for i in range(64):
            if isinstance(self.BOARD[i], King) and self.BOARD[i].color == color:
                loc = i
        
        # Check for king checks (?)
        if (isinstance(self.BOARD[loc + 1], King) 
            or isinstance(self.BOARD[loc - 1], King) 
            or isinstance(self.BOARD[loc + 8], King) 
            or isinstance(self.BOARD[loc - 8], King)
            or (isinstance(self.BOARD[loc + 7], King) and Board.index_2_coord(loc)[0] != "a")
            or (isinstance(self.BOARD[loc + 9], King) and Board.index_2_coord(loc)[0] != "h")
            or (isinstance(self.BOARD[loc - 7], King) and Board.index_2_coord(loc)[0] != "h")
            or (isinstance(self.BOARD[loc - 9], King) and Board.index_2_coord(loc)[0] != "a")):
            return True

        # Check for knight checks
        if ((isinstance(self.BOARD[loc + 10], Knight) and Board.index_2_coord(loc)[0] <= "f" and self.BOARD[loc + 10].color == color * -1) or
            (isinstance(self.BOARD[loc + 17], Knight) and Board.index_2_coord(loc)[0] <= "g" and self.BOARD[loc + 17].color == color * -1) or
            (isinstance(self.BOARD[loc + 6], Knight) and Board.index_2_coord(loc)[0] >= "c" and self.BOARD[loc + 6].color == color * -1) or
            (isinstance(self.BOARD[loc + 15], Knight) and Board.index_2_coord(loc)[0] >= "b" and self.BOARD[loc + 15].color == color * -1) or
            (isinstance(self.BOARD[loc - 10], Knight) and Board.index_2_coord(loc)[0] >= "c" and self.BOARD[loc - 10].color == color * -1) or
            (isinstance(self.BOARD[loc - 17], Knight) and Board.index_2_coord(loc)[0] >= "b" and self.BOARD[loc - 17].color == color * -1) or
            (isinstance(self.BOARD[loc - 6], Knight) and Board.index_2_coord(loc)[0] <= "f" and self.BOARD[loc - 6].color == color * -1) or
            (isinstance(self.BOARD[loc - 15], Knight) and Board.index_2_coord(loc)[0] <= "g" and self.BOARD[loc - 15].color == color * -1)):
            return True
        
        # Check for pawn checks
        if (color == 1 and ((isinstance(self.BOARD[loc + 7], Pawn) and self.BOARD[loc + 7].color == color * -1 and Board.index_2_coord(loc)[0] >= "b") or (isinstance(self.BOARD[loc + 9], Pawn) and self.BOARD[loc + 9].color == color * -1 and Board.index_2_coord(loc)[0] <= "g"))):
            return True
        if (color == -1 and ((isinstance(self.BOARD[loc - 7], Pawn) and self.BOARD[loc - 7].color == color * -1 and Board.index_2_coord(loc)[0] <= "g") or (isinstance(self.BOARD[loc - 9], Pawn) and self.BOARD[loc - 9].color == color * -1 and Board.index_2_coord(loc)[0] >= "b"))):
            return True

        # Check for bishop checks
        # NE Diagonal
        if Board.index_2_coord(loc)[0] != "h":
            j = loc
            while self.BOARD[j + 9] == "-" and Board.index_2_coord(j + 9)[0] != "h":
                j += 9
            j += 9
            if (isinstance(self.BOARD[j], Bishop) or isinstance(self.BOARD[j], Queen)) and self.BOARD[j].color == color * -1:
                return True

        # NW Diagonal
        if Board.index_2_coord(loc)[0] != "a":
            j = loc
            while self.BOARD[j + 7] == "-" and Board.index_2_coord(j + 7)[0] != "a":
                j += 7
            j += 7
            if (isinstance(self.BOARD[j], Bishop) or isinstance(self.BOARD[j], Queen)) and self.BOARD[j].color == color * -1:
                return True

        # SW Diagonal
        if Board.index_2_coord(loc)[0] != "a":
            j = loc
            while self.BOARD[j - 9] == "-" and Board.index_2_coord(j - 9)[0] != "a":
                j -= 9
            j -= 9
            if (isinstance(self.BOARD[j], Bishop) or isinstance(self.BOARD[j], Queen)) and self.BOARD[j].color == color * -1:
                return True

        # SE Diagonal
        if Board.index_2_coord(loc)[0] != "h":
            j = loc
            while self.BOARD[j - 7] == "-" and Board.index_2_coord(j - 7)[0] != "h":
                j -= 7
            j -= 7
            if (isinstance(self.BOARD[j], Bishop) or isinstance(self.BOARD[j], Queen)) and self.BOARD[j].color == color * -1:
                return True

        # Check for rook checks
        # North
        j = loc
        while self.BOARD[j + 8] == "-":
            j += 8
        j += 8
        if (isinstance(self.BOARD[j], Rook) or isinstance(self.BOARD[j], Queen)) and self.BOARD[j].color == color * -1:
            return True

        # South
        j = loc
        while self.BOARD[j - 8] == "-":
            j -= 8
        j -= 8
        if (isinstance(self.BOARD[j], Rook) or isinstance(self.BOARD[j], Queen)) and self.BOARD[j].color == color * -1:
            return True

        # East
        j = loc
        if Board.index_2_coord(j)[0] != "h":
            while self.BOARD[j + 1] == "-" and Board.index_2_coord(j + 1)[0] != "h":
                j += 1
            j += 1
            if (isinstance(self.BOARD[j], Rook) or isinstance(self.BOARD[j], Queen)) and self.BOARD[j].color == color * -1:
                return True

        # West
        j = loc
        if Board.index_2_coord(j)[0] != "a":
            while self.BOARD[j - 1] == "-" and Board.index_2_coord(j - 1)[0] != "a":
                j -= 1
            j -= 1
            if (isinstance(self.BOARD[j], Rook) or isinstance(self.BOARD[j], Queen)) and self.BOARD[j].color == color * -1:
                return True

        # Queen checks will be checked for within the bishop and rook check code

        return False

    # Determine if the board position can be classified as in the endgame
    def is_endgame(self):
        black_queens = 0
        white_queens = 0
        minor_black = 0
        minor_white = 0
        pieces = 0
        for i in range(64):
            piece = self.BOARD[i]
            if piece != None and piece != "-":
                pieces += 1
                if piece.color == 1 and isinstance(piece, Queen):
                    white_queens += 1
                if piece.color == -1 and isinstance(piece, Queen):
                    black_queens += 1
                if piece.color == 1 and (isinstance(piece, Knight) or isinstance(piece, Bishop)):
                    minor_white += 1
                if piece.color == -1 and (isinstance(piece, Knight) or isinstance(piece, Bishop)):
                    minor_black += 1
        
        if black_queens == 0 and white_queens == 0:
            return True
        if minor_black == 0 and minor_white == 0:
            return True
        if pieces <= 7:
            return
        return False

    # Return the FEN of the current position on the board
    def fen(self):
        fen = ""
        index = 0
        for i in range(9):
            rank_fen = ""
            while index < i * 8:
                if isinstance(self.BOARD[index], Pawn):
                    if self.BOARD[index].color == 1: 
                        rank_fen += "P"
                    else:
                        rank_fen += "p"
                    index += 1
                elif isinstance(self.BOARD[index], Knight):
                    if self.BOARD[index].color == 1: 
                        rank_fen += "N"
                    else:
                        rank_fen += "n"
                    index += 1
                elif isinstance(self.BOARD[index], Bishop):
                    if self.BOARD[index].color == 1: 
                        rank_fen += "B"
                    else:
                        rank_fen += "b"
                    index += 1
                elif isinstance(self.BOARD[index], Queen):
                    if self.BOARD[index].color == 1: 
                        rank_fen += "Q"
                    else:
                        rank_fen += "q"
                    index += 1
                elif isinstance(self.BOARD[index], Rook):
                    if self.BOARD[index].color == 1: 
                        rank_fen += "R"
                    else:
                        rank_fen += "r"
                    index += 1
                elif isinstance(self.BOARD[index], King):
                    if self.BOARD[index].color == 1: 
                        rank_fen += "K"
                    else:
                        rank_fen += "k"
                    index += 1
                else:
                    count = 0
                    while self.BOARD[index] == "-" and index < i * 8:
                        index += 1
                        count += 1
                    rank_fen += str(count)
            fen = "/" + rank_fen + fen
        fen = fen[1:-1]

        fen = fen + " w " if self.side_to_move == 1 else fen + " b "

        castle = False
        if self.white_can_castle_kingside:
            fen += "K"
            castle = True
        if self.white_can_castle_queenside:
            fen += "Q"
            castle = True
        if self.black_can_castle_kingside:
            fen += "k"
            castle = True
        if self.black_can_castle_queenside:
            fen += "q"
            castle = True
        if not castle:
            fen += "-"

        fen += " " + self.en_passant_square + " "

        fen += str(self.half_move_count) + " "

        fen += str(self.full_move_count)

        return fen

    # Produce unique Zobrist Hash of the Board
    def zobrist(self):
        h = 0
        for i in range(64):
            if self.BOARD[i] != "-":
                j = Board.piece_indices[self.BOARD[i].gui_id]
                h = h ^ Board.table[i][j - 1]
            if self.BOARD[i] == "-":
                h = h ^ Board.table[i][12]
        return h

    def syzygy_move(self):
        pass



