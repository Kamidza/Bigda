from typing import List

def fun(board: List[List]) -> str:
    # строки и столбцы на наличие победителя
    for i in range(3):

        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != '-':
            return f"{board[i][0]} wins!"
        # проверка колонок
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != '-':
            return f"{board[0][i]} wins!"
    
    # диагонали на победителя
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '-':
        return f"{board[0][0]} wins!"
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '-':
        return f"{board[0][2]} wins!"
    
    # не закончена ли доска
    for row in board:
        if '-' in row:
            return "unfinished!"
    
    return "draw!"

board_1 = [
    ['-', '-', 'o'],
    ['-', 'x', 'o'],
    ['x', 'o', 'x']
]
print(fun(board_1))  # "unfinished!"

board_2 = [
    ['-', '-', 'o'],
    ['-', 'o', 'o'],
    ['x', 'x', 'x']
]
print(fun(board_2))  # "x wins!"

board_3 = [
    ['x', 'o', 'x'],
    ['o', 'x', 'o'],
    ['o', 'x', 'o']
]
print(fun(board_3))  # "draw!"