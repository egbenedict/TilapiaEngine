from Engine import *

e = Engine("r2q1r2/1p1bbppk/p4n1p/3ppP2/P1BpP3/3P1R1Q/1PPBN1PP/R6K w - - 0 18")

print(e.get_board())
print(e.generate_legal_moves())

