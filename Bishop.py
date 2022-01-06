class Bishop:

    def __init__(self, color):
        self.color = color # 1 = white, -1 = black
        self.id = "bishop"
        self.base_value = 3.1

    def __str__(self):
        return "B" if self.color == 1 else "b"