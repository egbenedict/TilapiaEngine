from Engine import *

e = Engine("rnbqk2r/p1ppbppp/1p3n2/4p1B1/2BPP3/8/PPP2PPP/RN1QK1NR w KQkq - 2 5")

print(e.get_board())
print(e.generate_legal_moves())

