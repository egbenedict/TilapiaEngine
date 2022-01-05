from Engine import *

e = Engine("rnbqkbnr/2p1ppp1/p7/1p1pP2p/2P3P1/8/PP1P1P1P/RNBQKBNR w KQkq d6 0 5")

print(e.get_board())
print(e.generate_legal_moves())

