from frozen import *
from check import *
from rule import *
from setting import *

def IsValidMove(g, _from, _to):
    src = g.board.pieces[_from[0], _from[1]]
    target = g.board.pieces[_to[0], _to[1]]

    g.verbose = True
    if IsValidRule(g, g.board, _from, _to, True):
        return True
    else:
        return False


def IsGameOver(g): 
    attacking_piece, is_check = IsKingChecked(g, g.board)
    is_frozen = IsFrozen(g)
    if is_check:
        g.status = 'King checked by {}\n'.format(attacking_piece)
        #print('King checked by {}'.format(attacking_piece))
        if is_frozen:
            g.status += 'Checkmated by {}'.format(attacking_piece)
            #print('Checkmated by {}'.format(attacking_piece))
            g.is_checkmate = True
            return True
    else:
        if is_frozen:
            g.status += 'Stalemate'
            #print('Stalemate')
            g.is_stalemate = True
            return True
    return False

def IsValidInput(g):
    if g.myTeam == 'W':
        print("White's turn.")
    else:
        print("Black's turn.")

    #piece to move
    print('Enter piece to move.')
    src = input()

    try:
        if src[0] in VALID_INPUT.keys() and int(src[1]) in VALID_INPUT.values():
            pass
        elif src in QUIT: 
            return 'exit'
        elif src in RESET:
            return 'reset'
        else:
            print('\nInvalid Input.\n')
            return False
    except:
        print('\nInvalid Input.\n')
        return False

    src = (VALID_INPUT[src[0]]-1, int(src[1])-1)

    if g.board.pieces[src].name.startswith(g.enemyTeam):
        print("\nOpponent's piece cannot be moved.\n")
        return False
    if g.board.pieces[src].name == '':
        print('\nEmpty cell.\n')
        return False

    print(g.board.pieces[src].name)
    #where to move
    print('\nEnter location to move.\n')
    target = input()
    try:
        if target[0] in VALID_INPUT.keys() and int(target[1]) in VALID_INPUT.values():
            pass
        elif target in QUIT: 
            return 'exit'
        else:
            print('\nInvalid Input.\n')
            return False
    except:
        print('\nInvalid Input.\n')
        return False

    target = (VALID_INPUT[target[0]]-1, int(target[1])-1)
    if target[0] == src[0] and target[1] == src[1]:
        print("\nLocation to move is same as current piece.\n")
        return False
    try:
        if g.board.pieces[target].name.startswith(g.myTeam):
            print("\nCannot attack my own piece.\n")
            return False
    except:
        pass
    print(g.board.pieces[target].name)
    return [src, target]
