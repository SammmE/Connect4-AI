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

def scoreBoard(agentColor: int) -> int:
    # return score of board for agent
    # score is number of 3 in a rows for agent minus number of 3 in a rows for opponent
    # 3 in a row is 100 points, 2 in a row is 10 points, 1 in a row is 1 point
    # 3 in a row is 100 points, 2 in a row is 10 points, 1 in a row is 1 point
    # check horizontal
    score = 0
    for row in board:
        for i in range(4):
            if row[i] == row[i+1] == row[i+2] == agentColor:
                score += 100
            elif row[i] == row[i+1] == row[i+2] != 0:
                score -= 100
            elif row[i] == row[i+1] == agentColor:
                score += 10
            elif row[i] == row[i+1] != 0:
                score -= 10
            elif row[i] == agentColor:
                score += 1
            elif row[i] != 0:
                score -= 1
    # check vertical
    for i in range(7):
        for j in range(3):
            if board[j][i] == board[j+1][i] == board[j+2][i] == agentColor:
                score += 100
            elif board[j][i] == board[j+1][i] == board[j+2][i] != 0:
                score -= 100
            elif board[j][i] == board[j+1][i] == agentColor:
                score += 10
            elif board[j][i] == board[j+1][i] != 0:
                score -= 10
            elif board[j][i] == agentColor:
                score += 1
            elif board[j][i] != 0:
                score -= 1
    
    # check diagonal
    for i in range(3):
        for j in range(4):
            if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == agentColor:
                score += 100
            elif board[i][j] == board[i+1][j+1] == board[i+2][j+2] != 0:
                score -= 100
            elif board[i][j] == board[i+1][j+1] == agentColor:
                score += 10
            elif board[i][j] == board[i+1][j+1] != 0:
                score -= 10
            elif board[i][j] == agentColor:
                score += 1
            elif board[i][j] != 0:
                score -= 1
    
    for i in range(3):
        for j in range(4):
            if board[i][j+3] == board[i+1][j+2] == board[i+2][j+1] == agentColor:
                score += 100
            elif board[i][j+3] == board[i+1][j+2] == board[i+2][j+1] != 0:
                score -= 100
            elif board[i][j+3] == board[i+1][j+2] == agentColor:
                score += 10
            elif board[i][j+3] == board[i+1][j+2] != 0:
                score -= 10
            elif board[i][j+3] == agentColor:
                score += 1
            elif board[i][j+3] != 0:
                score -= 1
    
    return score

def agentMove(agentColor: int) -> int:
    # return column to drop piece in
    # Get all possible moves for agent
    global board
    originalBoard = np.copy(board)

    possibleMoves = []
    for i in range(7):
        if dropPiece(i, agentColor):
            possibleMoves.append(i)
            board = np.copy(originalBoard)
    
    # score each move
    scores = []
    for move in possibleMoves:
        dropPiece(move, agentColor)
        scores.append(scoreBoard(agentColor))
        board = np.copy(originalBoard)
    
    # get opponent's best move
    opponentColor = 3 - agentColor
    oppPossibleMoves = []
    for i in range(7):
        if dropPiece(i, opponentColor):
            oppPossibleMoves.append(i)
            board = np.copy(originalBoard)
    
    # score each move
    opponentScores = []
    for move in oppPossibleMoves:
        dropPiece(move, opponentColor)
        opponentScores.append(scoreBoard(opponentColor))
        board = np.copy(originalBoard)
    
    # get opponent's best move
    opponentBestMove = oppPossibleMoves[opponentScores.index(max(opponentScores))]

    # if opponent has a winning move, block it
    if max(opponentScores) >= 100:
        return opponentBestMove
    
    # return move with highest score
    return possibleMoves[scores.index(max(scores))]

def playGame(isAgent: bool, agentColor: int = 0):
    turn = int(input("Who goes first? (1 for red, 2 for yellow): "))
    firstTurn = turn
    printBoard()
    while True:
        if isAgent and turn == agentColor:
            print("Agent's turn")
            print("Agent is thinking...")
            move = agentMove(agentColor)
            print("Agent dropped piece in column", move)
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