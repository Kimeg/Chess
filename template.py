from setting import *

class Piece:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.move_count = 0
        self.captured = []

    def Get(self):
        return [self.x, self.y, self.name, self.move_count, self.captured]
       
    def Capture(self, piece):
        self.captured.append(piece)
    
    def Set(self, piece):
        self.name = piece.name
        self.move_count = piece.move_count
        self.captured = piece.captured
        
    def Reset(self):
        self.name = ''
        self.move_count = 0
        self.captured = []

class Board:
    def __init__(self):
        self.pieces = {}
        self.pos = {}

        self.index = 0
        self.hist = {}
        self.piece_count = {}

        self.castling_rook = ''
        self.enpassant_pawn = ''
        self.promoted_pawn = ''

    def Initialize(self, board):
        for j, row in enumerate(board):
            for i, piece in enumerate(row):    
                self.pieces[(i,j)] = Piece(i, j, piece)

                name = self.pieces[(i,j)].name
                if not name == '':
                    self.pos[name] = [i, j]

                    if name[:-1] in self.piece_count.keys():
                        self.piece_count[name[:-1]] += 1
                    else:
                        self.piece_count[name[:-1]] = 1
        
    def Move(self, _from, _to):
        src = self.pieces[(_from[0], _from[1])]
        target = self.pieces[(_to[0], _to[1])]

        src.move_count += 1
        captured = ''

        if not target.name == '':
            captured = target.name
            src.Capture(target.name) 
            self.pos.pop(target.name, None)
            self.piece_count[target.name[:-1]] -= 1

        target.Set(src)
        self.pos[target.name] = [target.x, target.y]

        src.Reset()        
        self.index += 1
        self.hist[self.index] = {"Name":target.name, "From":_from, "To":_to, "Captured": captured,
                                 "CastlingRook": self.castling_rook, "EnpassantPawn": self.enpassant_pawn,
                                 "PromotedPawn": self.promoted_pawn}

        self.castling_rook = ''
        self.enpassant_pawn = ''
        self.promoted_pawn = ''

    def Set(self, board):
        self.hist = board.hist
        self.index = board.index
        self.piece_count = board.piece_count

class Game:
    def __init__(self, board, template):
        self.board = board
        self.template = template

        self.board.Initialize(self.template)

        self.myTeam = 'W'
        self.enemyTeam = 'B'

        self.msg = ''
        self.verbose = False
        self.status = ''

        self.is_frozen = False
        self.is_valid_move = False
        self.is_valid_enpassant = False
        self.is_valid_castling = False
        self.is_valid_promotion = False
        self.is_check = False
        self.is_checkmate = False
        self.is_stalemate = False

    def Update_Msg(self, msg):
        if self.verbose:
            self.msg = msg

    def Display(self):
        print('\n-------------------------------------------------')
        for j in range(8):
            row = '| '
            for i in range(8):
                if self.board.pieces[(i,7-j)].name == '':
                    row += self.board.pieces[(i,7-j)].name + '    | '
                    continue
                row += self.board.pieces[(i,7-j)].name + ' | '

            print(row)
            print('-------------------------------------------------')
        print('\n')

    def TestDisplay(self):
        print('\n-------------------------------------------------')
        for j in range(8):
            row = '| '
            for i in range(8):
                if self.temp.pieces[(i,7-j)].name == '':
                    row += self.temp.pieces[(i,7-j)].name + '    | '
                    continue
                row += self.temp.pieces[(i,7-j)].name + ' | '

            print(row)
            print('-------------------------------------------------')
        print('\n')
        
    def TakeTurn(self):
        if self.myTeam == 'W':
            self.myTeam = 'B'
            self.enemyTeam = 'W'
        else:
            self.myTeam = 'W'
            self.enemyTeam = 'B'

        print(self.myTeam + "'s turn to move.")

    def CheckPromotion(self):
        end = 7
        if self.myTeam == 'B':
            end = 0

        prev_piece = self.board.hist[self.board.index]
        if not (prev_piece["Name"].startswith(self.myTeam+'P') and prev_piece["To"][1] == end):
            return

        choices = [self.myTeam+'Q', self.myTeam+'R', self.myTeam+'S', self.myTeam+'H']
        promoted = False
        count = 0
        while not promoted:
            pawns = [self.board.pieces[(i,end)] for i in range(8) if self.board.pieces[(i,end)].name.startswith(self.myTeam+'P')]
            for i, pawn in enumerate(pawns):
                if count > 0:
                    new = 'Q'
                else:
                    new = input()

                for group, choice in zip(PROMOTION_PIECES, choices):
                    if new in group:
                        self.board.pos.pop(pawn.name, None)
                        self.board.piece_count[pawn.name[:-1]] -= 1
                        try:
                            self.board.piece_count[choice] += 1
                        except:
                            self.board.piece_count[choice] = 1

                        self.board.promoted_pawn = pawn.name
                        pawn.name = choice + str(self.board.piece_count[choice])
                        promoted = True
                        break
            count += 1

def Copy(g):
    board = Board() 
    #board.Initialize(g.template)

    for key in g.board.pieces.keys():
        p = g.board.pieces[key]
        board.pieces[key] = Piece(p.x, p.y, p.name)
        board.pieces[key].Set(p)
    
        board.Set(g.board)
        if not p.name == '':
            board.pos[p.name] = [p.x, p.y]
    return board
