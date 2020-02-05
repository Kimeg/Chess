from rule import *
from setting import *
from template import *
from check import *

def CheckPawn(g, x, y):
    y_dir = 1
    if g.myTeam == 'B':
        y_dir = -1

    paths = [[1,y_dir],[-1,y_dir],[0,y_dir],[0,y_dir * 2]]
    if g.board.pieces[(x, y)].move_count > 0:
        paths = paths[:-1]
    return CheckDiscretePaths(g, x, y, paths)

def CheckKing(g, x, y):
    paths = KING_PATHS
    if g.board.pieces[(x, y)].move_count > 0:
        paths = KING_PATHS[:-2]
    return CheckDiscretePaths(g, x, y, paths)

def CheckKnight(g, x, y):
    return CheckDiscretePaths(g, x, y, KNIGHT_PATHS)

def CheckDiagPaths(g, x, y):
    top = 7-y; bot = y; right = 7-x; left = x
    dists = [min(top, right), min(top, left), min(bot, right), min(bot, left)]
    return CheckRayPieces(g, x, y, DIAG_PATHS, dists)

def CheckStraightPaths(g, x, y):
    top = 7-y; bot = y; right = 7-x; left = x
    dists = [top, right, bot, left]
    return CheckRayPieces(g, x, y, STRAIGHT_PATHS, dists)

def CheckRayPieces(g, x, y, directions, dists):
    for dirs, dist in zip(directions, dists):
        if dist > 0:
            for i in range(dist):
                tx = x + i * dirs[0]
                ty = y + i * dirs[1]

                if not tx in RANGE or not ty in RANGE:
                    break
    
                t = (tx, ty)
                if g.board.pieces[t].name.startswith(g.myTeam):
                    break

                board = Copy(g)
                if not IsValidRule(g, board, (x,y), t):
                    break

                board.Move((x,y), t)
                
                attacking_piece, is_checked = IsKingChecked(g, board)

                if not is_checked:
                    return False
    return True

def CheckDiscretePaths(g, x, y, paths):
    for path in paths:
        tx = x+path[0]
        ty = y+path[1]

        if not tx in RANGE or not ty in RANGE:
            continue

        t = (tx, ty)
        if g.board.pieces[t].name.startswith(g.myTeam):
            continue

        board = Copy(g)
        if not IsValidRule(g, board, (x,y), t):
            continue

        board.Move((x,y), t)
        
        attacking_piece, is_checked = IsKingChecked(g, board)

        if not is_checked:
            return False
    return True

def IsFrozen(g):
    pieces = [p for p in g.board.pos.keys() if p.startswith(g.myTeam)]

    for piece in pieces:
        x = g.board.pos[piece][0]
        y = g.board.pos[piece][1]

        if 'P' in piece:
            if not CheckPawn(g, x, y):
                return False
        if 'H' in piece:
            if not CheckKnight(g, x, y):
                return False
                
        if 'S' in piece or 'Q' in piece:
            if not CheckDiagPaths(g, x, y):
                return False
                 
        if 'R' in piece or 'Q' in piece:
            if not CheckStraightPaths(g, x, y):
                return False

        if 'K' in piece:
            if not CheckKing(g, x, y):
                return False
    return True
