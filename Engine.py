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

    def __init__(self, fen = startingFEN):
        self.board = Board(fen)
        self.move_log = []
    
    # Return board object
    def get_board(self):
        return self.board

    # Returns list of all legal moves in current board state, in addition to metadata about how to modify board
    def generate_legal_moves(self):
        move_list = []
        # Add all pseudo-legal moves first then filter after
        move_list.extend(self.generate_pawn_moves())
        move_list.extend(self.generate_knight_moves())
        move_list.extend(self.generate_bishop_moves())
        move_list.extend(self.generate_rook_moves())
        move_list.extend(self.generate_queen_moves())
        move_list.extend(self.generate_king_moves())
        move_list.extend(self.generate_castle_moves())
        
        move_list = self.filter_legal_moves(move_list)

        return move_list

    def print_legal_moves(self):
        return [x[0] for x in self.generate_legal_moves()]

    #TODO: incoroprate piece lists so no need to loop through entire board each time

    # Return a list of all valid pawn moves (including en passant) in current board state
    def generate_pawn_moves(self):
        pawn_moves = []
        for i in range(64):
            piece = self.board.get(i)
            if isinstance(piece, Pawn) and piece.color == self.board.side_to_move:
                # 1 Square Ahead
                if self.board.get(i + 8 * piece.color) == "-":
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
                 and self.board.get(i + 8 * piece.color) == "-" 
                 and self.board.get(i + 16 * piece.color) == "-"):
                    move = Board.index_2_coord(i + 16 * piece.color)
                    pawn_moves.append((move, i, i + 16 * piece.color, None, i + 8 * piece.color))

                # Diagonal Captures
                if (self.board.get(i + 7 * piece.color) != None and self.board.get(i + 7 * piece.color) != "-") and self.board.get(i + 7 * piece.color).color == piece.color * -1:
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

                if (self.board.get(i + 9 * piece.color) != None and self.board.get(i + 9 * piece.color) != "-") and self.board.get(i + 9 * piece.color).color == piece.color * -1:
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
                if (self.board.get(i + 7 * piece.color) != None and Board.index_2_coord(i + 7 * piece.color) == self.board.en_passant_square):
                    if not((Board.index_2_coord(i)[0] == "a" and piece.color == 1) or (Board.index_2_coord(i)[0] == "h" and piece.color == -1)):
                        move = Board.index_2_coord(i)[0] + "x" + self.board.en_passant_square
                        pawn_moves.append((move, i, i + 7 * piece.color, i - 1))

                if (self.board.get(i + 9 * piece.color) != None and Board.index_2_coord(i + 9 * piece.color) == self.board.en_passant_square):
                    if not((Board.index_2_coord(i)[0] == "h" and piece.color == 1) or (Board.index_2_coord(i)[0] == "a" and piece.color == -1)):
                        move = Board.index_2_coord(i)[0] + "x" + self.board.en_passant_square
                        pawn_moves.append((move, i, i + 9 * piece.color, i + 1))

        return pawn_moves

    # Return a list of all valid knight moves in current board state
    def generate_knight_moves(self):
        knight_moves = []
        for i in range(64):
            piece = self.board.get(i)
            if isinstance(piece, Knight) and piece.color == self.board.side_to_move:
                # NE Squares
                if int(Board.index_2_coord(i)[1]) < 7 and Board.index_2_coord(i)[0] != "h":
                    if self.board.get(i + 17) == "-":
                        move = "N" + Board.index_2_coord(i + 17)
                        knight_moves.append((move, i, i + 17))
                    elif self.board.get(i + 17).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i + 17)
                        knight_moves.append((move, i, i + 17))
                    
                if int(Board.index_2_coord(i)[1]) < 8 and Board.index_2_coord(i)[0] < "g":
                    if self.board.get(i + 10) == "-":
                        move = "N" + Board.index_2_coord(i + 10)
                        knight_moves.append((move, i, i + 10))
                    elif self.board.get(i + 10).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i + 10)
                        knight_moves.append((move, i, i + 10))

                # SE Squares
                if int(Board.index_2_coord(i)[1]) > 1 and Board.index_2_coord(i)[0] < "g":
                    if self.board.get(i - 6) == "-":
                        move = "N" + Board.index_2_coord(i - 6)
                        knight_moves.append((move, i, i - 6))
                    elif self.board.get(i - 6).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i - 6)
                        knight_moves.append((move, i, i - 6))
                    
                if int(Board.index_2_coord(i)[1]) > 2 and Board.index_2_coord(i)[0] < "h":
                    if self.board.get(i - 15) == "-":
                        move = "N" + Board.index_2_coord(i - 15)
                        knight_moves.append((move, i, i - 15))
                    elif self.board.get(i - 15).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i - 15)
                        knight_moves.append((move, i, i - 15))
                            
                # SW Squares
                if int(Board.index_2_coord(i)[1]) > 2 and Board.index_2_coord(i)[0] > "a":
                    if self.board.get(i - 17) == "-":
                        move = "N" + Board.index_2_coord(i - 17)
                        knight_moves.append((move, i, i - 17))
                    elif self.board.get(i - 17).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i - 17)
                        knight_moves.append((move, i, i - 17))
                    
                if int(Board.index_2_coord(i)[1]) > 1 and Board.index_2_coord(i)[0] > "b":
                    if self.board.get(i - 10) == "-":
                        move = "N" + Board.index_2_coord(i - 10)
                        knight_moves.append((move, i, i - 10))
                    elif self.board.get(i - 10).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i - 10)
                        knight_moves.append((move, i, i - 10))

                # NW Squares
                if int(Board.index_2_coord(i)[1]) < 8 and Board.index_2_coord(i)[0] > "b":
                    if self.board.get(i + 6) == "-":
                        move = "N" + Board.index_2_coord(i + 6)
                        knight_moves.append((move, i, i + 6))
                    elif self.board.get(i + 6).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i + 6)
                        knight_moves.append((move, i, i + 6))
                    
                if int(Board.index_2_coord(i)[1]) < 7 and Board.index_2_coord(i)[0] > "a":
                    if self.board.get(i + 15) == "-":
                        move = "N" + Board.index_2_coord(i + 15)
                        knight_moves.append((move, i, i + 15))
                    elif self.board.get(i + 15).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i + 15)
                        knight_moves.append((move, i, i + 15))
        return knight_moves
                        
    # Return a list of all valid bishop moves in current board state
    def generate_bishop_moves(self):
        bishop_moves = []
        for i in range(64):
            piece = self.board.get(i)
            if isinstance(piece, Bishop) and piece.color == self.board.side_to_move:
                # NE Diagonal
                j = i + 9
                while self.board.get(j) == "-" and Board.index_2_coord(j)[0] < "h" and int(Board.index_2_coord(j)[1]) < 8:
                    move = "B" + Board.index_2_coord(j)
                    bishop_moves.append((move, i, j))
                    j += 9
                if self.board.get(j) == "-":
                    move = "B" + Board.index_2_coord(j)
                    bishop_moves.append((move, i, j))
                elif self.board.get(j) != None and self.board.get(j).color == piece.color * -1:
                    move = "Bx" + Board.index_2_coord(j)
                    bishop_moves.append((move, i, j))

                # SE Diagonal
                j = i - 7
                while self.board.get(j) == "-" and Board.index_2_coord(j)[0] < "h" and int(Board.index_2_coord(j)[1]) > 1:
                    move = "B" + Board.index_2_coord(j)
                    bishop_moves.append((move, i, j))
                    j -= 7
                if self.board.get(j) == "-":
                    move = "B" + Board.index_2_coord(j)
                    bishop_moves.append((move, i, j))
                elif self.board.get(j) != None and self.board.get(j).color == piece.color * -1:
                    move = "Bx" + Board.index_2_coord(j)
                    bishop_moves.append((move, i, j))

                # SW Diagonal
                j = i - 9
                while self.board.get(j) == "-" and Board.index_2_coord(j)[0] > "a" and int(Board.index_2_coord(j)[1]) > 1:
                    move = "B" + Board.index_2_coord(j)
                    bishop_moves.append((move, i, j))
                    j -= 9
                if self.board.get(j) == "-":
                    move = "B" + Board.index_2_coord(j)
                    bishop_moves.append((move, i, j))
                elif self.board.get(j) != None and self.board.get(j).color == piece.color * -1:
                    move = "Bx" + Board.index_2_coord(j)
                    bishop_moves.append((move, i, j))

                # NW Diagonal
                j = i + 7
                while self.board.get(j) == "-" and Board.index_2_coord(j)[0] > "a" and int(Board.index_2_coord(j)[1]) < 8:
                    move = "B" + Board.index_2_coord(j)
                    bishop_moves.append((move, i, j))
                    j += 7
                if self.board.get(j) == "-":
                    move = "B" + Board.index_2_coord(j)
                    bishop_moves.append((move, i, j))
                elif self.board.get(j) != None and self.board.get(j).color == piece.color * -1:
                    move = "Bx" + Board.index_2_coord(j)
                    bishop_moves.append((move, i, j))

        return bishop_moves
    
    # Return a list of all valid queen moves in current board state
    def generate_queen_moves(self):
        queen_moves = []
        for i in range(64):
            piece = self.board.get(i)
            if isinstance(piece, Queen) and piece.color == self.board.side_to_move:
                # NE Diagonal
                j = i + 9
                while self.board.get(j) == "-" and Board.index_2_coord(j)[0] < "h" and int(Board.index_2_coord(j)[1]) < 8:
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                    j += 9
                if self.board.get(j) == "-":
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                elif self.board.get(j) != None and self.board.get(j).color == piece.color * -1:
                    move = "Qx" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))

                # SE Diagonal
                j = i - 7
                while self.board.get(j) == "-" and Board.index_2_coord(j)[0] < "h" and int(Board.index_2_coord(j)[1]) > 1:
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                    j -= 7
                if self.board.get(j) == "-":
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                elif self.board.get(j) != None and self.board.get(j).color == piece.color * -1:
                    move = "Qx" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))

                # SW Diagonal
                j = i - 9
                while self.board.get(j) == "-" and Board.index_2_coord(j)[0] > "a" and int(Board.index_2_coord(j)[1]) > 1:
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                    j -= 9
                if self.board.get(j) == "-":
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                elif self.board.get(j) != None and self.board.get(j).color == piece.color * -1:
                    move = "Qx" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))

                # NW Diagonal
                j = i + 7
                while self.board.get(j) == "-" and Board.index_2_coord(j)[0] > "a" and int(Board.index_2_coord(j)[1]) < 8:
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                    j += 7
                if self.board.get(j) == "-":
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                elif self.board.get(j) != None and self.board.get(j).color == piece.color * -1:
                    move = "Qx" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))

                # North
                j = i + 8
                while self.board.get(j) == "-" and int(Board.index_2_coord(j)[1]) < 8:
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                    j += 8
                if self.board.get(j) == "-":
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                elif self.board.get(j) != None and self.board.get(j).color == piece.color * -1:
                    move = "Qx" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))

                # South
                j = i - 8
                while self.board.get(j) == "-" and int(Board.index_2_coord(j)[1]) > 1:
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                    j -= 8
                if self.board.get(j) == "-":
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                elif self.board.get(j) != None and self.board.get(j).color == piece.color * -1:
                    move = "Qx" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))

                # West
                j = i - 1
                while self.board.get(j) == "-" and Board.index_2_coord(j)[0] > "a":
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                    j -= 1
                if self.board.get(j) == "-":
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                elif self.board.get(j) != None and self.board.get(j).color == piece.color * -1:
                    move = "Qx" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))

                # East
                j = i + 1
                while self.board.get(j) == "-" and Board.index_2_coord(j)[0] < "h":
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                    j += 1
                if self.board.get(j) == "-":
                    move = "Q" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))
                elif self.board.get(j) != None and self.board.get(j).color == piece.color * -1:
                    move = "Qx" + Board.index_2_coord(j)
                    queen_moves.append((move, i, j))

        return queen_moves

    # Return a list of all valid king moves in current board state
    def generate_king_moves(self):
        king_moves = []
        for i in range(64):
            piece = self.board.get(i)
            if isinstance(piece, King) and piece.color == self.board.side_to_move:
                # N
                if self.board.get(i + 8) == "-":
                    move = "K" + Board.index_2_coord(i + 8)
                    king_moves.append((move, i, i + 8))
                elif self.board.get(i + 8) != None and self.board.get(i + 8).color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i + 8)
                    king_moves.append((move, i, i + 8))
                
                # S
                if self.board.get(i - 8) == "-":
                    move = "K" + Board.index_2_coord(i - 8)
                    king_moves.append((move, i, i - 8))
                elif self.board.get(i - 8) != None and self.board.get(i - 8).color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i - 8)
                    king_moves.append((move, i, i - 8))
                
                # W
                if Board.index_2_coord(i)[0] != "a" and self.board.get(i - 1) == "-":
                    move = "K" + Board.index_2_coord(i - 1)
                    king_moves.append((move, i, i - 1))
                elif Board.index_2_coord(i)[0] != "a" and self.board.get(i - 1) != None and self.board.get(i - 1).color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i - 1)
                    king_moves.append((move, i, i - 1))

                # E
                if Board.index_2_coord(i)[0] != "h" and self.board.get(i + 1) == "-":
                    move = "K" + Board.index_2_coord(i + 1)
                    king_moves.append((move, i, i + 1))
                elif Board.index_2_coord(i)[0] != "h" and self.board.get(i + 1) != None and self.board.get(i + 1).color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i + 1)
                    king_moves.append((move, i, i + 1))

                # NW
                if Board.index_2_coord(i)[0] != "a" and int(Board.index_2_coord(i)[1]) != 8 and self.board.get(i + 7) == "-":
                    move = "K" + Board.index_2_coord(i + 7)
                    king_moves.append((move, i, i + 7))
                elif Board.index_2_coord(i)[0] != "a" and int(Board.index_2_coord(i)[1]) != 8 and self.board.get(i + 7) != None and self.board.get(i + 7).color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i + 7)
                    king_moves.append((move, i, i + 7))

                # NE
                if Board.index_2_coord(i)[0] != "h" and int(Board.index_2_coord(i)[1]) != 8 and self.board.get(i + 9) == "-":
                    move = "K" + Board.index_2_coord(i + 9)
                    king_moves.append((move, i, i + 9))
                elif Board.index_2_coord(i)[0] != "h" and int(Board.index_2_coord(i)[1]) != 8 and self.board.get(i + 9) != None and self.board.get(i + 9).color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i + 9)
                    king_moves.append((move, i, i + 9))

                # SW
                if Board.index_2_coord(i)[0] != "a" and int(Board.index_2_coord(i)[1]) != 1 and self.board.get(i - 9) == "-":
                    move = "K" + Board.index_2_coord(i - 9)
                    king_moves.append((move, i, i - 9))
                elif Board.index_2_coord(i)[0] != "a" and int(Board.index_2_coord(i)[1]) != 1 and self.board.get(i - 9) != None and self.board.get(i - 9).color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i - 9)
                    king_moves.append((move, i, i - 9))

                # SE
                if Board.index_2_coord(i)[0] != "h" and int(Board.index_2_coord(i)[1]) != 1 and self.board.get(i - 7) == "-":
                    move = "K" + Board.index_2_coord(i - 7)
                    king_moves.append((move, i, i - 7))
                elif Board.index_2_coord(i)[0] != "h" and int(Board.index_2_coord(i)[1]) != 1 and self.board.get(i - 7) != None and self.board.get(i - 7).color == piece.color * -1:
                    move = "Kx" + Board.index_2_coord(i - 7)
                    king_moves.append((move, i, i - 7))
        return king_moves

    # Return a list of all valid rook moves in current board state
    def generate_rook_moves(self):
        rook_moves = []
        for i in range(64):
            piece = self.board.get(i)
            if isinstance(piece, Rook) and piece.color == self.board.side_to_move:
                # North
                j = i + 8
                while self.board.get(j) == "-" and int(Board.index_2_coord(j)[1]) < 8:
                    move = "R" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))
                    j += 8
                if self.board.get(j) == "-":
                    move = "R" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))
                elif self.board.get(j) != None and self.board.get(j).color == piece.color * -1:
                    move = "Rx" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))

                # South
                j = i - 8
                while self.board.get(j) == "-" and int(Board.index_2_coord(j)[1]) > 1:
                    move = "R" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))
                    j -= 8
                if self.board.get(j) == "-":
                    move = "R" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))
                elif self.board.get(j) != None and self.board.get(j).color == piece.color * -1:
                    move = "Rx" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))

                # West
                j = i - 1
                while self.board.get(j) == "-" and Board.index_2_coord(j)[0] > "a":
                    move = "R" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))
                    j -= 1
                if self.board.get(j) == "-":
                    move = "R" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))
                elif self.board.get(j) != None and self.board.get(j).color == piece.color * -1:
                    move = "Rx" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))

                # East
                j = i + 1
                while self.board.get(j) == "-" and Board.index_2_coord(j)[0] < "h":
                    move = "R" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))
                    j += 1
                if self.board.get(j) == "-":
                    move = "R" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))
                elif self.board.get(j) != None and self.board.get(j).color == piece.color * -1:
                    move = "Rx" + Board.index_2_coord(j)
                    rook_moves.append((move, i, j))

        return rook_moves

    # Return a list of all valid castling moves in current board state
    def generate_castle_moves(self):
        castle_moves = []
        # White
        if self.board.side_to_move == 1:
            if self.board.white_can_castle_kingside and self.board.get_coord("f1") == "-" and self.board.get_coord("g1") == "-":
                castle_moves.append(("O-O", None))
            if self.board.white_can_castle_queenside and self.board.get_coord("b1") == "-" and self.board.get_coord("c1") == "-" and self.board.get_coord("d1") == "-":
                castle_moves.append(("O-O-O", None))
        else: # Black
            if self.board.black_can_castle_kingside and self.board.get_coord("f8") == "-" and self.board.get_coord("g8") == "-":
                castle_moves.append(("O-O", None))
            if self.board.black_can_castle_queenside and self.board.get_coord("b8") == "-" and self.board.get_coord("c8") == "-" and self.board.get_coord("d8") == "-":
                castle_moves.append(("O-O-O", None))

        return castle_moves

    def filter_legal_moves(self, move_list):
        legal_moves = []

        for move_tuple in move_list:
            if move_tuple[0] == "O-O":
                if self.board.side_to_move == 1: # White
                    variation_board = Board(None, self.board)
                    legal = not variation_board.check_for_checks(self.board.side_to_move)
                    variation_board.move(("", 4, 5))
                    legal = legal and not variation_board.check_for_checks(self.board.side_to_move)
                    variation_board = Board(None, self.board)
                    variation_board.move(move_tuple)
                    legal = legal and not variation_board.check_for_checks(self.board.side_to_move)
                    if legal:
                        legal_moves.append(move_tuple)

                else: # Black
                    variation_board = Board(None, self.board)
                    legal = not variation_board.check_for_checks(self.board.side_to_move)
                    variation_board.move(("", 60, 61))
                    legal = legal and not variation_board.check_for_checks(self.board.side_to_move)
                    variation_board = Board(None, self.board)
                    variation_board.move(move_tuple)
                    legal = legal and not variation_board.check_for_checks(self.board.side_to_move)
                    if legal:
                        legal_moves.append(move_tuple)
            elif move_tuple[0] == "O-O-O":
                if self.board.side_to_move == 1: # White
                    variation_board = Board(None, self.board)
                    legal = not variation_board.check_for_checks(self.board.side_to_move)
                    variation_board.move(("", 4, 3))
                    legal = legal and not variation_board.check_for_checks(self.board.side_to_move)
                    variation_board = Board(None, self.board)
                    variation_board.move(move_tuple)
                    legal = legal and not variation_board.check_for_checks(self.board.side_to_move)
                    if legal:
                        legal_moves.append(move_tuple)

                else: # Black
                    variation_board = Board(None, self.board)
                    legal = not variation_board.check_for_checks(self.board.side_to_move)
                    variation_board.move(("", 60, 59))
                    legal = legal and not variation_board.check_for_checks(self.board.side_to_move)
                    variation_board = Board(None, self.board)
                    variation_board.move(move_tuple)
                    legal = legal and not variation_board.check_for_checks(self.board.side_to_move)
                    if legal:
                        legal_moves.append(move_tuple)

            else:
                variation_board = Board(None, self.board)
                variation_board.move(move_tuple)
                # print(variation_board)

                legal = not variation_board.check_for_checks(self.board.side_to_move)
                # print(legal)
                if legal:
                    legal_moves.append(move_tuple)

        return legal_moves


    def make_random_move(self):
        move = random.choice(self.generate_legal_moves())
        self.board.move(move)
        self.move_log.append(move[0])


