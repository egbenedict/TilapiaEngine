class Pawn:

    def __init__(self, color):
        self.color = color # 1 = white, -1 = black

    def __str__(self):
        return "P" if self.color == 1 else "p"