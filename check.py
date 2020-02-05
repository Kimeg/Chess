def PawnCheck(g,board, x, y):
    if g.myTeam.startswith('W'):
        pawn_dir = 1
    else:
        pawn_dir = -1

    for i in [1, -1]:
        try:
            if board.pieces[(x-i, y+pawn_dir)].name.startswith(g.enemyTeam+'P'):
                #print '\nCheck by {}\n'.format(board.pieces[(x-i, y+pawn_dir)].name) 
                return board.pieces[(x-i, y+pawn_dir)].name, True
        except:
            pass
    return None, False

def KingCheck(xdiff, ydiff, piece):
    if abs(xdiff)<=1 and abs(ydiff)<=1:
        #print '\nCheck by {}\n'.format(piece) 
        return True
    return False
   
def KnightCheck(xdiff, ydiff, piece):
    if (abs(xdiff)==2 and abs(ydiff)==1) or (abs(xdiff)==1 and abs(ydiff)==2):
        #print '\nCheck by {}\n'.format(piece) 
        return True
    return False

def DiagCheck(g, board, x, y, xdiff, ydiff, piece):
    if abs(xdiff) == abs(ydiff):
        x_sign = int(xdiff/abs(xdiff))
        y_sign = int(ydiff/abs(ydiff))
    
        if abs(xdiff) > 1:
            for i in range(1, abs(xdiff)):
                if (board.pieces[(x + i * x_sign, y + i * y_sign)].name.startswith(g.myTeam)):
                    return False
            
            #print '\nCheck by {}\n'.format(piece) 
            return True    
        else:
            #print '\nCheck by {}\n'.format(piece) 
            return True
    return False

def StraightCheck(g, board, x, y, xdiff, ydiff, piece):
    diff = 0
    x_sign = 0 
    y_sign = 0 
    x_scaler = 0
    y_scaler = 0

    if xdiff == 0 and not ydiff == 0:
        diff = ydiff
        y_sign = int(ydiff/abs(ydiff))
        y_scaler = 1
    elif not xdiff == 0 and ydiff == 0:
        diff = xdiff
        x_sign = int(xdiff/abs(xdiff))
        x_scaler = 1

    if not diff == 0:
        if abs(diff) > 1:
            for i in range(1, abs(diff)):
                if (board.pieces[(x + i * x_sign * x_scaler, y + i * y_sign * y_scaler)].name.startswith(g.myTeam)):
                    return False
            #print '\nCheck by {}\n'.format(piece) 
            return True
        else:
            #print '\nCheck by {}\n'.format(piece) 
            return True
    return False

def IsKingChecked(g, board):
    # Store my king's position
    x = board.pos[g.myTeam+'K1'][0]
    y = board.pos[g.myTeam+'K1'][1]

    # Check pawns
    attacking_piece, is_check = PawnCheck(g, board, x, y)
    if is_check:
        return attacking_piece, True

    ''' 
    Iterate through opponent's pieces and check if any of them are in position to check my king.
    If any of my piece is in between my king and any of opponent's ray pieces, current iteration is halted 
    and next iteration starts
    '''
    for piece in board.pos.keys():
        if piece.startswith(g.enemyTeam):
            found = True
            xx = board.pos[piece][0]
            yy = board.pos[piece][1]

            xdiff = xx - x
            ydiff = yy - y

            # Check knights
            if 'H' in piece:
                if KnightCheck(xdiff, ydiff, piece):
                    return piece, True

            # Check bishops and queen
            if 'S' in piece or 'Q' in piece:

                if DiagCheck(g, board, x, y, xdiff, ydiff, piece):
                    return piece, True

            # Check rooks and queen
            if 'R' in piece or 'Q' in piece:
                if StraightCheck(g, board, x, y, xdiff, ydiff, piece):
                    return piece, True

            # Check king
            if 'K' in piece:
                if KingCheck(xdiff, ydiff, piece):
                    return piece, True

    return 'None', False    
