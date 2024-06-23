import random
piece_value = {"K":0,"Q":900,"R":500,"B":300,"N":300,"p":100}
checkmate = float('inf')
stalemate = 0

scoring=[[0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01],
        [0.02,0.02,0.02,0.02,0.02,0.02,0.02,0.02],
        [0.02,0.02,0.03,0.03,0.03,0.03,0.02,0.02],
        [0.02,0.02,0.04,0.04,0.04,0.04,0.02,0.02],
        [0.02,0.02,0.04,0.04,0.04,0.04,0.02,0.02],
        [0.02,0.02,0.03,0.03,0.03,0.03,0.02,0.02],
        [0.02,0.02,0.02,0.02,0.02,0.02,0.02,0.02],
        [0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01]]

def find_minimax(game,board, turn,alpha,beta, depth):
    if (depth == 0 or game.game_over()):
        return None, get_score(game,board)
    elif (turn==False): 
        possibility = game.all_valid_moves(turn)
        max_score = float('-inf')
        bestmove = None
        for move in possibility:
            game.move_piece(move, False) 
            evaluation = find_minimax(game, board,not turn,alpha,beta, depth - 1) 
            game.undo_move(False)
            if (evaluation[1] > max_score):
                max_score = evaluation[1]
                bestmove = move
            alpha = max(evaluation[1],alpha)
            if(alpha>=beta):
                break
        return bestmove, max_score
    else:
        possibility = game.all_valid_moves(turn)
        min_score = float('inf')
        bestmove = None
        for move in possibility:
            game.move_piece(move, False) 
            evaluation = find_minimax(game, board,not turn,alpha,beta, depth - 1) 
            game.undo_move(False)
            if (evaluation[1] < min_score):
                min_score = evaluation[1]
                bestmove = move
            beta = min(evaluation[1],beta)
            if(beta<=alpha):
                break
        return bestmove, min_score

def get_score(game,board):
    for i in range(7):
        if(board[7][i]=="bp"):
            board[7][i]="bQ"
    if(game.is_checkmate("wK")):
        return checkmate
    elif(game.is_checkmate("bK")):
        return checkmate * -1
    elif(game.is_stalemate()):
        return stalemate
    score = 0
    for i in range(8):
        for j in range(8):
            if(board[i][j][0]=='w'):
                score-=piece_value[board[i][j][1]]
                if(board[i][j][1]!='K'):
                    score-=scoring[i][j]
                else:
                    score+=scoring[i][j]
            elif(board[i][j][0]=='b'):
                score+=piece_value[board[i][j][1]]
                if(board[i][j][1]!='K'):
                    score+=scoring[i][j]
                else:
                    score-=scoring[i][j]
    pos = game.king_position('b')
    if(pos==(0,6) or pos==(0,2)):
        score+=0.5
    return score