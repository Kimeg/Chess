from check import *
import template
from IO import *
from setting import *

def Castling(g, board, src, target):
    if not src[0] == 4:
        g.Update_Msg('NoCas1')
        #print 'No castling : not in a standard game.'
        return False

    if board.pieces[src].move_count > 0 or not src[0] == 4:
        g.Update_Msg('NoCas2')
        #print 'No castling : King has moved at least once.'
        return False

    xdiff = target[0] - src[0]

    x_dir = xdiff / abs(xdiff)       


    if x_dir > 0:
        rook = board.pieces[(7, src[1])]
        end = 3
    else:
        rook = board.pieces[(0, src[1])]
        end = 4

    if not rook.name.startswith(g.myTeam+'R'):
        g.Update_Msg('NoCas3')
        #print 'No castling : Rook is not available'
        return False

    if rook.move_count > 0:
        g.Update_Msg('NoCas4')
        #print 'No castling : Rook has moved at least once'
        return False

    for i in range(1,end):
        x = src[0] + i * x_dir
        y = src[1]
        if not board.pieces[(x, y)].name == '':
            g.Update_Msg('NoCas5')
            #print 'No castling : obstacle(s)'
            return False

    for i in range(end+1):
        x = src[0] + i * x_dir
        y = src[1]
        t = (x,y)
        copy_board = template.Copy(g)

        copy_board.Move(src, t)
    
        attacking_piece, is_checked = IsKingChecked(g, copy_board)
        if (is_checked):
            g.Update_Msg('NoCas6')
            MSG[g.msg] = 'No castling : King is checked by {}'.format(attacking_piece)
            #print 'No castling : King is checked by {}'.format(attacking_piece)
            return False

    g.Update_Msg('Cas')
    #print 'castling'
    board.castling_rook = rook.name
    board.Move((rook.x, rook.y), (src[0]+x_dir, src[1]))
    return True


def Enpassant(g, board, src, target):
    y_dir = 1
    if g.myTeam == 'B':
        y_dir = -1

    enpassant_piece = board.pieces[(target[0], target[1]-y_dir)]

    if not enpassant_piece.name.startswith(g.enemyTeam+'P'):
        g.Update_Msg('NoEnp1')
        #print "No enpassant : opponent's piece at enpassant position is not a pawn."
        return False
        
    if not board.hist[g.board.index]["Name"] == enpassant_piece.name:
        g.Update_Msg('NoEnp2')
        #print 'No enpassant : previously moved piece is not the enpassant piece'
        return False

    if not enpassant_piece.move_count == 1:
        g.Update_Msg('NoEnp3')
        #print "No enpassant : opponent's pawn at enpassant location has moved more than once."
        return False
        
    if not board.pieces[src].y == enpassant_piece.y:
        g.msg = 'NoEnp4'
        #print "No enpassant : my pawn is at wrong position for enpassant move."
        return False

    board.pos.pop(enpassant_piece.name)
    enpassant_piece.Reset()
    g.Update_Msg('Enp')
    board.enpassant_pawn = enpassant_piece.name
    #print "Enpassant"
    return True

def KnightRule(g, xdiff, ydiff):
    if (abs(xdiff)==2 and abs(ydiff)==1) or (abs(xdiff)==1 and abs(ydiff)==2):
        g.Update_Msg('ValidKnight')
        #print "\nvalid knight rule\n"
        return True
    g.Update_Msg('InValidKnight')
    #print "\ninvalid knight rule\n"
    return False

def DiagRule(g, board, x, y, xdiff, ydiff):
    if abs(xdiff) == abs(ydiff):
        x_sign = int(xdiff/abs(xdiff))
        y_sign = int(ydiff/abs(ydiff))
    
        if abs(xdiff) >= 1:
            for i in range(abs(xdiff)):
                i += 1

                p = board.pieces[(x + i * x_sign, y + i * y_sign)].name
                if not p == '':
                    if abs(xdiff)==i:
                        # opponent's piece at target location
                        g.Update_Msg('PathDiag')
                        #print "\nvalid diag rule\n"
                        return True
                    # my piece or opponent piece is blocking
                    g.Update_Msg('PathDiagBlocked')
                    if not g.msg == '':
                        MSG[g.msg] = p + ' is blocking the path.'
                    #print p + ' is blocking the path.'
                    return False
            # no piece found up to target location
            g.Update_Msg('PathDiag')
            #print "\nvalid diag rule\n"
            return True
    g.Update_Msg('PathNotDiag')
    #print "\ninvalid diagonal rule\n"
    return False

