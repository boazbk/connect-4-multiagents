import numpy as np
import os
import sys
import math
import random
import time
from board import *
from bots import *

#pygame version number and welcome message hidden.
#os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

board = None
gb = None
game_over = False


# dev statement to turn of the UI when having a bot vs bot match
# turning UI off in this case helps improve the performance of the bots.
graphics = False

turn = random.randint(Board.PLAYER1_PIECE, Board.PLAYER2_PIECE)

def next_turn():
    global turn
    print(turn,end=" ")
    if turn == board.PLAYER1_PIECE:
        turn = board.PLAYER2_PIECE
    else:
        turn = board.PLAYER1_PIECE

def check_win(piece):
    if board.winning_move(piece):
        if graphics:
            gb.write_on_board("PLAYER " + str(piece) + " WINS!", PLAYER_COLOUR[piece - 1], 350, 50, 70, True)
            gb.update_gboard()
        print("\nPLAYER " + str(piece) + " WINS!")
        return piece
    
    if board.check_draw():
        if graphics:
            gb.write_on_board("IT'S A TIE!", gb.LIGHTBLUE, 350, 50, 70, True)
            gb.update_gboard()
        print("\n IT'S A TIE!")
        return True
    return False


def connect4(p1, p2, ui=True, noise = 0.0):
    global game_over, board, gb, graphics
    game_over = False
    graphics=ui

    board = Board(turn)
    #board.print_board()
    time_p1 = time_p2 = 0
    moves_count_p1 = moves_count_p2 = 0
    print("Starting game",p1,p2)
    winner = 0
    while not game_over:
        # Player1's Input
        start = time.perf_counter()
        if turn == board.PLAYER1_PIECE and not game_over:
            col = p1.get_move(board)
            # get random number between 0 and 1
            if random.random() < noise:
                options = [i for i in range(board.COLUMNS) if board.is_valid_location(i)]
                col = random.choice(options)

            if board.is_valid_location(col):
                board.drop_piece(col, board.PLAYER1_PIECE)
                moves_count_p1 += 1
                next_turn()
                winner = check_win(board.PLAYER1_PIECE)
                if winner != False:
                    game_over = True
                
        end = time.perf_counter()

        time_p1 += (end - start)

        # Player2's Input
        start = time.perf_counter()
        if turn == board.PLAYER2_PIECE and not game_over:
            col = p2.get_move(board)
            if random.random() < noise:
                options = [i for i in range(board.COLUMNS) if board.is_valid_location(i)]
                col = random.choice(options)


            if board.is_valid_location(col):
                board.drop_piece(col, board.PLAYER2_PIECE)
                moves_count_p2 += 1
                next_turn()
                winner = check_win(board.PLAYER2_PIECE)
                if winner != False:
                    game_over = True
                
        end = time.perf_counter()

        time_p2 += (end - start)

        if game_over:
            #pygame.time.wait(1000)

            print("\nPlayer 1")
            print("TIME: " + "{:.2f}".format(round(time_p1, 2)) + " seconds")
            print("MOVES: "+ str(moves_count_p1))
            print("\nPlayer 2")
            print("TIME: " + "{:.2f}".format(round(time_p2, 2)) + " seconds")
            print("MOVES: "+ str(moves_count_p2))
            return winner

