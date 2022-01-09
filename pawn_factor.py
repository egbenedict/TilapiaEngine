
def pawn_factor(board):
    # Doubled pawns:
    doubled_pawns = [0, 0, 0]

    back_white_pawns = [0, 0, 0, 0, 0, 0, 0, 0]
    back_black_pawns = [0, 0, 0, 0, 0, 0, 0, 0]

    front_white_pawns = [0, 0, 0, 0, 0, 0, 0, 0]
    front_black_pawns = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(8):

        for j in range(8):
            white_pawns, black_pawns = 0, 0
            index = i
            index += 8 * j

            if isinstance(board.BOARD[index], Pawn):
                if board.BOARD[index].color == 1:
                    white_pawns += 1
                    if back_white_pawns[i] == 0:
                        back_white_pawns[i] = j + 1
                    front_white_pawns[i] = j + 1
                else:
                    black_pawns += 1
                    if front_black_pawns[i] == 0:
                        front_black_pawns[i] = j + 1
                    back_black_pawns[i] = j + 1
            
            doubled_pawns[1] -= (max(0, white_pawns - 1)) * 50
            doubled_pawns[-1] -= (max(0, black_pawns - 1)) * 50

    doubled_pawns_factor = doubled_pawns[1] - doubled_pawns[-1]
    
    # Backward Pawns
    white_backward_pawns = 0
    black_backward_pawns = 0
    for n in range(1, 7):
        if back_white_pawns[n] != 0 and back_white_pawns[n] < back_white_pawns[n - 1] and back_white_pawns[n] < back_white_pawns[n + 1]:
            white_backward_pawns += 1
        if back_black_pawns[n] > back_black_pawns[n - 1] and back_black_pawns[n] > back_black_pawns[n + 1]:
            black_backward_pawns += 1

    backward_pawn_factor = (white_backward_pawns - black_backward_pawns) * -30

    # Passed Pawns
    white_passed_pawns = 0
    black_passed_pawns = 0
    for n in range(1, 7):
        if front_white_pawns[n] >= back_black_pawns[n - 1] and front_white_pawns[n] >= back_black_pawns[n + 1] and front_white_pawns[n] >= back_black_pawns[n]:
            white_passed_pawns += 1
        if front_black_pawns[n] != 0 and (front_black_pawns[n] <= back_white_pawns[n - 1] or back_white_pawns[n - 1] == 0 ) and (front_black_pawns[n] <= back_white_pawns[n + 1] or back_white_pawns[n + 1] == 0) and (front_black_pawns[n] <= back_white_pawns[n] or back_white_pawns[n] == 0):
            black_passed_pawns += 1
    if front_white_pawns[0] >= back_black_pawns[1] and front_white_pawns[0] >= back_black_pawns[0]:
        white_passed_pawns += 1
    if front_white_pawns[7] >= back_black_pawns[6] and front_white_pawns[7] >= back_black_pawns[7]:
        white_passed_pawns += 1
    if (front_black_pawns[0] <= back_white_pawns[1] or back_white_pawns[1] == 0) and (back_white_pawns[0] == 0 or front_black_pawns[0] <= back_white_pawns[0]):
        black_passed_pawns += 1
    if (front_black_pawns[7] <= back_white_pawns[6] or back_white_pawns[6] == 0) and (front_black_pawns[7] <= back_white_pawns[7] or back_white_pawns[7] == 0):
        black_passed_pawns += 1

    passed_pawn_factor = (white_passed_pawns - black_passed_pawns) * 30

    # Pawn Islands
    white_island, black_island = False, False
    white_pawn_islands = 0
    black_pawn_islands = 0

    front_white_pawns.append(0)
    front_black_pawns.append(0)
    for i in range(9):
        if front_white_pawns[i] == 0 and white_island == True:
            white_pawn_islands += 1
            white_island = False
        if front_white_pawns[i] > 0:
            white_island = True

        if front_black_pawns[i] == 0 and black_island == True:
            black_pawn_islands += 1
            black_island = False
        if front_black_pawns[i] > 0:
            black_island = True
        

    # print(white_pawn_islands, black_pawn_islands)
    pawn_island_factor = (white_pawn_islands - black_pawn_islands) * -10 if black_pawn_islands == 0 else 0

    pawn_factor = backward_pawn_factor + doubled_pawns_factor + passed_pawn_factor + pawn_island_factor

    print(backward_pawn_factor, passed_pawn_factor, doubled_pawns_factor, pawn_island_factor)
    return pawn_factor        

