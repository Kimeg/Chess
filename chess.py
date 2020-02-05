from template import *
from time import time
from check import *
from IO import *
from setting import *
import numpy as np
import os

########################################
#### Developed by Kimeg ################
#### Contact : kimeg7@hanmail.net ######
#### Copyright 2020 ####################
########################################

def Test(g, src, target, taketurn = True):
    if src[0]==target[0] and src[1]==target[1]:
        print("Same location")
        return
    if g.board.pieces[target].name.startswith(g.myTeam):
        print("Cannot attack my piece.")
        return
    if g.board.pieces[target].name == '':
        print("empty cell.")
        return
    if IsValidMove(g, src, target):
        g.board.Move(src, target)
        g.CheckPromotion()
        if taketurn:
            g.TakeTurn()
    g.Display()
    return

def Display_Message(g):
    if not g.msg == '':
        captured = ''
        try:
            if not g.board.hist[g.board.index]["Captured"] == '':
                captured = ' (x' + g.board.hist[g.board.index]["Captured"] + ')'

            name = g.board.hist[g.board.index]["Name"]
            _from = g.board.hist[g.board.index]["From"]
            _to = g.board.hist[g.board.index]["To"]
            msg = MSG[g.msg] + INPUT_MAPPING[_from[0]]+str(_from[1]+1) + ' (' + name + ')' + ' -> ' + INPUT_MAPPING[_to[0]]+str(_to[1]+1) +  captured
        except:
            msg = MSG[g.msg]

        print(msg)
        g.msg = ''
    return

def main():
    print("############ Chess #############")
    print("This game is playable using cli.")
    print('\nreset : play new game\nexit : exit game\npiece name (ex. g2) : select piece to move or where to move.')
    print('\nNew Game\n')

    # various templates are available in setting.py
    board = CHESS_BOARD

    try:
        template = board
    except:
        template = CHESS_BOARD

    # initialize game with specified (or default) template
    g = Game(Board(), template)

    while True:
        g.Display()

        if IsGameOver(g):
            print(g.status)
            g.status = ''
            print('\nStart a new game? (Y/N)\n')
            regame = input()
        
            if regame in REGAME:
                print('\nNew Game\n')
                g = Game(Board(), template)
                continue

            print('\nExiting the game.\n')
            break

        Display_Message(g)
        result = IsValidInput(g)

        if result == False:
            continue
        elif result == 'exit':
            print('\nExiting the game.\n')
            break
        elif result == 'reset':
            print("\nNew Game\n")
            g = Game(Board(), template)
            continue

        src = result[0]
        target = result[1]

        g.verbose = False
        if IsValidMove(g, src, target):
            g.board.Move(src, target)
            g.CheckPromotion()
            g.TakeTurn()

    return

if __name__ == "__main__":
    main()
