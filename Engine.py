from Board import *
from Rook import *
from Queen import *
from Knight import *
from Bishop import *
from King import *
from Pawn import *
import random

class Engine:

    startingFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def __init__(self, fen = startingFEN, board = None):
        if board == None:
            self.official_board = Board(fen)
        else:
            self.official_board = Board(None, board)
        self.move_log = []
    
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
        return [x[0] for x in self.generate_legal_moves(board)]

    #TODO: incoroprate piece lists so no need to loop through entire board each time

    # Return a list of all valid pawn moves (including en passant) in current board state
    def generate_pawn_moves(self, board):
        pawn_moves = []
        for i in range(64):
            piece = board.get(i)
            if isinstance(piece, Pawn) and piece.color == board.side_to_move:
                # 1 Square Ahead
                if board.get(i + 8 * piece.color) == "-":
                    move = Board.index_2_coord(i + 8 * piece.color)
                    # Promotion
                    if (int(Board.index_2_coord(i)[1]) == 7 and piece.color == 1) or (int(Board.index_2_coord(i)[1]) == 2 and piece.color == -1):
                        pawn_moves.append((Board.index_2_coord(i + 8 * piece.color) + "=Q", i, i + 8 * piece.color))
                        pawn_moves.append((Board.index_2_coord(i + 8 * piece.color) + "=R", i, i + 8 * piece.color))
                        pawn_moves.append((Board.index_2_coord(i + 8 * piece.color) + "=B", i, i + 8 * piece.color))
                        pawn_moves.append((Board.index_2_coord(i + 8 * piece.color) + "=N", i, i + 8 * piece.color))
                    else:
                        pawn_moves.append((move, i, i + 8 * piece.color))

                # 2 Squares Ahead
                if (((Board.index_2_coord(i)[1] == "2" and piece.color == 1)
                 or (Board.index_2_coord(i)[1] == "7" and piece.color == -1)) 
                 and board.get(i + 8 * piece.color) == "-" 
                 and board.get(i + 16 * piece.color) == "-"):
                    move = Board.index_2_coord(i + 16 * piece.color)
                    pawn_moves.append((move, i, i + 16 * piece.color, None, i + 8 * piece.color))

                # Diagonal Captures
                if (board.get(i + 7 * piece.color) != None and board.get(i + 7 * piece.color) != "-") and board.get(i + 7 * piece.color).color == piece.color * -1:
                    if not((Board.index_2_coord(i)[0] == "a" and piece.color == 1) or (Board.index_2_coord(i)[0] == "h" and piece.color == -1)):
                        move = Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 7 * piece.color)
                        # Promotion
                        if (int(Board.index_2_coord(i)[1]) == 7 and piece.color == 1) or (int(Board.index_2_coord(i)[1]) == 2 and piece.color == -1):
                            pawn_moves.append((Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 7 * piece.color) + "=Q", i, i + 7 * piece.color))
                            pawn_moves.append((Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 7 * piece.color) + "=R", i, i + 7 * piece.color))
                            pawn_moves.append((Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 7 * piece.color) + "=B", i, i + 7 * piece.color))
                            pawn_moves.append((Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 7 * piece.color) + "=N", i, i + 7 * piece.color))
                        else:
                            pawn_moves.append((move, i, i + 7 * piece.color))

                if (board.get(i + 9 * piece.color) != None and board.get(i + 9 * piece.color) != "-") and board.get(i + 9 * piece.color).color == piece.color * -1:
                    if not((Board.index_2_coord(i)[0] == "h" and piece.color == 1) or (Board.index_2_coord(i)[0] == "a" and piece.color == -1)):
                        move = Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 9 * piece.color)
                        # Promotion
                        if (int(Board.index_2_coord(i)[1]) == 7 and piece.color == 1) or (int(Board.index_2_coord(i)[1]) == 2 and piece.color == -1):
                            pawn_moves.append((Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 9 * piece.color) + "=Q", i, i + 9 * piece.color))
                            pawn_moves.append((Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 9 * piece.color) + "=R", i, i + 9 * piece.color))
                            pawn_moves.append((Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 9 * piece.color) + "=B", i, i + 9 * piece.color))
                            pawn_moves.append((Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 9 * piece.color) + "=N", i, i + 9 * piece.color))
                        else:
                            pawn_moves.append((move, i, i + 9 * piece.color))

                # En Passant
                if (board.get(i + 7 * piece.color) != None and Board.index_2_coord(i + 7 * piece.color) == board.en_passant_square):
                    if not((Board.index_2_coord(i)[0] == "a" and piece.color == 1) or (Board.index_2_coord(i)[0] == "h" and piece.color == -1)):
                        move = Board.index_2_coord(i)[0] + "x" + board.en_passant_square
                        pawn_moves.append((move, i, i + 7 * piece.color, i - 1))

                if (board.get(i + 9 * piece.color) != None and Board.index_2_coord(i + 9 * piece.color) == board.en_passant_square):
                    if not((Board.index_2_coord(i)[0] == "h" and piece.color == 1) or (Board.index_2_coord(i)[0] == "a" and piece.color == -1)):
                        move = Board.index_2_coord(i)[0] + "x" + board.en_passant_square
                        pawn_moves.append((move, i, i + 9 * piece.color, i + 1))

        return pawn_moves

    # Return a list of all valid knight moves in current board state
    def generate_knight_moves(self, board):
        knight_moves = []
        for i in range(64):
            piece = board.get(i)
            if isinstance(piece, Knight) and piece.color == board.side_to_move:
                # NE Squares
                if int(Board.index_2_coord(i)[1]) < 7 and Board.index_2_coord(i)[0] != "h":
                    if board.get(i + 17) == "-":
                        move = "N" + Board.index_2_coord(i + 17)
                        knight_moves.append((move, i, i + 17))
                    elif board.get(i + 17).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i + 17)
                        knight_moves.append((move, i, i + 17))
                    
                if int(Board.index_2_coord(i)[1]) < 8 and Board.index_2_coord(i)[0] < "g":
                    if board.get(i + 10) == "-":
                        move = "N" + Board.index_2_coord(i + 10)
                        knight_moves.append((move, i, i + 10))
                    elif board.get(i + 10).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i + 10)
                        knight_moves.append((move, i, i + 10))

                # SE Squares
                if int(Board.index_2_coord(i)[1]) > 1 and Board.index_2_coord(i)[0] < "g":
                    if board.get(i - 6) == "-":
                        move = "N" + Board.index_2_coord(i - 6)
                        knight_moves.append((move, i, i - 6))
                    elif board.get(i - 6).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i - 6)
                        knight_moves.append((move, i, i - 6))
                    
                if int(Board.index_2_coord(i)[1]) > 2 and Board.index_2_coord(i)[0] < "h":
                    if board.get(i - 15) == "-":
                        move = "N" + Board.index_2_coord(i - 15)
                        knight_moves.append((move, i, i - 15))
                    elif board.get(i - 15).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i - 15)
                        knight_moves.append((move, i, i - 15))
                            
                # SW Squares
                if int(Board.index_2_coord(i)[1]) > 2 and Board.index_2_coord(i)[0] > "a":
                    if board.get(i - 17) == "-":
                        move = "N" + Board.index_2_coord(i - 17)
                        knight_moves.append((move, i, i - 17))
                    elif board.get(i - 17).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i - 17)
                        knight_moves.append((move, i, i - 17))
                    
                if int(Board.index_2_coord(i)[1]) > 1 and Board.index_2_coord(i)[0] > "b":
                    if board.get(i - 10) == "-":
                        move = "N" + Board.index_2_coord(i - 10)
                        knight_moves.append((move, i, i - 10))
                    elif board.get(i - 10).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i - 10)
                        knight_moves.append((move, i, i - 10))

                # NW Squares
                if int(Board.index_2_coord(i)[1]) < 8 and Board.index_2_coord(i)[0] > "b":
                    if board.get(i + 6) == "-":
                        move = "N" + Board.index_2_coord(i + 6)
                        knight_moves.append((move, i, i + 6))
                    elif board.get(i + 6).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i + 6)
                        knight_moves.append((move, i, i + 6))
                    
                if int(Board.index_2_coord(i)[1]) < 7 and Board.index_2_coord(i)[0] > "a":
                    if board.get(i + 15) == "-":
                        move = "N" + Board.index_2_coord(i + 15)
                        knight_moves.append((move, i, i + 15))
                    elif board.get(i + 15).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i + 15)
                        knight_moves.append((move, i, i + 15))
        return knight_moves
                        
    # Return a list of all valid bishop moves in current board state
    def generate_bishop_moves(self, board):
        bishop_moves = []
        for i in range(64):
            piece = board.get(i)
            if isinstance(piece, Bishop) and piece.color == board.side_to_move:
                # NE Diagonal
                if Board.index_2_coord(i)[0] < "h":
                    j = i + 9
                    while board.get(j) == "-" and Board.index_2_coord(j)[0] < "h" and int(Board.index_2_coord(j)[1]) < 8:
                        move = "B" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))
                        j += 9
                    if board.get(j) == "-":
                        move = "B" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))
                    elif board.get(j) != None and board.get(j).color == piece.color * -1:
                        move = "Bx" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))

                # SE Diagonal
                if Board.index_2_coord(i)[0] < "h":
                    j = i - 7
                    while board.get(j) == "-" and Board.index_2_coord(j)[0] < "h" and int(Board.index_2_coord(j)[1]) > 1:
                        move = "B" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))
                        j -= 7
                    if board.get(j) == "-":
                        move = "B" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))
                    elif board.get(j) != None and board.get(j).color == piece.color * -1:
                        move = "Bx" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))

                # SW Diagonal
                if Board.index_2_coord(i)[0] > "a":
                    j = i - 9
                    while board.get(j) == "-" and Board.index_2_coord(j)[0] > "a" and int(Board.index_2_coord(j)[1]) > 1:
                        move = "B" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))
                        j -= 9
                    if board.get(j) == "-":
                        move = "B" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))
                    elif board.get(j) != None and board.get(j).color == piece.color * -1:
                        move = "Bx" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))

                # NW Diagonal
                if Board.index_2_coord(i)[0] > "a":
                    j = i + 7
                    while board.get(j) == "-" and Board.index_2_coord(j)[0] > "a" and int(Board.index_2_coord(j)[1]) < 8:
                        move = "B" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))
                        j += 7
                    if board.get(j) == "-":
                        move = "B" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))
                    elif board.get(j) != None and board.get(j).color == piece.color * -1:
                        move = "Bx" + Board.index_2_coord(j)
                        bishop_moves.append((move, i, j))

        return bishop_moves
    
    # Return a list of all valid queen moves in current board state
    def generate_queen_moves(self, board):
        queen_moves = []
        for i in range(64):
            piece = board.get(i)
            if isinstance(piece, Queen) and piece.color == board.side_to_move:
                # NE Diagonal
                if Board.index_2_coord(i)[0] < "h":
                    j = i + 9
                    while board.get(j) == "-" and Board.index_2_coord(j)[0] < "h" and int(Board.index_2_coord(j)[1]) < 8:
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                        j += 9
                    if board.get(j) == "-":
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                    elif board.get(j) != None and board.get(j).color == piece.color * -1:
                        move = "Qx" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))

                # SE Diagonal
                if Board.index_2_coord(i)[0] < "h":
                    j = i - 7
                    while board.get(j) == "-" and Board.index_2_coord(j)[0] < "h" and int(Board.index_2_coord(j)[1]) > 1:
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                        j -= 7
                    if board.get(j) == "-":
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                    elif board.get(j) != None and board.get(j).color == piece.color * -1:
                        move = "Qx" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))

                # SW Diagonal
                if Board.index_2_coord(i)[0] > "a":
                    j = i - 9
                    while board.get(j) == "-" and Board.index_2_coord(j)[0] > "a" and int(Board.index_2_coord(j)[1]) > 1:
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                        j -= 9
                    if board.get(j) == "-":
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                    elif board.get(j) != None and board.get(j).color == piece.color * -1:
                        move = "Qx" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))

                # NW Diagonal
                if Board.index_2_coord(i)[0] > "a":
                    j = i + 7
                    while board.get(j) == "-" and Board.index_2_coord(j)[0] > "a" and int(Board.index_2_coord(j)[1]) < 8:
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                        j += 7
                    if board.get(j) == "-":
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                    elif board.get(j) != None and board.get(j).color == piece.color * -1:
                        move = "Qx" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))

                # North
                j = i + 8
                while board.get(j) == "-" and int(Board.index_2_coord(j)[1]) < 8:
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                    j += 8
                if board.get(j) == "-":
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                elif board.get(j) != None and board.get(j).color == piece.color * -1:
                    move = "Qx" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))

                # South
                j = i - 8
                while board.get(j) == "-" and int(Board.index_2_coord(j)[1]) > 1:
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                    j -= 8
                if board.get(j) == "-":
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                elif board.get(j) != None and board.get(j).color == piece.color * -1:
                    move = "Qx" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))

                # West
                if Board.index_2_coord(i)[0] > "a":
                    j = i - 1
                    while board.get(j) == "-" and Board.index_2_coord(j)[0] > "a":
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                        j -= 1
                    if board.get(j) == "-":
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                    elif board.get(j) != None and board.get(j).color == piece.color * -1:
                        move = "Qx" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))

                # East
                if Board.index_2_coord(i)[0] < "h":
                    j = i + 1
                    while board.get(j) == "-" and Board.index_2_coord(j)[0] < "h":
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                        j += 1
                    if board.get(j) == "-":
                        move = "Q" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))
                    elif board.get(j) != None and board.get(j).color == piece.color * -1:
                        move = "Qx" + Board.index_2_coord(j)
                        queen_moves.append((move, i, j))

        return queen_moves

    # Return a list of all valid king moves in current board state
    def generate_king_moves(self, board):
        king_moves = []
        for i in range(64):
            piece = board.get(i)
            if isinstance(piece, King) and piece.color == board.side_to_move:
                # N
                if board.get(i + 8) == "-":
                    move = "K" + Board.index_2_coord(i + 8)
                    king_moves.append((move, i, i + 8))
                elif board.get(i + 8) != None and board.get(i + 8).color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i + 8)
                    king_moves.append((move, i, i + 8))
                
                # S
                if board.get(i - 8) == "-":
                    move = "K" + Board.index_2_coord(i - 8)
                    king_moves.append((move, i, i - 8))
                elif board.get(i - 8) != None and board.get(i - 8).color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i - 8)
                    king_moves.append((move, i, i - 8))
                
                # W
                if Board.index_2_coord(i)[0] != "a" and board.get(i - 1) == "-":
                    move = "K" + Board.index_2_coord(i - 1)
                    king_moves.append((move, i, i - 1))
                elif Board.index_2_coord(i)[0] != "a" and board.get(i - 1) != None and board.get(i - 1).color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i - 1)
                    king_moves.append((move, i, i - 1))

                # E
                if Board.index_2_coord(i)[0] != "h" and board.get(i + 1) == "-":
                    move = "K" + Board.index_2_coord(i + 1)
                    king_moves.append((move, i, i + 1))
                elif Board.index_2_coord(i)[0] != "h" and board.get(i + 1) != None and board.get(i + 1).color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i + 1)
                    king_moves.append((move, i, i + 1))

                # NW
                if Board.index_2_coord(i)[0] != "a" and int(Board.index_2_coord(i)[1]) != 8 and board.get(i + 7) == "-":
                    move = "K" + Board.index_2_coord(i + 7)
                    king_moves.append((move, i, i + 7))
                elif Board.index_2_coord(i)[0] != "a" and int(Board.index_2_coord(i)[1]) != 8 and board.get(i + 7) != None and board.get(i + 7).color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i + 7)
                    king_moves.append((move, i, i + 7))

                # NE
                if Board.index_2_coord(i)[0] != "h" and int(Board.index_2_coord(i)[1]) != 8 and board.get(i + 9) == "-":
                    move = "K" + Board.index_2_coord(i + 9)
                    king_moves.append((move, i, i + 9))
                elif Board.index_2_coord(i)[0] != "h" and int(Board.index_2_coord(i)[1]) != 8 and board.get(i + 9) != None and board.get(i + 9).color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i + 9)
                    king_moves.append((move, i, i + 9))

                # SW
                if Board.index_2_coord(i)[0] != "a" and int(Board.index_2_coord(i)[1]) != 1 and board.get(i - 9) == "-":
                    move = "K" + Board.index_2_coord(i - 9)
                    king_moves.append((move, i, i - 9))
                elif Board.index_2_coord(i)[0] != "a" and int(Board.index_2_coord(i)[1]) != 1 and board.get(i - 9) != None and board.get(i - 9).color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i - 9)
                    king_moves.append((move, i, i - 9))

                # SE
                if Board.index_2_coord(i)[0] != "h" and int(Board.index_2_coord(i)[1]) != 1 and board.get(i - 7) == "-":
                    move = "K" + Board.index_2_coord(i - 7)
                    king_moves.append((move, i, i - 7))
                elif Board.index_2_coord(i)[0] != "h" and int(Board.index_2_coord(i)[1]) != 1 and board.get(i - 7) != None and board.get(i - 7).color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i - 7)
                    king_moves.append((move, i, i - 7))
        return king_moves

    # Return a list of all valid rook moves in current board state
    def generate_rook_moves(self, board):
        rook_moves = []
        for i in range(64):
            piece = board.get(i)
            if isinstance(piece, Rook) and piece.color == board.side_to_move:
                # North
                j = i + 8
                while board.get(j) == "-" and int(Board.index_2_coord(j)[1]) < 8:
                    move = "R" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))
                    j += 8
                if board.get(j) == "-":
                    move = "R" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))
                elif board.get(j) != None and board.get(j).color == piece.color * -1:
                    move = "Rx" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))

                # South
                j = i - 8
                while board.get(j) == "-" and int(Board.index_2_coord(j)[1]) > 1:
                    move = "R" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))
                    j -= 8
                if board.get(j) == "-":
                    move = "R" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))
                elif board.get(j) != None and board.get(j).color == piece.color * -1:
                    move = "Rx" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))

                # West
                if Board.index_2_coord(i)[0] > "a":
                    j = i - 1
                    while board.get(j) == "-" and Board.index_2_coord(j)[0] > "a":
                        move = "R" + Board.index_2_coord(j)
                        rook_moves.append((move, i, j))
                        j -= 1
                    if board.get(j) == "-":
                        move = "R" + Board.index_2_coord(j)
                        rook_moves.append((move, i, j))
                    elif board.get(j) != None and board.get(j).color == piece.color * -1:
                        move = "Rx" + Board.index_2_coord(j)
                        rook_moves.append((move, i, j))

                # East
                if Board.index_2_coord(i)[0] < "h":
                    j = i + 1
                    while board.get(j) == "-" and Board.index_2_coord(j)[0] < "h":
                        move = "R" + Board.index_2_coord(j)
                        rook_moves.append((move, i, j))
                        j += 1
                    if board.get(j) == "-":
                        move = "R" + Board.index_2_coord(j)
                        rook_moves.append((move, i, j))
                    elif board.get(j) != None and board.get(j).color == piece.color * -1:
                        move = "Rx" + Board.index_2_coord(j)
                        rook_moves.append((move, i, j))

        return rook_moves

    # Return a list of all valid castling moves in current board state
    def generate_castle_moves(self, board):
        castle_moves = []
        # White
        if board.side_to_move == 1:
            if board.white_can_castle_kingside and board.get_coord("f1") == "-" and board.get_coord("g1") == "-":
                castle_moves.append(("O-O", None))
            if board.white_can_castle_queenside and board.get_coord("b1") == "-" and board.get_coord("c1") == "-" and board.get_coord("d1") == "-":
                castle_moves.append(("O-O-O", None))
        else: # Black
            if board.black_can_castle_kingside and board.get_coord("f8") == "-" and board.get_coord("g8") == "-":
                castle_moves.append(("O-O", None))
            if board.black_can_castle_queenside and board.get_coord("b8") == "-" and board.get_coord("c8") == "-" and board.get_coord("d8") == "-":
                castle_moves.append(("O-O-O", None))

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
        print("Material Factor: " + str(material_factor))

        # TODO: Add Bishop Pair Bonus, Output Knight Bonus, Bad Bishops, Rook on Open File

        # Piece Square Bonuses
        square_bonus_factor = self.calculate_square_bonuses(board)
        print("Square Bonus Factor: " + str(square_bonus_factor))

        # Pawn Structure
        pawn_factor = self.calculate_pawn_factor(board)
        print("Pawn Factor: " + str(pawn_factor))
        
        # Mobility
        mobility_factor = len(self.generate_legal_moves(board)) * 0.8 * board.side_to_move
        print("Mobility Factor: " + str(mobility_factor))

        # Tempo Bonus
        tempo_bonus = 0.2 * board.side_to_move

        # Check for checkmate / stalemate

        is_checkmate = self.is_it_checkmate(board)
        is_stalemate = self.is_it_stalemate(board)

        if is_checkmate:
            return -float("inf")
        if is_stalemate:
            return 0.0
        
        return (material_factor + square_bonus_factor + pawn_factor + mobility_factor + tempo_bonus) * board.side_to_move / 100.0

    def calculate_material_factor(self, board):
        material_count = [0, 0, 0]
        for i in range(64):
            piece = board.get(i)
            if piece != None and piece != "-" and not isinstance(piece, King):
                material_count[piece.color] += piece.base_value
    
        material_factor = material_count[1] - material_count[-1]
        return material_factor

    def calculate_square_bonuses(self, board):
        piece_square_bonuses = [0, 0, 0]
        endgame = board.is_endgame()
        for i in range(64):
            piece = board.get(i)
            if piece != None and piece != "-":
                piece_square_bonuses[piece.color] += piece.get_bonus(i, endgame)

        square_bonus_factor = piece_square_bonuses[1] - piece_square_bonuses[-1]
        return square_bonus_factor

    def calculate_pawn_factor(self, board):
        # Doubled pawns:
        doubled_pawns = [0, 0, 0]
        for i in range(8):
            white_pawns = 0
            black_pawns = 0
            for _ in range(8):
                if isinstance(board.get(i), Pawn) and board.get(i).color == 1:
                    white_pawns += 1
                if isinstance(board.get(i), Pawn) and board.get(i).color == -1:
                    black_pawns += 1
                i += 8
            doubled_pawns[1] -= (max(0, white_pawns - 1)) * 50
            doubled_pawns[-1] -= (max(0, black_pawns - 1)) * 50

        doubled_pawns_factor = doubled_pawns[1] - doubled_pawns[-1]
        # print("Doubled Pawns Factor: " + str(doubled_pawns_factor))

        # Backward Pawns:
        back_white_pawns = [0, 0, 0, 0, 0, 0, 0, 0]
        back_black_pawns = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(8):
            j = i
            c = 1
            while not (isinstance(board.get(j), Pawn) and board.get(j).color == 1) and j < 64:
                j += 8
                c += 1
            if j < 64:
                back_white_pawns[i] = c 
        for i in range(8):
            j = i
            c = 1
            while j < 64:
                if isinstance(board.get(j), Pawn) and board.get(j).color == -1:
                    back_black_pawns[i] = c
                j += 8
                c += 1

        white_backward_pawns = 0
        black_backward_pawns = 0
        for n in range(1, 7):
            if back_white_pawns[n] != 0 and back_white_pawns[n] < back_white_pawns[n - 1] and back_white_pawns[n] < back_white_pawns[n + 1]:
                white_backward_pawns += 1
            if back_black_pawns[n] > back_black_pawns[n - 1] and back_black_pawns[n] > back_black_pawns[n + 1]:
                black_backward_pawns += 1

        backward_pawn_factor = (white_backward_pawns - black_backward_pawns) * -30
        # print("Backward Pawns Factor: " + str(backward_pawn_factor))

        # Passed Pawns
        front_white_pawns = [0, 0, 0, 0, 0, 0, 0, 0]
        front_black_pawns = [0, 0, 0, 0, 0, 0, 0, 0]

        for i in range(8):
            j = i
            c = 1
            while j < 64:
                if isinstance(board.get(j), Pawn) and board.get(j).color == 1:
                    front_white_pawns[i] = c
                j += 8
                c += 1
        for i in range(8):
            j = i
            c = 1
            while not (isinstance(board.get(j), Pawn) and board.get(j).color == -1) and j < 64:
                j += 8
                c += 1
            if j < 64:
                front_black_pawns[i] = c 

        white_passed_pawns = 0
        black_passed_pawns = 0
        for n in range(1, 7):
            if front_white_pawns[n] >= back_black_pawns[n - 1] and front_white_pawns[n] >= back_black_pawns[n + 1] and front_white_pawns[n] >= back_black_pawns[n]:
                white_passed_pawns += 1
            if front_black_pawns[n] != 0 and (front_black_pawns[n] <= back_white_pawns[n - 1] or back_white_pawns[n - 1] == 0 ) and (front_black_pawns[n] <= back_white_pawns[n + 1] or back_white_pawns[n + 1] == 0) and (front_black_pawns[n] <= back_white_pawns[n] or back_white_pawns[n] == 0):
                black_passed_pawns += 1
        if front_white_pawns[0] >= back_black_pawns[1] and front_white_pawns[0] >= back_black_pawns[0]:
            white_passed_pawns += 1
        if front_white_pawns[7] >= back_black_pawns[6] and front_white_pawns[7] >= back_black_pawns[7]:
            white_passed_pawns += 1
        if (front_black_pawns[0] <= back_white_pawns[1] or back_white_pawns[1] == 0) and (back_white_pawns[0] == 0 or front_black_pawns[0] <= back_white_pawns[0]):
            black_passed_pawns += 1
        if (front_black_pawns[7] <= back_white_pawns[6] or back_white_pawns[6] == 0) and (front_black_pawns[7] <= back_white_pawns[7] or back_white_pawns[7] == 0):
            black_passed_pawns += 1

        passed_pawn_factor = (white_passed_pawns - black_passed_pawns) * 30
        # print("Passed Pawns Factor: " + str(passed_pawn_factor))
        
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
        pawn_island_factor = (white_pawn_islands - black_pawn_islands) * -10 if black_pawn_islands == 0 else 0
        # print("Pawn Island Factor: " + str(pawn_island_factor))

        pawn_factor = backward_pawn_factor + doubled_pawns_factor + passed_pawn_factor + pawn_island_factor
        return pawn_factor

    def is_it_checkmate(self, board):
        if len(self.generate_legal_moves(board)) == 0 and board.check_for_checks(board.side_to_move):
            return True
        return False
    
    def is_it_stalemate(self, board):
        if len(self.generate_legal_moves(board)) == 0 and not board.check_for_checks(board.side_to_move):
            return True
        return False



