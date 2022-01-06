class Knight:

    def __init__(self, color):
        self.color = color # 1 = white, -1 = black
        self.id = "knight"
        self.base_value = 3.0

    def __str__(self):
        return "N" if self.color == 1 else "n"