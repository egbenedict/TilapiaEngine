from Board import *
from Rook import *
from Queen import *
from Knight import *
from Bishop import *
from King import *
from Pawn import *

class Engine:

    startingFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def __init__(self, fen = startingFEN):
        self.board = Board(fen)
        self.move_log = []
    
    # Return board object
    def get_board(self):
        return self.board

    # Returns list of all legal moves in current board state
    def generate_legal_moves(self):
        move_list = []
        # Add all pseudo-legal moves first then filter after
        move_list.extend(self.generate_pawn_moves())
        move_list.extend(self.generate_knight_moves())
        
        return move_list

    
    def generate_pawn_moves(self):
        pawn_moves = []
        for i in range(64):
            piece = self.board.get(i)
            if isinstance(piece, Pawn) and piece.color == self.board.side_to_move:
                # 1 Square Ahead
                if self.board.get(i + 8 * piece.color) == "-":
                    move = Board.index_2_coord(i) + Board.index_2_coord(i + 8 * piece.color)
                    pawn_moves.append(move)

                # 2 Squares Ahead
                if (((Board.index_2_coord(i)[1] == "2" and piece.color == 1)
                 or (Board.index_2_coord(i)[1] == "7" and piece.color == -1)) 
                 and self.board.get(i + 8 * piece.color) == "-" 
                 and self.board.get(i + 16 * piece.color) == "-"):
                    move = Board.index_2_coord(i) + Board.index_2_coord(i + 16 * piece.color)
                    pawn_moves.append(move)

                # Diagonal Captures
                if (self.board.get(i + 7 * piece.color) != None and self.board.get(i + 7 * piece.color) != "-") and self.board.get(i + 7 * piece.color).color == piece.color * -1:
                    if not((Board.index_2_coord(i)[0] == "a" and piece.color == 1) or (Board.index_2_coord(i)[0] == "h" and piece.color == -1)):
                        move = Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 7 * piece.color)
                        pawn_moves.append(move)

                if (self.board.get(i + 9 * piece.color) != None and self.board.get(i + 9 * piece.color) != "-") and self.board.get(i + 9 * piece.color).color == piece.color * -1:
                    if not((Board.index_2_coord(i)[0] == "h" and piece.color == 1) or (Board.index_2_coord(i)[0] == "a" and piece.color == -1)):
                        move = Board.index_2_coord(i)[0] + "x" + Board.index_2_coord(i + 9 * piece.color)
                        pawn_moves.append(move)

                # En Passant
                if (self.board.get(i + 7 * piece.color) != None and Board.index_2_coord(i + 7 * piece.color) == self.board.en_passant_square):
                    if not((Board.index_2_coord(i)[0] == "a" and piece.color == 1) or (Board.index_2_coord(i)[0] == "h" and piece.color == -1)):
                        move = Board.index_2_coord(i)[0] + "x" + self.board.en_passant_square
                        pawn_moves.append(move)

                if (self.board.get(i + 9 * piece.color) != None and Board.index_2_coord(i + 9 * piece.color) == self.board.en_passant_square):
                    if not((Board.index_2_coord(i)[0] == "h" and piece.color == 1) or (Board.index_2_coord(i)[0] == "a" and piece.color == -1)):
                        move = Board.index_2_coord(i)[0] + "x" + self.board.en_passant_square
                        pawn_moves.append(move)

        return pawn_moves

    def generate_knight_moves(self):
        knight_moves = []
        for i in range(64):
            piece = self.board.get(i)
            if isinstance(piece, Knight) and piece.color == self.board.side_to_move:
                # NE Squares
                if int(Board.index_2_coord(i)[1]) < 7 and Board.index_2_coord(i)[0] != "h":
                    if self.board.get(i + 17) == "-":
                        move = "N" + Board.index_2_coord(i + 17)
                        knight_moves.append(move)
                    elif self.board.get(i + 17).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i + 17)
                        knight_moves.append(move)
                    
                if int(Board.index_2_coord(i)[1]) < 8 and Board.index_2_coord(i)[0] < "g":
                    if self.board.get(i + 10) == "-":
                        move = "N" + Board.index_2_coord(i + 10)
                        knight_moves.append(move)
                    elif self.board.get(i + 10).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i + 10)
                        knight_moves.append(move)

                # SE Squares
                if int(Board.index_2_coord(i)[1]) > 1 and Board.index_2_coord(i)[0] < "g":
                    if self.board.get(i - 6) == "-":
                        move = "N" + Board.index_2_coord(i - 6)
                        knight_moves.append(move)
                    elif self.board.get(i - 6).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i - 6)
                        knight_moves.append(move)
                    
                if int(Board.index_2_coord(i)[1]) > 2 and Board.index_2_coord(i)[0] < "h":
                    if self.board.get(i - 15) == "-":
                        move = "N" + Board.index_2_coord(i - 15)
                        knight_moves.append(move)
                    elif self.board.get(i - 15).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i - 15)
                        knight_moves.append(move)
                            
                # SW Squares
                if int(Board.index_2_coord(i)[1]) > 2 and Board.index_2_coord(i)[0] > "a":
                    if self.board.get(i - 17) == "-":
                        move = "N" + Board.index_2_coord(i - 17)
                        knight_moves.append(move)
                    elif self.board.get(i - 17).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i - 17)
                        knight_moves.append(move)
                    
                if int(Board.index_2_coord(i)[1]) > 1 and Board.index_2_coord(i)[0] > "b":
                    if self.board.get(i - 10) == "-":
                        move = "N" + Board.index_2_coord(i - 10)
                        knight_moves.append(move)
                    elif self.board.get(i - 10).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i - 10)
                        knight_moves.append(move)

                # NW Squares
                if int(Board.index_2_coord(i)[1]) < 8 and Board.index_2_coord(i)[0] > "b":
                    if self.board.get(i + 6) == "-":
                        move = "N" + Board.index_2_coord(i + 6)
                        knight_moves.append(move)
                    elif self.board.get(i + 6).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i + 6)
                        knight_moves.append(move)
                    
                if int(Board.index_2_coord(i)[1]) < 7 and Board.index_2_coord(i)[0] > "a":
                    if self.board.get(i + 15) == "-":
                        move = "N" + Board.index_2_coord(i + 15)
                        knight_moves.append(move)
                    elif self.board.get(i + 15).color == piece.color * -1:
                        move = "Nx" + Board.index_2_coord(i + 15)
                        knight_moves.append(move)
        return knight_moves
                        
    def generate_bishop_moves(self):
        pass

    def generate_queen_moves(self):
        pass

    def generate_king_moves(self):
        pass

    def generate_castle_moves(self):
        pass

    def generate_en_passant_moves(self):
        pass # Later
