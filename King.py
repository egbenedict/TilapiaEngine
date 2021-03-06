class King:

    # Square Bonus Maps 
    # (White, Opening):
    # -30,-40,-40,-50,-50,-40,-40,-30,
    # -30,-40,-40,-50,-50,-40,-40,-30,
    # -30,-40,-40,-50,-50,-40,-40,-30,
    # -30,-40,-40,-50,-50,-40,-40,-30,
    # -20,-30,-30,-40,-40,-30,-30,-20,
    # -10,-20,-20,-20,-20,-20,-20,-10,
    #  10,  0, -5, -5, -5,  -5,  0, 10,
    #  20, 30, 10,  0,  0, 10, 30, 20
    # 
    # (White, Endgame):
    # -50,-40,-30,-20,-20,-30,-40,-50,
    # -30,-20,-10,  0,  0,-10,-20,-30,
    # -30,-10, 20, 30, 30, 20,-10,-30,
    # -30,-10, 30, 40, 40, 30,-10,-30,
    # -30,-10, 30, 40, 40, 30,-10,-30,
    # -30,-10, 20, 30, 30, 20,-10,-30,
    # -30,-30,  0,  0,  0,  0,-30,-30,
    # -50,-30,-30,-30,-30,-30,-30,-50

    # (Black, Opening):
    # 20, 30, 10,  0,  0, 10, 30, 20,
    # 10,  0, -5, -5, -5, -5,  0, 10,
    # -10,-20,-20,-20,-20,-20,-20,-10,
    #   -20,-30,-30,-40,-40,-30,-30,-20,
    #  -30,-40,-40,-50,-50,-40,-40,-30,
    # -30,-40,-40,-50,-50,-40,-40,-30,
    # -30,-40,-40,-50,-50,-40,-40,-30,
    # -30,-40,-40,-50,-50,-40,-40,-30,
    # 
    # (Black, Endgame):
    # -50,-30,-30,-30,-30,-30,-30,-50
    # -30,-30,  0,  0,  0,  0,-30,-30,
    # -30,-10, 20, 30, 30, 20,-10,-30,
    # -30,-10, 30, 40, 40, 30,-10,-30,
    # -30,-10, 30, 40, 40, 30,-10,-30,
    # -30,-10, 20, 30, 30, 20,-10,-30,
    # -30,-20,-10,  0,  0,-10,-20,-30,
    # -50,-40,-30,-20,-20,-30,-40,-50,

    
    square_bonuses = [None, [[20, 30, 10,  0,  0, 10, 30, 20, 
                              10,  0,  -5,  -5,  -5,  -5,  0, 10,
                              -10,-20,-20,-20,-20,-20,-20,-10,
                              -20,-30,-30,-40,-40,-30,-30,-20,
                              -30,-40,-40,-50,-50,-40,-40,-30,
                              -30,-40,-40,-50,-50,-40,-40,-30,
                              -30,-40,-40,-50,-50,-40,-40,-30,
                              -30,-40,-40,-50,-50,-40,-40,-30],
                             [-50,-30,-30,-30,-30,-30,-30,-50,  
                              -30,-30,  0,  0,  0,  0,-30,-30,
                              -30,-10, 20, 30, 30, 20,-10,-30,
                              -30,-10, 30, 40, 40, 30,-10,-30,
                              -30,-10, 30, 40, 40, 30,-10,-30,
                              -30,-10, 20, 30, 30, 20,-10,-30,
                              -30,-20,-10,  0,  0,-10,-20,-30,
                              -50,-40,-30,-20,-20,-30,-40,-50]],
                            [[-30,-40,-40,-50,-50,-40,-40,-30,
                              -30,-40,-40,-50,-50,-40,-40,-30,
                              -30,-40,-40,-50,-50,-40,-40,-30,
                               -30,-40,-40,-50,-50,-40,-40,-30,
                              -10,-20,-20,-20,-20,-20,-20,-10,
                              -10,  5,  5,  5,  5,  5,  0,-10,
                             10,  0,  -5,  -5,  -5, -5,  0, 10,
                              20, 30, 10,  0,  0, 10, 30, 20],
                             [-50,-40,-30,-20,-20,-30,-40,-50,  
                              -30,-20,-10,  0,  0,-10,-20,-30,
                              -30,-10, 20, 30, 30, 20,-10,-30,
                              -30,-10, 30, 40, 40, 30,-10,-30,
                              -30,-10, 30, 40, 40, 30,-10,-30,
                              -30,-10, 20, 30, 30, 20,-10,-30,
                              -30,-30,  0,  0,  0,  0,-30,-30,
                              -50,-30,-30,-30,-30,-30,-30,-50]]]



    def __init__(self, color):
        self.color = color # 1 = white, -1 = black
        self.id = "king"
        self.gui_id = "wK" if self.color == 1 else "bK"

    def __str__(self):
        return "???" if self.color == 1 else "???"

    def get_bonus(self, i, endgame):
        if endgame:
            return King.square_bonuses[self.color][1][i]
        else:
            return King.square_bonuses[self.color][0][i]