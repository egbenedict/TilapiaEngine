from Engine import *

e = Engine("r1bqkbn1/1p1ppp1r/6p1/p1p4p/1nKPQ3/4P1PB/PPP2P1P/RNB3NR w q - 0 10")

print(e.get_board())
print(e.generate_legal_moves())

