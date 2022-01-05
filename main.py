from Engine import *

e = Engine("rnbqkb2/p2pppp1/1p3r1n/1Rp4p/P6P/3R4/1PPPPPP1/1NBQKBN1 w q - 0 8")

print(e.get_board())
print(e.generate_legal_moves())

