import numpy as np
import random as rd
import math
import time


def ai_student(board, player, temps):
    # Tentative de créer un algorithme MCTS
    # Crédit pour l'utilisation de bitstring : https://towardsdatascience.com/creating-the-perfect-connect-four-ai-bot-c165115557b0
    # Tout le reste du code vient de moi après décryptage de la base de la théorie sur le MCTS

    start_time = time.time()

    board = np.array(board)
    board[board == -1.] = 2
    board[board == 1.] = 1
    board[board == 0.] = 0

    bitmap, mask = get_position_mask_bitmap(board, player)
    bitmap_opponent, mask_opponent = get_position_mask_bitmap(board, abs(player-3))

    leaf = legal_moves(mask)
    UCT = np.zeros(7)
    N = np.zeros(7)
    Q = np.zeros(7)
    W = np.zeros(7)
    D = np.zeros(7)
    for node in leaf:
        UCT[node] = np.inf

    for col in leaf:
        # Creates the attack and defense moves, to check if one is a winning move
        attack_bitmap, attack_mask = make_move(bitmap, mask, col)
        if connected_four(attack_bitmap ^ attack_mask):
            return col, 100, 1

    for col in leaf:
        defense_bitmap, defense_mask = make_move(bitmap_opponent, mask_opponent, col)
        if connected_four(defense_bitmap ^ defense_mask):
            return col, None, 1

    while time.time() - start_time < temps:
        node = np.argmax(UCT)
        bitmap_simulation, mask_simulation = make_move(bitmap, mask, node)
        #for i in range(50):
        result = run_game(bitmap_simulation, mask_simulation)
        if result == 1:
            Q[node] += 1
            W[node] += 1
        if result == 0:
            Q[node] += 0.0001
            D[node] += 1
        N[node] += 1
        UCT[node] = Q[node] / N[node] + math.sqrt(1.4 * math.log(sum(N)) / N[node])

    Best_move = np.argmax(N)
    #print(((2 * W[Best_move] / N[Best_move]) - 1) * 100)
    #print(Q[Best_move] / N[Best_move] * 100)
    return Best_move, ((2 * W[Best_move] / N[Best_move]) - 1) * 100, sum(N)


def get_position_mask_bitmap(board, player):
    position, mask = '', ''
    # Start with right-most column
    for j in range(6, -1, -1):
        # Add 0-bits to sentinel
        mask += '0'
        position += '0'
        # Start with bottom row
        for i in range(0, 6):
            mask += ['0', '1'][board[i, j] != 0]
            position += ['0', '1'][board[i, j] == player]
    return int(position, 2), int(mask, 2)


def make_move(position, mask, col):
    new_position = position ^ mask
    new_mask = mask | (mask + (1 << (col*7)))
    return new_position, new_mask


def connected_four(position):
    # Horizontal check
    m = position & (position >> 7)
    if m & (m >> 14):
        return True
    # Diagonal \
    m = position & (position >> 6)
    if m & (m >> 12):
        return True
    # Diagonal /
    m = position & (position >> 8)
    if m & (m >> 16):
        return True
    # Vertical
    m = position & (position >> 1)
    if m & (m >> 2):
        return True
    # Nothing found
    return False


def run_game(the_bitmap, the_mask):
    i = 0
    while the_mask != 279258638311359:

        move = ai_random(the_bitmap, the_mask)
        the_bitmap, the_mask = make_move(the_bitmap, the_mask, move)
        if connected_four(the_bitmap):
            return (-1)**i
        i += 1

    return 0


def ai_random(arg_bitmap, arg_mask):
    # Collects the moves which can be played (i.e. the nonfull columns)
    nonfull_cols = legal_moves(arg_mask)
    for col in nonfull_cols:

        # Creates the attack and defense moves, to check if one is a winning move
        attack_bitmap, attack_mask = make_move(arg_bitmap, arg_mask, col)
        if connected_four(attack_bitmap ^ attack_mask):
            return col


        copy_cols = nonfull_cols[:]
        copy_cols.remove(col)
        if copy_cols != []:
            temp_bitmap, temp_mask = make_move(arg_bitmap, arg_mask, rd.choice(copy_cols))
            defense_bitmap, defense_mask = make_move(temp_bitmap, temp_mask, col)
            if connected_four(defense_bitmap ^ defense_mask):
                return col

    # Otherwise, plays random
    return rd.choice(nonfull_cols)


def legal_moves(mask):
    bit_moves = []
    for i in range(7):
        col_mask = 0b111111 << 7 * i
        if col_mask != mask & col_mask:
            bit_moves.append(i)
    return bit_moves
