import os
import pickle
import time

from sudoku.sudoku import Sudoku
from sudoku.solver import iter_solving_sudoku

# making dir for saves
if not os.path.exists('.//files'):
    os.mkdir('.//files')

# Type starting 1. game creating or 2. load another saved game
print('\tType:\nload <file name>\n\tor\nstart game')
print('>>>', end='    ')
while True:
    command = input().strip().lower().split()
    try:
        if command == ['start', 'game']:
            print('\tInput count known numbers')
            print('>>>', end='    ')
            count_known_number = int(input().strip())
            game = Sudoku(count_known_elem=count_known_number)
            break
        elif (command[0] == 'load'
        and os.path.exists('.//files//'+command[1]+'.pkl')):
            with open('.//files//'+command[1]+'.pkl', 'rb') as f:
                game = pickle.load(f)
            break
        raise ValueError
    except ValueError:
        print('\tTry again')
        print('>>>', end='    ')

# Game type people solve sudoku or computer solve
print('\tSelect game type:\n1\t(you play)\
\n2\t(computer play)\n\t(print 1 or 2):')
print('>>>', end='    ')
while True:
    try:
        input_game_type = int(input().strip())
        if input_game_type == 1:
            playing = True
            break
        elif input_game_type == 2:
            playing = False
            break
        raise ValueError
    except ValueError:
        print('\tTry again')
        print('>>>', end='    ')


def input_command():
    print('>>>', end='    ')
    i = input().strip().split()
    if i[0] == 'save':
        return None, i[1], None
    elif len(i) == 3 and all(map(str.isdigit, i)):
        return int(i[0]), int(i[1]), int(i[2])
    raise ValueError


if playing:
    game.show()
    print('\tInput\nsave path/for/save/name_file')
    while not game.end():
        try:
            i = input_command()
            if i[0] is None:
                game.save_game('.//files//'+i[1])
                break
            else:
                game.input_number(*i)
                game.show()
        except ValueError:
            print('\tType again')
            continue
else:
    game.show()
    for (i, j), value in iter_solving_sudoku(game.size, game.table):
        print(f'In (row {i}, col {j}) paste {value}')
        try:
            game.input_number(i, j, value, comp=True)
            game.show()
        except ValueError:
            pass
