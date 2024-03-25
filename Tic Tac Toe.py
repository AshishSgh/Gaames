import numpy as np
def key_selector():
    keys = np.array(['0', 'X'])
    p = str.upper(input('Choose 0 or X: '))
    while p not in keys:
        print('Choose either 0 or X')
        p=str.upper(input('Choose 0 or X: '))
    c = keys[keys != p][0]
    return p,c


def player_turn(board,p):    
    row = input('Enter row ') 
    col = input('Enter column ') 
    if row not in ['1', '2', '3'] or col not in ['1', '2', '3']: 
        print('You gave invalid input')
        return player_turn(board, p)
    
    row = int(row) - 1
    col = int(col) - 1
    if board[row][col]!='':
        print("This position have aleready been used")
        return player_turn(board, p)
    else :
        board[row][col]=p
    return board


def game_state(board):          
    score = None
    empty_cell = np.count_nonzero(board == '')
    diag = board.diagonal()
    anti_diag = np.fliplr(board).diagonal()
    
    if empty_cell == 0:
        score = 0
    for i in range(3):
        row = board[i]
        col = board[:, i]    
        if np.all(row == p) or np.all(col == p) or np.all(diag == p) or np.all(anti_diag == p):
            score = empty_cell + 1
        if np.all(row == c) or np.all(col == c) or np.all(diag == c) or np.all(anti_diag == c):
            score = -1*(empty_cell + 1)
        
    return score


def outcomes(board, player):    #player = p or c
    next_branch = []
    if game_state(board) != None:
        next_branch.append(board)
    else:
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    dummy_board = np.copy(board)
                    dummy_board[i][j] = player
                    next_branch.append(dummy_board)
    return next_branch


def minimax(board, player):    #player = +1 is maximiser and -1 is minimiser
    next_branch = outcomes(board, player_minimax_map[player])
    scores = []
    
    for move in next_branch:
        if game_state(move) == None:
            scores.append(minimax(move, -1*player))
        else:
            scores.append(game_state(move))
            
    if player == 1:
        return max(scores)
    else:
        return min(scores)

    
def computer_turn(board, c):
    next_branch = outcomes(board,c)
    scores = np.array([])
    for move in next_branch:
        scores = np.append(scores, minimax(move, 1))
    
    for move,score in zip(next_branch, scores):
        if score == min(scores):
            best_move = move
            
    return best_move




#Main Game Loop
board = np.array([['','',''],['','',''],['','','']])
p,c = key_selector()

player_minimax_map = {1: p, -1: c}

while game_state(board) == None:
    print(board)
    board = player_turn(board, p)
    print(board)
    print("Computer's Turn")
    board = computer_turn(board, c)

if game_state(board) > 0:
    print('You Won')
if game_state(board) < 0:
    print('You Lost')
if game_state(board) == 0:
    print('Game Tied')