def StraightRule(g, board, x, y, xdiff, ydiff):
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
    else:
        #print "\ninvalid straight rule\n"
        g.Update_Msg('PathNotStraight')
        return False

    if abs(diff) >= 1:
        for i in range(abs(diff)):
            i += 1
            p = board.pieces[(x + i * x_sign * x_scaler, y + i * y_sign * y_scaler)].name
            if not p == '':
                if abs(diff) == i:
                    g.Update_Msg('PathStraight')
                    #print "\nvalid straight rule\n"
                    return True
                g.Update_Msg('PathStraightBlocked')
                if not g.msg == '':
                    MSG[g.msg] = p + ' is blocking the path.'
                #print p + ' is blocking the path.'
                return False
        g.Update_Msg('PathStraight')
        #print "\nvalid straight rule\n"
        return True
    g.Update_Msg('PathNotStraight')
    #print "\nimpossible case. debug your code if this message gets printed.\n"
    return False

def QueenRule(g, board, x, y, xdiff, ydiff):
    if DiagRule(g, board, x, y, xdiff, ydiff) or StraightRule(g, board, x, y, xdiff, ydiff):
        #print "\nvalid queen rule\n"
        return True
    #print "\ninvalid queen rule\n"
    return False

def KingRule(g, board, xdiff, ydiff, src, target):
    if abs(xdiff) > 1 or abs(ydiff) > 1:
        if abs(xdiff) == 2 and ydiff == 0:
            if Castling(g, board, src, target):
                return True
        g.Update_Msg('InValidKing')
        #print "\ninvalid king rule\n"
        return False
    g.Update_Msg('ValidKing')
    #print "\nvalid king rule\n"
    return True

def PawnRule(g, board, name, x, y, xdiff, ydiff, src, target):
    y_dir = 1
    if name.startswith('B'):
        y_dir = -1
        ydiff = -ydiff

    if ydiff < 0:
        g.Update_Msg('PawnBackwards')
        #print "\npawn cannot move backwards\n"
        return False
    else:
        if ydiff > 0:
            if ydiff > 2:
                g.Update_Msg('PawnMultiple')
                #print "\npawn cannot move 3 or more blocks\n"
                return False

            if ydiff == 1:
                if xdiff == 0:
                    if board.pieces[target].name == '':
                        g.Update_Msg('ValidPawn')
                        #print "\nvalid pawn rule\n"
                        return True
                    g.Update_Msg('PawnBlocked')
                    #print "\nobstacle\n"
                    return False
                else:
                    if abs(xdiff) == 1:

                        if board.pieces[target].name.startswith(g.enemyTeam):
                            g.Update_Msg('ValidPawn')
                            #print "\nvalid pawn rule\n"
                            return True
                        else:
                            if board.pieces[target].name.startswith(g.myTeam):
                                g.Update_Msg('PawnBlocked')
                                #print "\nobstacle\n"
                                return False
                            else:
                                if Enpassant(g, board, src, target):
                                    #print "\nvalid pawn rule\n"
                                    return True
                                else:
                                    g.Update_Msg('InvalidPawn')
                    else:
                        g.Update_Msg('InvalidPawn')
                        return False
            else:
                if xdiff == 0:
                    y_pos = 1
                    if g.myTeam == 'B':
                        y_pos = 6

                    if board.pieces[(x,y)].move_count > 0 or not y_pos == y:
                        return False

                    for i in range(1,3):
                        if not board.pieces[(x,y + i * y_dir)].name == '':
                            return False

                    g.Update_Msg('ValidPawn')
                    #print "\nvalid pawn rule\n"
                    return True
                else:
                    g.Update_Msg('InvalidPawn')
                    return False

        g.Update_Msg('InvalidPawn')
        return False            
    #print "\nvalid pawn rule\n"
    return True

def PreCheck(g, name, x, y, xdiff, ydiff, src, target):
    copy_board = template.Copy(g)

    if 'P' in name:
        PawnRule(g, copy_board, name, x, y, xdiff, ydiff, src, target)  

    copy_board.Move(src, target)

    attacking_piece, is_checked = IsKingChecked(g, copy_board)

    return not is_checked

def IsValidRule(g, board, src, target, verbose = False):
    if verbose:
        g.verbose = True
    else:
        g.verbose = False

    name = board.pieces[src].name

    x = board.pieces[src].x
    y = board.pieces[src].y

    xdiff = board.pieces[target].x - x
    ydiff = board.pieces[target].y - y

    if name.startswith(g.myTeam):
        if PreCheck(g, name, x, y, xdiff, ydiff, src, target):
            if 'H' in name: 
                return KnightRule(g, xdiff, ydiff)

            elif 'S' in name:
                return DiagRule(g, board, x, y, xdiff, ydiff)

            elif 'R' in name:
                return StraightRule(g, board, x, y, xdiff, ydiff)
                                    
            elif 'Q' in name:     
                return QueenRule(g, board, x, y, xdiff, ydiff)

            elif 'K' in name:
                return KingRule(g, board, xdiff, ydiff, src, target)

            elif 'P' in name:
                return PawnRule(g, board, name, x, y, xdiff, ydiff, src, target)
        return False
    return True

