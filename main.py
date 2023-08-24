import numpy as np
from rich import print

board = np.zeros((6, 7), dtype=int)

def printBoard():
    # print red if 1's yellow if 2's and white if 0's
    for row in board:
        for col in row:
            if col == 1:
                print("[red]●[/red]", end=" ")
            elif col == 2:
                print("[yellow]●[/yellow]", end=" ")
            else:
                print("[white]○[/white]", end=" ")
        print()

def checkWin() -> int:
    # return zero if no winner, 1 if red wins, 2 if yellow wins
    # check horizontal
    for row in board:
        for i in range(4):
            if row[i] == row[i+1] == row[i+2] == row[i+3] != 0:
                return row[i]
    # check vertical
    for i in range(7):
        for j in range(3):
            if board[j][i] == board[j+1][i] == board[j+2][i] == board[j+3][i] != 0:
                return board[j][i]
    # check diagonal
    for i in range(3):
        for j in range(4):
            if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] != 0:
                return board[i][j]
    for i in range(3):
        for j in range(4):
            if board[i][j+3] == board[i+1][j+2] == board[i+2][j+1] == board[i+3][j] != 0:
                return board[i][j+3]
    return 0

def checkTie() -> bool:
    # return true if tie, false if not
    for row in board:
        for col in row:
            if col == 0:
                return False
    return True

def dropPiece(col: int, color: int) -> bool:
    # return true if successful, false if not
    if col < 0 or col > 6:
        return False
    for i in range(5, -1, -1):
        if board[i][col] == 0:
            board[i][col] = color
            return True
    return False

# Use a minimax algorithm to find the best move for the agent
def agentMove(color: int, depth: int = 4):
    # return the column the agent should drop its piece in
    # if no move is possible, return -1
    # get old board
    global board
    oldBoard = np.copy(board)

    # check if agent can win in one move
    for i in range(7):
        if dropPiece(i, color):
            if checkWin() == color:
                board = np.copy(oldBoard)
                return i
            board = np.copy(oldBoard)


    bestMove = np.random.randint(0, 7)
    randomMove = True
    bestScore = -100000000
    for i in range(7):
        if dropPiece(i, color):
            score = minimax(depth, False, -100000000, 100000000)
            board = np.copy(oldBoard)
            if score > bestScore:
                bestScore = score
                randomMove = False
                bestMove = i
    
    if bestMove != -1:
        randomMove = False

    return [bestMove, bestScore, randomMove]

def minimax(depth: int, isMaximizing: bool, alpha: int, beta: int) -> int:
    # return the score of the best move
    # if isMaximizing is true, return the highest score
    # if isMaximizing is false, return the lowest score
    # alpha and beta are used for alpha-beta pruning
    global board
    oldBoard = np.copy(board)

    if checkWin() == 1:
        return 100000000
    elif checkWin() == 2:
        return -100000000
    elif checkTie():
        return 0
    if depth == 0:
        return 0
    if isMaximizing:
        bestScore = -100000000
        for i in range(7):
            if dropPiece(i, 1):
                score = minimax(depth-1, False, alpha, beta)
                board = np.copy(oldBoard)
                bestScore = max(bestScore, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        return bestScore
    else:
        bestScore = 100000000
        for i in range(7):
            if dropPiece(i, 2):
                score = minimax(depth-1, True, alpha, beta)
                board = np.copy(oldBoard)
                bestScore = min(bestScore, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
        return bestScore

def playGame(isAgent: bool, agentColor: int = 0):
    turn = int(input("Who goes first? (1 for red, 2 for yellow): "))
    firstTurn = turn
    printBoard()
    while True:
        if isAgent and turn == agentColor:
            print("Agent's turn")
            print("Agent is thinking...")
            [move, score, isRandom] = agentMove(agentColor, 9)
            print("Agent dropped piece in column", move, "with score", score, end="")
            if isRandom:
                print(" (random move)")
            else:
                print()
            dropPiece(move, agentColor)
        elif isAgent and turn != agentColor:
            print("Your turn")
            move = int(input("What column do you want to drop your piece in? (0-6): "))
            dropPiece(move, 3-agentColor)
        else:
            if turn == 1:
                print("[red]Red's turn[/red]")
                move = int(input("What column do you want to drop your piece in? (0-6): "))
                dropPiece(move, 1)
            else:
                print("[yellow]Yellow's turn[/yellow]")
                move = int(input("What column do you want to drop your piece in? (0-6): "))
                dropPiece(move, 2)
        
        printBoard()
        
        if checkWin() == 1:
            print("[bold red]Red wins![/bold red]")
            break
        elif checkWin() == 2:
            print("[bold yellow]Yellow wins![bold yellow]")
            break
        elif checkTie():
            print("[bold white]Tie![/bold white]")
            break
    
        if turn == 1:
            turn = 2
        else:
            turn = 1

playGame(True, 1)