class King:

    def __init__(self, color):
        self.color = color # 1 = white, -1 = black
        self.id = "king"

    def __str__(self):
        return "K" if self.color == 1 else "k"