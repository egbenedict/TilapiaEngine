from Board import *
from Rook import *
from Queen import *
from Knight import *
from Bishop import *
from King import *
from Pawn import *
import random
import time

class Engine:

    startingFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    piece_values = {
        "pawn" : 1,
        "knight" : 3.2,
        "bishop" : 3.3,
        "rook" : 5,
        "queen" : 9,
        "king" : 200
    }

    NUM_BOOK_MOVES = 10

    def __init__(self, fen = startingFEN, board = None):
        if board == None:
            self.official_board = Board(fen)
        else:
            self.official_board = Board(None, board)
        self.move_log = []
        self.current_node_count = 0

        self.transposition_table = {}

        self.just_syzygied = False
        self.just_booked = False

        self.last_table_try = 0
        self.last_book_try = 0
    
    # Return board object
    def get_board(self):
        return self.official_board

    # Returns list of all legal moves in current board state, in addition to metadata about how to modify board
    def generate_legal_moves(self, board):
        move_list = []
        # Add all pseudo-legal moves first then filter after
        move_list.extend(self.generate_pawn_moves(board))
        move_list.extend(self.generate_knight_moves(board))
        move_list.extend(self.generate_bishop_moves(board))
        move_list.extend(self.generate_rook_moves(board))
        move_list.extend(self.generate_queen_moves(board))
        move_list.extend(self.generate_king_moves(board))
        move_list.extend(self.generate_castle_moves(board))
        
        move_list = self.filter_legal_moves(move_list, board)

        return move_list

    def print_legal_moves(self, board):
        return [x[0] for x in board.legal_moves] if board.legal_moves != None else [x[0] for x in self.generate_legal_moves(board)]

    #TODO: incoroprate piece lists so no need to loop through entire board each time

    # Return a list of all valid pawn moves (including en passant) in current board state
    def generate_pawn_moves(self, board):
        pawn_moves = []
        for i in range(64):
            piece = board.BOARD[i]
            if isinstance(piece, Pawn) and piece.color == board.side_to_move:
                # 1 Square Ahead
                if board.BOARD[i + 8 * piece.color] == "-":
                    move = Board.index_2_coord(i + 8 * piece.color)
                    # Promotion
                    if (i // 8 == 6 and piece.color == 1) or (i // 8 == 1 and piece.color == -1):
                        pawn_moves.append((Board.index_2_coord(i + 8 * piece.color) + "=Q", i, i + 8 * piece.color))
                        pawn_moves.append((Board.index_2_coord(i + 8 * piece.color) + "=R", i, i + 8 * piece.color))
                        pawn_moves.append((Board.index_2_coord(i + 8 * piece.color) + "=B", i, i + 8 * piece.color))
                        pawn_moves.append((Board.index_2_coord(i + 8 * piece.color) + "=N", i, i + 8 * piece.color))
                    else:
                        pawn_moves.append((move, i, i + 8 * piece.color))

                # 2 Squares Ahead
                if (((Board.index_2_coord(i)[1] == "2" and piece.color == 1)
                 or (Board.index_2_coord(i)[1] == "7" and piece.color == -1)) 
                 and board.BOARD[i + 8 * piece.color] == "-" 
                 and board.BOARD[i + 16 * piece.color] == "-"):
                    move = Board.index_2_coord(i + 16 * piece.color)
                    pawn_moves.append((move, i, i + 16 * piece.color, None, i + 8 * piece.color))

                # Diagonal Captures
                if (board.BOARD[i + 7 * piece.color] != None and board.BOARD[i + 7 * piece.color] != "-") and board.BOARD[i + 7 * piece.color].color == piece.color * -1:
                    if not((Board.index_2_coord(i)[0] == "a" and piece.color == 1) or (Board.index_2_coord(i)[0] == "h" and piece.color == -1)):
                        move = Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 7 * piece.color)
                        # Promotion
                        if (i // 8 == 6 and piece.color == 1) or (i // 8 == 1 and piece.color == -1):
                            pawn_moves.append((Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 7 * piece.color) + "=Q", i, i + 7 * piece.color))
                            pawn_moves.append((Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 7 * piece.color) + "=R", i, i + 7 * piece.color))
                            pawn_moves.append((Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 7 * piece.color) + "=B", i, i + 7 * piece.color))
                            pawn_moves.append((Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 7 * piece.color) + "=N", i, i + 7 * piece.color))
                        else:
                            pawn_moves.append((move, i, i + 7 * piece.color))

                if (board.BOARD[i + 9 * piece.color] != None and board.BOARD[i + 9 * piece.color] != "-") and board.BOARD[i + 9 * piece.color].color == piece.color * -1:
                    if not((Board.index_2_coord(i)[0] == "h" and piece.color == 1) or (Board.index_2_coord(i)[0] == "a" and piece.color == -1)):
                        move = Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 9 * piece.color)
                        # Promotion
                        if (i // 8 == 6 and piece.color == 1) or (i // 8 == 1 and piece.color == -1):
                            pawn_moves.append((Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 9 * piece.color) + "=Q", i, i + 9 * piece.color))
                            pawn_moves.append((Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 9 * piece.color) + "=R", i, i + 9 * piece.color))
                            pawn_moves.append((Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 9 * piece.color) + "=B", i, i + 9 * piece.color))
                            pawn_moves.append((Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 9 * piece.color) + "=N", i, i + 9 * piece.color))
                        else:
                            pawn_moves.append((move, i, i + 9 * piece.color))

                # En Passant
                if (board.BOARD[i + 7 * piece.color] != None and Board.index_2_coord(i + 7 * piece.color) == board.en_passant_square):
                    if not((Board.index_2_coord(i)[0] == "a" and piece.color == 1) or (Board.index_2_coord(i)[0] == "h" and piece.color == -1)):
                        move = Board.index_2_coord(i)[0] + "x" + board.en_passant_square
                        pawn_moves.append((move, i, i + 7 * piece.color, i - piece.color))

                if (board.BOARD[i + 9 * piece.color] != None and Board.index_2_coord(i + 9 * piece.color) == board.en_passant_square):
                    if not((Board.index_2_coord(i)[0] == "h" and piece.color == 1) or (Board.index_2_coord(i)[0] == "a" and piece.color == -1)):
                        move = Board.index_2_coord(i)[0] + "x" + board.en_passant_square
                        pawn_moves.append((move, i, i + 9 * piece.color, i + piece.color))

        return pawn_moves

    # Return a list of all valid knight moves in current board state
    def generate_knight_moves(self, board):
        knight_moves = []
        for i in range(64):
            piece = board.BOARD[i]
            if isinstance(piece, Knight) and piece.color == board.side_to_move:
                # NE Squares
                if int(Board.index_2_coord(i)[1]) < 7 and Board.index_2_coord(i)[0] != "h":
                    if board.BOARD[i + 17] == "-":
                        move = "N" + Board.index_2_coord(i + 17)
                        knight_moves.append((move, i, i + 17))
                    elif board.BOARD[i + 17].color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i + 17)
                        knight_moves.append((move, i, i + 17))
                    
                if int(Board.index_2_coord(i)[1]) < 8 and Board.index_2_coord(i)[0] < "g":
                    if board.BOARD[i + 10] == "-":
                        move = "N" + Board.index_2_coord(i + 10)
                        knight_moves.append((move, i, i + 10))
                    elif board.BOARD[i + 10].color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i + 10)
                        knight_moves.append((move, i, i + 10))

                # SE Squares
                if int(Board.index_2_coord(i)[1]) > 1 and Board.index_2_coord(i)[0] < "g":
                    if board.BOARD[i - 6] == "-":
                        move = "N" + Board.index_2_coord(i - 6)
                        knight_moves.append((move, i, i - 6))
                    elif board.BOARD[i - 6].color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i - 6)
                        knight_moves.append((move, i, i - 6))
                    
                if int(Board.index_2_coord(i)[1]) > 2 and Board.index_2_coord(i)[0] < "h":
                    if board.BOARD[i - 15] == "-":
                        move = "N" + Board.index_2_coord(i - 15)
                        knight_moves.append((move, i, i - 15))
                    elif board.BOARD[i - 15].color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i - 15)
                        knight_moves.append((move, i, i - 15))
                            
                # SW Squares
                if int(Board.index_2_coord(i)[1]) > 2 and Board.index_2_coord(i)[0] > "a":
                    if board.BOARD[i - 17] == "-":
                        move = "N" + Board.index_2_coord(i - 17)
                        knight_moves.append((move, i, i - 17))
                    elif board.BOARD[i - 17].color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i - 17)
                        knight_moves.append((move, i, i - 17))
                    
                if int(Board.index_2_coord(i)[1]) > 1 and Board.index_2_coord(i)[0] > "b":
                    if board.BOARD[i - 10] == "-":
                        move = "N" + Board.index_2_coord(i - 10)
                        knight_moves.append((move, i, i - 10))
                    elif board.BOARD[i - 10].color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i - 10)
                        knight_moves.append((move, i, i - 10))

                # NW Squares
                if int(Board.index_2_coord(i)[1]) < 8 and Board.index_2_coord(i)[0] > "b":
                    if board.BOARD[i + 6] == "-":
                        move = "N" + Board.index_2_coord(i + 6)
                        knight_moves.append((move, i, i + 6))
                    elif board.BOARD[i + 6].color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i + 6)
                        knight_moves.append((move, i, i + 6))
                    
                if int(Board.index_2_coord(i)[1]) < 7 and Board.index_2_coord(i)[0] > "a":
                    if board.BOARD[i + 15] == "-":
                        move = "N" + Board.index_2_coord(i + 15)
                        knight_moves.append((move, i, i + 15))
                    elif board.BOARD[i + 15].color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i + 15)
                        knight_moves.append((move, i, i + 15))
        return knight_moves
                        
    # Return a list of all valid bishop moves in current board state
    def generate_bishop_moves(self, board):
        bishop_moves = []
        for i in range(64):
            piece = board.BOARD[i]
            if isinstance(piece, Bishop) and piece.color == board.side_to_move:
                # NE Diagonal
                if Board.index_2_coord(i)[0] < "h":
                    j = i + 9
                    while board.BOARD[j] == "-" and Board.index_2_coord(j)[0] < "h" and int(Board.index_2_coord(j)[1]) < 8:
                        move = "B" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))
                        j += 9
                    if board.BOARD[j] == "-":
                        move = "B" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))
                    elif board.BOARD[j] != None and board.BOARD[j].color == piece.color * -1:
                        move = "Bx" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))

                # SE Diagonal
                if Board.index_2_coord(i)[0] < "h":
                    j = i - 7
                    while board.BOARD[j] == "-" and Board.index_2_coord(j)[0] < "h" and int(Board.index_2_coord(j)[1]) > 1:
                        move = "B" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))
                        j -= 7
                    if board.BOARD[j] == "-":
                        move = "B" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))
                    elif board.BOARD[j] != None and board.BOARD[j].color == piece.color * -1:
                        move = "Bx" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))

                # SW Diagonal
                if Board.index_2_coord(i)[0] > "a":
                    j = i - 9
                    while board.BOARD[j] == "-" and Board.index_2_coord(j)[0] > "a" and int(Board.index_2_coord(j)[1]) > 1:
                        move = "B" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))
                        j -= 9
                    if board.BOARD[j] == "-":
                        move = "B" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))
                    elif board.BOARD[j] != None and board.BOARD[j].color == piece.color * -1:
                        move = "Bx" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))

                # NW Diagonal
                if Board.index_2_coord(i)[0] > "a":
                    j = i + 7
                    while board.BOARD[j] == "-" and Board.index_2_coord(j)[0] > "a" and int(Board.index_2_coord(j)[1]) < 8:
                        move = "B" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))
                        j += 7
                    if board.BOARD[j] == "-":
                        move = "B" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))
                    elif board.BOARD[j] != None and board.BOARD[j].color == piece.color * -1:
                        move = "Bx" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))

        return bishop_moves
    
    # Return a list of all valid queen moves in current board state
    def generate_queen_moves(self, board):
        queen_moves = []
        for i in range(64):
            piece = board.BOARD[i]
            if isinstance(piece, Queen) and piece.color == board.side_to_move:
                # NE Diagonal
                if Board.index_2_coord(i)[0] < "h":
                    j = i + 9
                    while board.BOARD[j] == "-" and Board.index_2_coord(j)[0] < "h" and int(Board.index_2_coord(j)[1]) < 8:
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                        j += 9
                    if board.BOARD[j] == "-":
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                    elif board.BOARD[j] != None and board.BOARD[j].color == piece.color * -1:
                        move = "Qx" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))

                # SE Diagonal
                if Board.index_2_coord(i)[0] < "h":
                    j = i - 7
                    while board.BOARD[j] == "-" and Board.index_2_coord(j)[0] < "h" and int(Board.index_2_coord(j)[1]) > 1:
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                        j -= 7
                    if board.BOARD[j] == "-":
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                    elif board.BOARD[j] != None and board.BOARD[j].color == piece.color * -1:
                        move = "Qx" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))

                # SW Diagonal
                if Board.index_2_coord(i)[0] > "a":
                    j = i - 9
                    while board.BOARD[j] == "-" and Board.index_2_coord(j)[0] > "a" and int(Board.index_2_coord(j)[1]) > 1:
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                        j -= 9
                    if board.BOARD[j] == "-":
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                    elif board.BOARD[j] != None and board.BOARD[j].color == piece.color * -1:
                        move = "Qx" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))

                # NW Diagonal
                if Board.index_2_coord(i)[0] > "a":
                    j = i + 7
                    while board.BOARD[j] == "-" and Board.index_2_coord(j)[0] > "a" and int(Board.index_2_coord(j)[1]) < 8:
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                        j += 7
                    if board.BOARD[j] == "-":
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                    elif board.BOARD[j] != None and board.BOARD[j].color == piece.color * -1:
                        move = "Qx" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))

                # North
                j = i + 8
                while board.BOARD[j] == "-" and int(Board.index_2_coord(j)[1]) < 8:
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                    j += 8
                if board.BOARD[j] == "-":
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                elif board.BOARD[j] != None and board.BOARD[j].color == piece.color * -1:
                    move = "Qx" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))

                # South
                j = i - 8
                while board.BOARD[j] == "-" and int(Board.index_2_coord(j)[1]) > 1:
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                    j -= 8
                if board.BOARD[j] == "-":
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                elif board.BOARD[j] != None and board.BOARD[j].color == piece.color * -1:
                    move = "Qx" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))

                # West
                if Board.index_2_coord(i)[0] > "a":
                    j = i - 1
                    while board.BOARD[j] == "-" and Board.index_2_coord(j)[0] > "a":
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                        j -= 1
                    if board.BOARD[j] == "-":
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                    elif board.BOARD[j] != None and board.BOARD[j].color == piece.color * -1:
                        move = "Qx" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))

                # East
                if Board.index_2_coord(i)[0] < "h":
                    j = i + 1
                    while board.BOARD[j] == "-" and Board.index_2_coord(j)[0] < "h":
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                        j += 1
                    if board.BOARD[j] == "-":
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                    elif board.BOARD[j] != None and board.BOARD[j].color == piece.color * -1:
                        move = "Qx" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))

        return queen_moves

    # Return a list of all valid king moves in current board state
    def generate_king_moves(self, board):
        king_moves = []
        for i in range(64):
            piece = board.BOARD[i]
            if isinstance(piece, King) and piece.color == board.side_to_move:
                # N
                if board.BOARD[i + 8] == "-":
                    move = "K" + Board.index_2_coord(i + 8)
                    king_moves.append((move, i, i + 8))
                elif board.BOARD[i + 8] != None and board.BOARD[i + 8].color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i + 8)
                    king_moves.append((move, i, i + 8))
                
                # S
                if board.BOARD[i - 8] == "-":
                    move = "K" + Board.index_2_coord(i - 8)
                    king_moves.append((move, i, i - 8))
                elif board.BOARD[i - 8] != None and board.BOARD[i - 8].color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i - 8)
                    king_moves.append((move, i, i - 8))
                
                # W
                if Board.index_2_coord(i)[0] != "a" and board.BOARD[i - 1] == "-":
                    move = "K" + Board.index_2_coord(i - 1)
                    king_moves.append((move, i, i - 1))
                elif Board.index_2_coord(i)[0] != "a" and board.BOARD[i - 1] != None and board.BOARD[i - 1].color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i - 1)
                    king_moves.append((move, i, i - 1))

                # E
                if Board.index_2_coord(i)[0] != "h" and board.BOARD[i + 1] == "-":
                    move = "K" + Board.index_2_coord(i + 1)
                    king_moves.append((move, i, i + 1))
                elif Board.index_2_coord(i)[0] != "h" and board.BOARD[i + 1] != None and board.BOARD[i + 1].color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i + 1)
                    king_moves.append((move, i, i + 1))

                # NW
                if Board.index_2_coord(i)[0] != "a" and int(Board.index_2_coord(i)[1]) != 8 and board.BOARD[i + 7] == "-":
                    move = "K" + Board.index_2_coord(i + 7)
                    king_moves.append((move, i, i + 7))
                elif Board.index_2_coord(i)[0] != "a" and int(Board.index_2_coord(i)[1]) != 8 and board.BOARD[i + 7] != None and board.BOARD[i + 7].color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i + 7)
                    king_moves.append((move, i, i + 7))

                # NE
                if Board.index_2_coord(i)[0] != "h" and int(Board.index_2_coord(i)[1]) != 8 and board.BOARD[i + 9] == "-":
                    move = "K" + Board.index_2_coord(i + 9)
                    king_moves.append((move, i, i + 9))
                elif Board.index_2_coord(i)[0] != "h" and int(Board.index_2_coord(i)[1]) != 8 and board.BOARD[i + 9] != None and board.BOARD[i + 9].color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i + 9)
                    king_moves.append((move, i, i + 9))

                # SW
                if Board.index_2_coord(i)[0] != "a" and int(Board.index_2_coord(i)[1]) != 1 and board.BOARD[i - 9] == "-":
                    move = "K" + Board.index_2_coord(i - 9)
                    king_moves.append((move, i, i - 9))
                elif Board.index_2_coord(i)[0] != "a" and int(Board.index_2_coord(i)[1]) != 1 and board.BOARD[i - 9] != None and board.BOARD[i - 9].color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i - 9)
                    king_moves.append((move, i, i - 9))

                # SE
                if Board.index_2_coord(i)[0] != "h" and int(Board.index_2_coord(i)[1]) != 1 and board.BOARD[i - 7] == "-":
                    move = "K" + Board.index_2_coord(i - 7)
                    king_moves.append((move, i, i - 7))
                elif Board.index_2_coord(i)[0] != "h" and int(Board.index_2_coord(i)[1]) != 1 and board.BOARD[i - 7] != None and board.BOARD[i - 7].color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i - 7)
                    king_moves.append((move, i, i - 7))
        return king_moves

    # Return a list of all valid rook moves in current board state
    def generate_rook_moves(self, board):
        rook_moves = []
        for i in range(64):
            piece = board.BOARD[i]
            if isinstance(piece, Rook) and piece.color == board.side_to_move:
                # North
                j = i + 8
                while board.BOARD[j] == "-" and int(Board.index_2_coord(j)[1]) < 8:
                    move = "R" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))
                    j += 8
                if board.BOARD[j] == "-":
                    move = "R" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))
                elif board.BOARD[j] != None and board.BOARD[j].color == piece.color * -1:
                    move = "Rx" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))

                # South
                j = i - 8
                while board.BOARD[j] == "-" and int(Board.index_2_coord(j)[1]) > 1:
                    move = "R" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))
                    j -= 8
                if board.BOARD[j] == "-":
                    move = "R" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))
                elif board.BOARD[j] != None and board.BOARD[j].color == piece.color * -1:
                    move = "Rx" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))

                # West
                if Board.index_2_coord(i)[0] > "a":
                    j = i - 1
                    while board.BOARD[j] == "-" and Board.index_2_coord(j)[0] > "a":
                        move = "R" + Board.index_2_coord(j)
                        rook_moves.append((move, i, j))
                        j -= 1
                    if board.BOARD[j] == "-":
                        move = "R" + Board.index_2_coord(j)
                        rook_moves.append((move, i, j))
                    elif board.BOARD[j] != None and board.BOARD[j].color == piece.color * -1:
                        move = "Rx" + Board.index_2_coord(j)
                        rook_moves.append((move, i, j))

                # East
                if Board.index_2_coord(i)[0] < "h":
                    j = i + 1
                    while board.BOARD[j] == "-" and Board.index_2_coord(j)[0] < "h":
                        move = "R" + Board.index_2_coord(j)
                        rook_moves.append((move, i, j))
                        j += 1
                    if board.BOARD[j] == "-":
                        move = "R" + Board.index_2_coord(j)
                        rook_moves.append((move, i, j))
                    elif board.BOARD[j] != None and board.BOARD[j].color == piece.color * -1:
                        move = "Rx" + Board.index_2_coord(j)
                        rook_moves.append((move, i, j))

        return rook_moves

    # Return a list of all valid castling moves in current board state
    def generate_castle_moves(self, board):
        castle_moves = []
        # White
        if board.side_to_move == 1:
            if board.white_can_castle_kingside and board.get_coord("f1") == "-" and board.get_coord("g1") == "-":
                castle_moves.append(("O-O", 4, 6))
            if board.white_can_castle_queenside and board.get_coord("b1") == "-" and board.get_coord("c1") == "-" and board.get_coord("d1") == "-":
                castle_moves.append(("O-O-O", 4, 2))
        else: # Black
            if board.black_can_castle_kingside and board.get_coord("f8") == "-" and board.get_coord("g8") == "-":
                castle_moves.append(("O-O", 60, 62))
            if board.black_can_castle_queenside and board.get_coord("b8") == "-" and board.get_coord("c8") == "-" and board.get_coord("d8") == "-":
                castle_moves.append(("O-O-O", 60, 58))

        return castle_moves

    def filter_legal_moves(self, move_list, board):
        legal_moves = []

        for move_tuple in move_list:
            if move_tuple[0] == "O-O":
                if board.side_to_move == 1: # White
                    variation_board = Board(None, board)
                    legal = not variation_board.check_for_checks(board.side_to_move)
                    variation_board.move(("", 4, 5))
                    legal = legal and not variation_board.check_for_checks(board.side_to_move)
                    variation_board = Board(None, board)
                    variation_board.move(move_tuple)
                    legal = legal and not variation_board.check_for_checks(board.side_to_move)
                    if legal:
                        legal_moves.append(move_tuple)

                else: # Black
                    variation_board = Board(None, board)
                    legal = not variation_board.check_for_checks(board.side_to_move)
                    variation_board.move(("", 60, 61))
                    legal = legal and not variation_board.check_for_checks(board.side_to_move)
                    variation_board = Board(None, board)
                    variation_board.move(move_tuple)
                    legal = legal and not variation_board.check_for_checks(board.side_to_move)
                    if legal:
                        legal_moves.append(move_tuple)
            elif move_tuple[0] == "O-O-O":
                if board.side_to_move == 1: # White
                    variation_board = Board(None, board)
                    legal = not variation_board.check_for_checks(board.side_to_move)
                    variation_board.move(("", 4, 3))
                    legal = legal and not variation_board.check_for_checks(board.side_to_move)
                    variation_board = Board(None, board)
                    variation_board.move(move_tuple)
                    legal = legal and not variation_board.check_for_checks(board.side_to_move)
                    if legal:
                        legal_moves.append(move_tuple)

                else: # Black
                    variation_board = Board(None, board)
                    legal = not variation_board.check_for_checks(board.side_to_move)
                    variation_board.move(("", 60, 59))
                    legal = legal and not variation_board.check_for_checks(board.side_to_move)
                    variation_board = Board(None, board)
                    variation_board.move(move_tuple)
                    legal = legal and not variation_board.check_for_checks(board.side_to_move)
                    if legal:
                        legal_moves.append(move_tuple)

            else:
                variation_board = Board(None, board)
                variation_board.move(move_tuple)
                # print(variation_board)

                legal = not variation_board.check_for_checks(board.side_to_move)
                # print(legal)
                if legal:
                    legal_moves.append(move_tuple)

        return legal_moves

    # Make a random legal move on the current board
    def make_random_move(self, board):
        move = random.choice(self.generate_legal_moves(board))
        board.move(move)
        self.move_log.append(move[0])



    # Compute an objective evalutation of the strength of the position relative to the side to move
    def evaluate(self, board):
        
        # Material points
        material_factor = self.calculate_material_factor(board)
        # print("Material Factor: " + str(material_factor))

        # TODO: Add Bishop Pair Bonus, Output Knight Bonus, Bad Bishops, Rook on Open File

        # Piece Square Bonuses
        square_bonus_factor = self.calculate_square_bonuses(board)
        # print("Square Bonus Factor: " + str(square_bonus_factor))

        # Pawn Structure
        pawn_factor = self.calculate_pawn_factor(board)
        # print("Pawn Factor: " + str(pawn_factor))
        
        # Mobility
        mobility_factor = 0 if board.legal_moves == None else len(board.legal_moves) * 0.8 * board.side_to_move
        # print("Mobility Factor: " + str(mobility_factor))

        # Tempo Bonus
        tempo_bonus = 20 * board.side_to_move

        # Check for checkmate / stalemate

        is_checkmate = self.is_it_checkmate(board)
        is_stalemate = self.is_it_stalemate(board)

        if is_checkmate:
            return -float("inf")
        if is_stalemate or board.threefold or board.half_move_count == 100:
            return 0.0
        
        return (material_factor + square_bonus_factor + pawn_factor + mobility_factor + tempo_bonus) * board.side_to_move / 100.0

    # Calculate a rudimentary material factor based off of basic piece centipawn values
    def calculate_material_factor(self, board):
        material_count = [0, 0, 0]
        white_bishops = 0
        black_bishops = 0
        for i in range(64):
            piece = board.BOARD[i]
            if isinstance(piece, Bishop):
                if piece.color == 1:
                    white_bishops += 1
                else:
                    black_bishops += 1
            if piece != None and piece != "-" and not isinstance(piece, King):
                material_count[piece.color] += piece.base_value
    
        material_factor = material_count[1] - material_count[-1]

        black_bishop_pair = 10 if black_bishops >= 2 else 0
        white_bishop_pair = 10 if white_bishops >= 2 else 0

        # print(white_bishop_pair - black_bishop_pair)

        material_factor += white_bishop_pair - black_bishop_pair

        return material_factor

    # Calculate square bonuses for each piece based off of piece maps in respective classes
    def calculate_square_bonuses(self, board):
        piece_square_bonuses = [0, 0, 0]
        endgame = board.is_endgame()
        for i in range(64):
            piece = board.BOARD[i]
            if piece != None and piece != "-":
                piece_square_bonuses[piece.color] += piece.get_bonus(i, endgame)

        square_bonus_factor = piece_square_bonuses[1] - piece_square_bonuses[-1]
        return square_bonus_factor

    # Calculate bonuses for good / bad pawn structures
    def calculate_pawn_factor(self, board):
        # Doubled pawns:
        doubled_pawns = [0, 0, 0]

        back_white_pawns = [0, 0, 0, 0, 0, 0, 0, 0]
        back_black_pawns = [0, 0, 0, 0, 0, 0, 0, 0]

        front_white_pawns = [0, 0, 0, 0, 0, 0, 0, 0]
        front_black_pawns = [0, 0, 0, 0, 0, 0, 0, 0]

        for i in range(8):
            white_pawns, black_pawns = 0, 0
            for j in range(8):
                index = i
                index += 8 * j

                if isinstance(board.BOARD[index], Pawn):
                    if board.BOARD[index].color == 1:
                        white_pawns += 1
                        if back_white_pawns[i] == 0:
                            back_white_pawns[i] = j + 1
                        front_white_pawns[i] = j + 1
                    else:
                        black_pawns += 1
                        if front_black_pawns[i] == 0:
                            front_black_pawns[i] = j + 1
                        back_black_pawns[i] = j + 1
                
            doubled_pawns[1] -= (max(0, white_pawns - 1)) * 50
            doubled_pawns[-1] -= (max(0, black_pawns - 1)) * 50
            # print(doubled_pawns)
        doubled_pawns_factor = doubled_pawns[1] - doubled_pawns[-1]
        
        # Backward Pawns
        white_backward_pawns = 0
        black_backward_pawns = 0
        for n in range(1, 7):
            if back_white_pawns[n] != 0 and back_white_pawns[n] < back_white_pawns[n - 1] and back_white_pawns[n] < back_white_pawns[n + 1]:
                white_backward_pawns += 1
            if back_black_pawns[n] > back_black_pawns[n - 1] and back_black_pawns[n] > back_black_pawns[n + 1]:
                black_backward_pawns += 1

        backward_pawn_factor = (white_backward_pawns - black_backward_pawns) * -30

        # Passed Pawns
        white_passed_pawns = 0
        black_passed_pawns = 0
        for n in range(1, 7):
            if front_white_pawns[n] >= back_black_pawns[n - 1] and front_white_pawns[n] >= back_black_pawns[n + 1] and front_white_pawns[n] >= back_black_pawns[n]:
                white_passed_pawns += 1
            if front_black_pawns[n] != 0 and (front_black_pawns[n] <= back_white_pawns[n - 1] or back_white_pawns[n - 1] == 0 ) and (front_black_pawns[n] <= back_white_pawns[n + 1] or back_white_pawns[n + 1] == 0) and (front_black_pawns[n] <= back_white_pawns[n] or back_white_pawns[n] == 0):
                black_passed_pawns += 1
        if front_white_pawns[0] >= back_black_pawns[1] and front_white_pawns[0] >= back_black_pawns[0] and front_white_pawns[0] != 0:
            white_passed_pawns += 1
        if front_white_pawns[7] >= back_black_pawns[6] and front_white_pawns[7] >= back_black_pawns[7] and front_white_pawns[7] != 0:
            white_passed_pawns += 1
        if (front_black_pawns[0] <= back_white_pawns[1] or back_white_pawns[1] == 0) and (back_white_pawns[0] == 0 or front_black_pawns[0] <= back_white_pawns[0]) and front_black_pawns[0] != 0:
            black_passed_pawns += 1
        if (front_black_pawns[7] <= back_white_pawns[6] or back_white_pawns[6] == 0) and (front_black_pawns[7] <= back_white_pawns[7] or back_white_pawns[7] == 0) and front_black_pawns[7] != 0:
            black_passed_pawns += 1

        # print(front_black_pawns, back_white_pawns)
        passed_pawn_factor = (white_passed_pawns - black_passed_pawns) * 30

        # Pawn Islands
        white_island, black_island = False, False
        white_pawn_islands = 0
        black_pawn_islands = 0

        front_white_pawns.append(0)
        front_black_pawns.append(0)
        for i in range(9):
            if front_white_pawns[i] == 0 and white_island == True:
                white_pawn_islands += 1
                white_island = False
            if front_white_pawns[i] > 0:
                white_island = True

            if front_black_pawns[i] == 0 and black_island == True:
                black_pawn_islands += 1
                black_island = False
            if front_black_pawns[i] > 0:
                black_island = True
            

        # print(white_pawn_islands, black_pawn_islands)
        pawn_island_factor = (white_pawn_islands - black_pawn_islands) * -10 if black_pawn_islands != 0 else 0

        # print(backward_pawn_factor, passed_pawn_factor, doubled_pawns_factor, pawn_island_factor)

        pawn_factor = backward_pawn_factor + doubled_pawns_factor + passed_pawn_factor + pawn_island_factor
        return pawn_factor        

    # Check if the current board position is a checkmate
    def is_it_checkmate(self, board):
        legal_moves = board.legal_moves if board.legal_moves != None else self.generate_legal_moves(board)
        if len(legal_moves) == 0 and board.check_for_checks(board.side_to_move):
            return True
        return False
    
    # Check if the current board position is a stalemate
    def is_it_stalemate(self, board):
        legal_moves = board.legal_moves if board.legal_moves != None else self.generate_legal_moves(board)
        if len(legal_moves) == 0 and not board.check_for_checks(board.side_to_move):
            return True
        return False

    # Determine if the game is over or not
    def is_it_over(self, board):
        return self.is_it_checkmate(board) or self.is_it_stalemate(board) or self.official_board.threefold or self.official_board.half_move_count == 100

    # Initial search algorithm, a form of minimax
    def negamax(self, board, depth=3, first=True):
        if depth == 0:
            return self.evaluate(board)
        if self.is_it_stalemate(board) or board.threefold or board.half_move_count == 100:
            return 0.0
        max_val = -float("inf")
        move_list = board.legal_moves if board.legal_moves != None else self.generate_legal_moves(board)
        best_move = move_list[0][0] if len(move_list) > 0 else None
        for move_tuple in move_list:
            self.current_node_count += 1
            variation_board = Board(None, board)
            variation_board.move(move_tuple)
            variation_board.legal_moves = self.generate_legal_moves(variation_board)
            score = -self.negamax(variation_board, depth - 1, False)
            if score >= max_val: # Can add some element of randomness here!
                max_val = score
                best_move = move_tuple

        return (max_val, best_move) if first else max_val

    # The wrapper function for negamax
    def search(self, board, final_depth):
        depth = 1
        max_val = -float("inf")
        while depth <= final_depth:
            val, move = self.negamax(board, depth)
            if val == float("inf") or depth == final_depth:
                max_val = val
                best_move = move
            if max_val == float("inf"):
                return max_val, best_move
            depth += 1
        return max_val, best_move

    # Current search algorithm
    def alpha_beta_search(self, board, final_depth, quiescence_depth=4, book=True, tablebases=True):
        if board.full_move_count <= Engine.NUM_BOOK_MOVES and book:
            too_soon = not self.just_booked and (time.time() - self.last_book_try < 60 and self.last_book_try != 0)
            if not too_soon:
                self.just_booked = True
                try:
                    # print("Probing book...")
                    move = self.book_move(board)
                    if move != None:
                        # print("Found a move")
                        return move
                except:
                    self.last_book_try = time.time()
                    print("Opening Book Failed! (either too many requests or poor internet connection)")
                    self.just_booked = False
                    return self.alpha_beta(board, -float("inf"), float("inf"), final_depth, quiescence_depth)
        if tablebases:
            if board.syzygy or board.syzygy_time():
                # print("just syzygied")
                too_soon = (not self.just_syzygied and (time.time() - self.last_table_try < 60 and self.last_table_try != 0))
                if not too_soon:
                    self.just_syzygied = True
                    try:
                        # print("Probing Syzygy Tablebases...")
                        return (None, self.syzygy_move(board))
                    except:
                        self.last_table_try = time.time()
                        print("Syzygy Failed! (either too many requests or poor internet connection)")
                        self.just_syzygied = False
                        return self.alpha_beta(board, -float("inf"), float("inf"), final_depth, quiescence_depth)
        self.just_syzygied = False
        self.just_booked = False
        return self.alpha_beta(board, -float("inf"), float("inf"), final_depth, quiescence_depth)

    # Execute a move on the official board and update the move log
    def move(self, move_tuple):
        self.official_board.move(move_tuple)
        self.official_board.legal_moves = self.generate_legal_moves(self.official_board)
        self.move_log.append(move_tuple[0])
        if self.official_board.threefold:
            self.move_log.append("Draw by Threefold Repetition")
        elif self.official_board.half_move_count == 100:
            self.move_log.append("Draw by 50 Move Rule")
        elif self.is_it_checkmate(self.official_board):
            self.move_log.append("Checkmate")
        elif self.is_it_stalemate(self.official_board):
            self.move_log.append("Stalemate")

    # Interface for GUI move
    def gui_move(self, move_duple):
        possible_moves = self.official_board.legal_moves if self.official_board.legal_moves != None else self.generate_legal_moves(self.official_board)
        for move_tuple in possible_moves:
            if move_tuple[1] == move_duple[0] and move_tuple[2] == move_duple[1]:
                if "=R" not in move_tuple[0] and "=B" not in move_tuple[0] and "=N" not in move_tuple[0]:
                    self.move(move_tuple)

    # Return the pgn of the game to the current point (although still not 100% correct)
    def get_pgn(self):
        pgn = ""
        count = 2
        for move in self.move_log:
            if "Draw" in move:
                pgn += move
                break
            else:
                if count % 2 == 0:
                    pgn += str(int(count / 2)) + ". "
                pgn += move + " "
                count += 1
        return pgn

    # Quiescent search for alpha beta minimax
    def quiesce(self, board, alpha, beta, depth):
        self.current_node_count += 1
        stand_pat = self.evaluate(board)

        # if depth == 0: # Correct???
        #     return stand_pat

        if stand_pat >= beta:
            return beta

        delta = 975 # As opposed to 200

        if stand_pat < alpha - delta:
            return alpha

        if alpha < stand_pat:
            alpha = stand_pat

        move_list = board.legal_moves if board.legal_moves != None else self.generate_legal_moves(board)
        move_list = self.mvv_lva(move_list, board)
        for move_tuple in move_list:
            if "x" in move_tuple[0]:
                variation_board = Board(None, board)
                variation_board.move(move_tuple)
                variation_board.legal_moves = self.generate_legal_moves(variation_board)
                score = -self.quiesce(variation_board, -beta, -alpha, depth - 1)

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
        
        return alpha

    # Alpha beta pruning minimax search algorithm
    def alpha_beta(self, board, alpha, beta, depth_left, quiescence_depth, first=True):
        key = (board.zobrist(), board.side_to_move)
        if self.transposition_table.get(key, None) != None and self.transposition_table[key][2] >= depth_left and self.transposition_table[key][1] != None:
            variation_board = Board(None, board)
            variation_board.move(self.transposition_table[key][1])
            self.current_node_count += 1
            if not variation_board.twofold and variation_board.half_move_count != 100:
                return self.transposition_table[key][:2] if first else self.transposition_table[key][0]

        if depth_left == 0:
            return self.quiesce(board, alpha, beta, quiescence_depth) # !!!!!
        if self.is_it_stalemate(board) or board.threefold or board.half_move_count == 100:
            return 0.0
        move_list = board.legal_moves if board.legal_moves != None else self.generate_legal_moves(board)
        move_list = self.mvv_lva(move_list, board)
        best_move = move_list[0] if len(move_list) > 0 else None
        if self.transposition_table.get(key, None) != None:
            for i in range(len(move_list)):
                if move_list[i] == self.transposition_table[key][1]:
                    # print("Hi")
                    move_list.insert(0, move_list.pop(i))
        for move_tuple in move_list:
            variation_board = Board(None, board)
            variation_board.move(move_tuple)
            self.current_node_count += 1
            variation_board.legal_moves = self.generate_legal_moves(variation_board)
            score = -self.alpha_beta(variation_board, -beta, -alpha, depth_left - 1, quiescence_depth, False)
            if score >= beta:
                best_move = move_tuple
                self.transposition_table[key] = (beta, best_move, depth_left)
                return (beta, move_tuple) if first else beta
            if score > alpha:
                best_move = move_tuple
                alpha = score

        self.transposition_table[key] = (alpha, best_move, depth_left)
        return (alpha, best_move) if first else alpha

    # Sorts moves based off of Most Valuable Victim - Least Valuable Aggressor Principle
    def mvv_lva(self, move_list, board):
        captures = [m for m in move_list if "x" in m[0] and len(m) != 4]
        noncaptures = [m for m in move_list if "x" not in m[0] or len(m) == 4]
        captures.sort(key=lambda m: (-Engine.piece_values[board.BOARD[m[2]].id], Engine.piece_values[board.BOARD[m[1]].id]))
        captures.extend(noncaptures)
        return captures

    def syzygy_move(self, board):
        # print("syzygied")
        base_url = "https://tablebase.lichess.ovh/standard?fen="
        url = base_url + board.fen().replace(" ", "_")
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()
        contents = mybytes.decode("utf8")
        fp.close()

        move = contents.split("\"")[25]

        # print(move)

        sq1 = Board.coord_to_index[move[:2]]
        sq2 = Board.coord_to_index[move[2:4]]
        promote_to = None
        if len(move) == 5:
            promote_to = move[4].upper()

        possible_moves = self.generate_legal_moves(board)
        if promote_to != None:
            for move_tuple in possible_moves:
                if move_tuple[1] == sq1 and move_tuple[2] == sq2 and ("=" + promote_to) in move_tuple[0]:
                    return move_tuple
        else:
            for move_tuple in possible_moves:
                if move_tuple[1] == sq1 and move_tuple[2] == sq2:
                    return move_tuple

    # Probes the Lichess Opening Explorer database and chooses one of the top 4 moves
    def book_move(self, board):
        base_url = "https://explorer.lichess.ovh/masters?fen="
        url = base_url + board.fen().replace(" ", "_") + "&moves=4&topGames=0"
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()
        contents = mybytes.decode("utf8")
        fp.close()

        temp = contents.split("{")
        contents = []
        for i in range(len(temp)):
            if "id" not in temp[i] and "name" not in temp[i]:
                contents.append(temp[i])
            
        total_position_info = contents[1]
        if len(contents) >= 6:
            move1_info = contents[2]
            move2_info = contents[3]
            move3_info = contents[4]
            move4_info = contents[5]

            move1_info = move1_info.split("\"")
            move1 = move1_info[3]
            move1_name = move1_info[7]
            move1_white = int(move1_info[12][1:-1])
            move1_draw = int(move1_info[14][1:-1])
            move1_black = int(move1_info[16][1:-1])
            move1_games = move1_white + move1_draw + move1_black

            move2_info = move2_info.split("\"")
            move2 = move2_info[3]
            move2_name = move2_info[7]
            move2_white = int(move2_info[12][1:-1])
            move2_draw = int(move2_info[14][1:-1])
            move2_black = int(move2_info[16][1:-1])
            move2_games = move2_white + move2_draw + move2_black

            move3_info = move3_info.split("\"")
            move3 = move3_info[3]
            move3_name = move3_info[7]
            move3_white = int(move3_info[12][1:-1])
            move3_draw = int(move3_info[14][1:-1])
            move3_black = int(move3_info[16][1:-1])
            move3_games = move3_white + move3_draw + move3_black

            move4_info = move4_info.split("\"")
            move4 = move4_info[3]
            move4_name = move4_info[7]
            move4_white = int(move4_info[12][1:-1])
            move4_draw = int(move4_info[14][1:-1])
            move4_black = int(move4_info[16][1:-1])
            move4_games = move4_white + move4_draw + move4_black

            total_games = move1_games + move2_games + move3_games + move4_games

            move1_ratio = move1_games / total_games
            move2_ratio = move2_games / total_games
            move3_ratio = move3_games / total_games
            move4_ratio = move4_games / total_games

            rand_decimal = random.random()

            if rand_decimal < move1_ratio:
                move = move1
                move_name = move1_name
            elif rand_decimal < move1_ratio + move2_ratio:
                move = move2
                move_name = move2_name
            elif rand_decimal < move1_ratio + move2_ratio + move3_ratio:
                move = move3
                move_name = move3_name
            else:
                move = move4
                move_name = move4_name
        elif len(contents) == 5:
            move1_info = contents[2]
            move2_info = contents[3]
            move3_info = contents[4]

            move1_info = move1_info.split("\"")
            move1 = move1_info[3]
            move1_name = move1_info[7]
            move1_white = int(move1_info[12][1:-1])
            move1_draw = int(move1_info[14][1:-1])
            move1_black = int(move1_info[16][1:-1])
            move1_games = move1_white + move1_draw + move1_black

            move2_info = move2_info.split("\"")
            move2 = move2_info[3]
            move2_name = move2_info[7]
            move2_white = int(move2_info[12][1:-1])
            move2_draw = int(move2_info[14][1:-1])
            move2_black = int(move2_info[16][1:-1])
            move2_games = move2_white + move2_draw + move2_black

            move3_info = move3_info.split("\"")
            move3 = move3_info[3]
            move3_name = move3_info[7]
            move3_white = int(move3_info[12][1:-1])
            move3_draw = int(move3_info[14][1:-1])
            move3_black = int(move3_info[16][1:-1])
            move3_games = move3_white + move3_draw + move3_black

            total_games = move1_games + move2_games + move3_games

            move1_ratio = move1_games / total_games
            move2_ratio = move2_games / total_games
            move3_ratio = move3_games / total_games

            rand_decimal = random.random()

            if rand_decimal < move1_ratio:
                move = move1
                move_name = move1_name
            elif rand_decimal < move1_ratio + move2_ratio:
                move = move2
                move_name = move2_name
            else:
                move = move3
                move_name = move3_name
        elif len(contents) == 4:
            move1_info = contents[2]
            move2_info = contents[3]

            move1_info = move1_info.split("\"")
            move1 = move1_info[3]
            move1_name = move1_info[7]
            move1_white = int(move1_info[12][1:-1])
            move1_draw = int(move1_info[14][1:-1])
            move1_black = int(move1_info[16][1:-1])
            move1_games = move1_white + move1_draw + move1_black

            move2_info = move2_info.split("\"")
            move2 = move2_info[3]
            move2_name = move2_info[7]
            move2_white = int(move2_info[12][1:-1])
            move2_draw = int(move2_info[14][1:-1])
            move2_black = int(move2_info[16][1:-1])
            move2_games = move2_white + move2_draw + move2_black

            total_games = move1_games + move2_games

            move1_ratio = move1_games / total_games
            move2_ratio = move2_games / total_games

            rand_decimal = random.random()

            if rand_decimal < move1_ratio:
                move = move1
                move_name = move1_name
            else:
                move = move2
                move_name = move2_name
        elif len(contents) == 3:
            move1_info = contents[2]

            move1_info = move1_info.split("\"")
            move1 = move1_info[3]
            move1_name = move1_info[7]
            move1_white = int(move1_info[12][1:-1])
            move1_draw = int(move1_info[14][1:-1])
            move1_black = int(move1_info[16][1:-1])
            move1_games = move1_white + move1_draw + move1_black

            total_games = move1_games

            move1_ratio = move1_games / total_games

            rand_decimal = random.random()

            if rand_decimal < move1_ratio:
                move = move1
                move_name = move1_name
            else:
                move = None
        else:
            return None
        
        if move_name == "O-O" and board.side_to_move == 1:
            move = "e1g1"
        elif move_name == "O-O" and board.side_to_move == -1:
            move = "e8g8"
        elif move_name == "O-O-O" and board.side_to_move == 1:
            move = "e1c1"
        elif move_name == "O-O-O" and board.side_to_move == -1:
            move = "e8c8"

        # print(move)

        sq1 = Board.coord_to_index[move[:2]]
        sq2 = Board.coord_to_index[move[2:4]]
        promote_to = None
        if len(move) == 5:
            promote_to = move[4].upper()

        possible_moves = self.generate_legal_moves(board)
        if promote_to != None:
            for move_tuple in possible_moves:
                if move_tuple[1] == sq1 and move_tuple[2] == sq2 and ("=" + promote_to) in move_tuple[0]:
                    # print(move_tuple)
                    return (None, move_tuple)
        else:
            for move_tuple in possible_moves:
                if move_tuple[1] == sq1 and move_tuple[2] == sq2:
                    # print(move_tuple)
                    return (None, move_tuple)