class Queen:

    # Square Bonus Maps 
    # (White, Opening):
    # -20,-10,-10, -5, -5,-10,-10,-20,
    # -10,  0,  0,  0,  0,  0,  0,-10,
    # -10,  0,  5,  5,  5,  5,  0,-10,
    #  0,   0,  5,  5,  5,  5,  0,  0,
    #  0,   0,  5,  5,  5,  5,  0,  0,
    # -10,  5,  5,  5,  5,  5,  0,-10,
    # -10,  0,  5,  0,  0,  0,  0,-10,
    # -20,-10,-10, -5,  0,-10,-10,-20,
    # 
    # (White, Endgame):
    # -20,-10,-10,-10,-10,-10,-10,-20,
    # -10,  0,  0,  0,  0,  0,  0,-10,
    # -10,  0,  5,  5,  5,  5,  0,-10,
    # -10,  0,  5,  5,  5,  5,  0,-10,
    # -10,  0,  5,  5,  5,  5,  0,-10,
    # -10,  0,  5,  5,  5,  5,  0,-10,
    # -10,  0,  0,  0,  0,  0,  0,-10,
    # -20,-10,-10,-10,-10,-10,-10,-20,

    # (Black, Opening):
    # -20,-10,-10, -5,  0,-10,-10,-20,
    # -10,  0,  5,  0,  0,  0,  0,-10,
    # -10,  5,  5,  5,  5,  5,  0,-10,
    #   0,  0,  5,  5,  5,  5,  0,  0,
    #   0,  0,  5,  5,  5,  5,  0,  0,
    # -10,  0,  5,  5,  5,  5,  0,-10,
    # -10,  0,  0,  0,  0,  0,  0,-10,
    # -20,-10,-10, -5, -5,-10,-10,-20,
    # 
    # (Black, Endgame):
    # -20,-10,-10,-10,-10,-10,-10,-20,
    # -10,  0,  0,  0,  0,  0,  0,-10,
    # -10,  0,  5,  5,  5,  5,  0,-10,
    # -10,  0,  5,  5,  5,  5,  0,-10,
    # -10,  0,  5,  5,  5,  5,  0,-10,
    # -10,  0,  5,  5,  5,  5,  0,-10,
    # -10,  0,  0,  0,  0,  0,  0,-10,
    # -20,-10,-10,-10,-10,-10,-10,-20,  

    
    square_bonuses = [None, [[-20, -10, -10, -5, 0, -10, -10, -20, 
                              -10, 0, 5, 0, 0, 0, 0, -10,
                              -10,  5,  5,  5,  5,  5,  0,-10,
                              0,   0,  5,  5,  5,  5,  0,  0,
                              0,   0,  5,  5,  5,  5,  0,  0,
                              -10,  0,  5,  5,  5,  5,  0,-10,
                              -10,  0,  0,  0,  0,  0,  0,-10,
                              -20,-10,-10, -5, -5,-10,-10,-20],
                             [-20,-10,-10,-10,-10,-10,-10,-20,   
                              -10,  0,  0,  0,  0,  0,  0,-10,
                              -10,  0,  5,  5,  5,  5,  0,-10,
                              -10,  0,  5,  5,  5,  5,  0,-10,
                              -10,  0,  5,  5,  5,  5,  0,-10,
                              -10,  0,  5,  5,  5,  5,  0,-10,
                              -10,  0,  0,  0,  0,  0,  0,-10,
                              -20,-10,-10,-10,-10,-10,-10,-20]],
                            [[-20,-10,-10, -5, -5,-10,-10,-20,
                              -10,  0,  0,  0,  0,  0,  0,-10,
                              -10,  0,  5,  5,  5,  5,  0,-10,
                               0,  0,  5,  5,  5,  5,  0,  0,
                              0,  0,  5,  5,  5,  5,  0,  0,
                              -10,  5,  5,  5,  5,  5,  0,-10,
                             -10,  0,  5,  0,  0,  0,  0,-10,
                              -20,-10,-10, -5,  0,-10,-10,-20],
                             [-20,-10,-10,-10,-10,-10,-10,-20,   
                              -10,  0,  0,  0,  0,  0,  0,-10,
                              -10,  0,  5,  5,  5,  5,  0,-10,
                              -10,  0,  5,  5,  5,  5,  0,-10,
                              -10,  0,  5,  5,  5,  5,  0,-10,
                              -10,  0,  5,  5,  5,  5,  0,-10,
                              -10,  0,  0,  0,  0,  0,  0,-10,
                              -20,-10,-10,-10,-10,-10,-10,-20]]]



    def __init__(self, color):
        self.color = color # 1 = white, -1 = black
        self.id = "queen"
        self.base_value = 900
        self.gui_id = "wQ" if self.color == 1 else "bQ"

    def __str__(self):
        return "???" if self.color == 1 else "???"


    def get_bonus(self, i, endgame):
        if endgame:
            return Queen.square_bonuses[self.color][1][i]
        else:
            return Queen.square_bonuses[self.color][0][i]