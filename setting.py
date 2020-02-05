CHESS_BOARD = [ ['WR1','WH1','WS1','WQ1','WK1','WS2','WH2','WR2'],
                ['WP1','WP2','WP3','WP4','WP5','WP6','WP7','WP8'],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['BP1','BP2','BP3','BP4','BP5','BP6','BP7','BP8'],
                ['BR1','BH1','BS1','BQ1','BK1','BS2','BH2','BR2'] ]

CASTLING    = [ ['WR1','WH1','WS1','WQ1','WK1','WS2','WH2','WR2'],
                ['','','','','WQ2','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['BR1','BH1','BS1','BQ1','BK1','','','BR2'] ]

ENPASSANT   = [ ['','','','','WK1','','',''],
                ['WP1','WP2','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['BP1','BP2','','','','','',''],
                ['','','','','BK1','','',''] ]

CHECKMATE   = [ ['BK1','BQ1','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','WP1','','','BQ2',''],
                ['','','','','','','',''],
                ['','','','','','','','WK1'] ]

STALEMATE   = [ ['','','','','WK1','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','WQ1','',''],
                ['','','','','','','','BK1'] ]

PROMOTION   = [ ['','','','WR2','WK1','','',''],
                ['BP1','BP2','','WS1','WR1','','',''],
                ['','','WH2','WH1','WQ1','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['','','','','','','',''],
                ['WP2','','WP1','','','','BH2','BH3'],
                ['','','','','','','BH1','BK1'] ]

ENPASSANTCHECK = [['','','','','','','',''],
                  ['','','','','','','',''],
                  ['','','','','','','',''],
                  ['','','','WK1','','','',''],
                  ['','','','','','WP1','',''],
                  ['','','','','','','',''],
                  ['','','','','BP1','','',''],
                  ['','','','','','','','BK1'] ]

AIDEDCHECK = [['','','','','','','',''],
                  ['','','BR1','','','','',''],
                  ['','','','','','','',''],
                  ['','','','','','','',''],
                  ['','','','','','','',''],
                  ['','','','','BQ1','','',''],
                  ['','','','','','','',''],
                  ['','','','WK1','','','','BK1'] ]

PIN =            [['','','','','WK1','','',''],
                  ['','','','','','','',''],
                  ['','','','','WP1','','',''],
                  ['','','','','','BP1','',''],
                  ['','','','','','','',''],
                  ['','','','','','','BK1',''],
                  ['','','','','','','',''],
                  ['','','','','','','',''] ]

KING_PATHS = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1],[2,0],[-2,0]]
KNIGHT_PATHS = [[2,1],[1,2],[-1,2],[-2,1],[-2,-1],[-1,-2],[1,-2],[2,-1]]
DIAG_PATHS = [[1,1],[-1,1],[1,-1],[-1,-1]]
STRAIGHT_PATHS = [[0,1],[1,0],[0,-1],[-1,0]]

QUEEN = ['Q','q','Queen','QUEEN','queen']
ROOK = ['R','r','Rook','ROOK','rook','castle','CASTLE','Castle','c','C']
BISHOP = ['B','b','Bishop','bishop','BISHOP','s','S']
KNIGHT = ['K','k','knight','Knight','KNIGHT','horse','HORSE','Horse','h','H']
PROMOTION_PIECES = [QUEEN, ROOK, BISHOP, KNIGHT]

RANGE = list(range(8))
VALID_INPUT = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,
               'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8}
INPUT_MAPPING = {0: 'a', 1: 'b', 2: 'c', 3: 'd',
                 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

RESET = ['re','RE','Re','reset','Reset','RESET','Regame','REGAME','regame']
REGAME = ['y','Y','Yes','yes','YES']
QUIT = ['q','Q','Quit','QUIT','quit','exit','Exit','EXIT']
MSG = {'NoCas1': '\nNo castling : not in a standard game.\n',
       'NoCas2': '\nNo castling : King has moved at least once.\n',
       'NoCas3': '\nNo castling : Rook is not available\n',
       'NoCas4': '\nNo castling : Rook has moved at least once\n',
       'NoCas5': '\nNo castling : obstacle(s)\n',
       'NoCas6': '',
       'Cas' : '\nCastling\n',
       'NoEnp1' : "\nNo enpassant : opponent's piece at enpassant position is not a pawn.\n",
       'NoEnp2' : '\nNo enpassant : previously moved piece is not the enpassant piece\n',
       'NoEnp3' : "\nNo enpassant : opponent's pawn at enpassant location has moved more than once.\n",
       'NoEnp4' : "\nNo enpassant : my pawn is at wrong position for enpassant move.\n",
       'Enp' : "\nEnpassant\n",
       'ValidKnight' : "\nValid knight path\n",
       'InValidKnight' : "\nInvalid knight path\n",
       'PathDiag' : "\nValid diagonal path\n",
       'PathNotDiag' : "\nInvalid diagonal path\n",
       'PathDiagBlocked' : '',
       'PathStraight' : "\nValid straight path\n",
       'PathNotStraight' : "\nInvalid straight path\n",
       'PathStraightBlocked' : '',
       'ValidKing' : "\nValid king move\n",
       'InValidKing' : "\nInvalid king move\n",
       'PawnBackwards' : "\nPawn cannot move backwards\n",
       'PawnMultiple' : "\nPawn cannot move 3 or more blocks\n",
       'ValidPawn' : "\nValid pawn move\n",
       'PawnBlocked' : "\nPath is blocked by a piece.\n",
       'InvalidPawn' : "\nInvalid pawn move\n"}


'''
Left Castling

query = [[(2,7),(1,6)],
         [(1,7),(0,5)],        
         [(3,7),(2,6)],        
         [(4,7),(2,7)]]

Right Castling

query = [[(5,7),(6,6)],
         [(6,7),(5,5)],        
         [(4,7),(6,7)]]

Enpassant

query = [[(0,1), (0,3)],
         [(0,3), (0,4)],
         [(1,6), (1,4)],
         [(0,4), (1,5)]]

CheckMate

query = [[(4,1),(4,3)],
         [(4,6),(4,4)],        
         [(3,0),(7,4)],
         [(1,6),(1,4)],
         [(5,0),(2,3)],
         [(1,4),(2,3)],
         [(7,4),(5,6)]]

query = [[(4,1),(4,3)],
         [(5,6),(5,4)],        
         [(1,0),(2,3)],
         [(6,6),(6,4)],
         [(3,0),(7,4)]]

StaleMate

query = [[(4,0),(4,1)]]

Promotion

query = [[(0,6),(0,7)],
         [(2,6),(2,7)],
         [(0,7),(1,5)],
         [(2,7),(3,5)]]

EnpassantCheck

query = [[(4,6),(4,4)],
         [(5,4),(4,5)]]

'''
'''
    tol = 0.5
    g.Display()
    g.TakeTurn()

    count = 0
    t0 = time()
    while True:
        if time()-t0 > tol:
            t0 = time()
            Test(g, query[count][0], query[count][1])
            count += 1
            if IsGameOver(g):
                break
        if count == len(query):
            break
    '''