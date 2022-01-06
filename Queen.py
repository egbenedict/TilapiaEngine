class Queen:

    def __init__(self, color):
        self.color = color # 1 = white, -1 = black
        self.id = "queen"
        self.base_value = 900

    def __str__(self):
        return "Q" if self.color == 1 else "q"