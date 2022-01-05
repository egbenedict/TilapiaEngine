from Engine import *

e = Engine("r1bqkbn1/1P3p1r/3pp1p1/p6p/1nK1Q3/4P1PB/PPP2P1P/RNB3NR w q - 0 13")

print(e.get_board())
print(e.generate_legal_moves())

