
"""

BoardStat - условное обозначение для определения расположения фигур на шахматной доске.
Используется стандартное шахматное расположение:
с лева направо обозначенное буквами a-h, снизу вверх цифрами 1-8
Также подразумевается стандартное начальное расположение, в котором
внизу (a1-h2) - белые фигуры, а наверху (a7-h8) - черные.

Для обозначения статуса в данном проекте применим
одну строку где через пробел указаны статусы каждого из 64 клеток:
цвет и название фигуры либо клетка пустая.
Порядок начинается с верхнего левого угла с лева на право до нижнего правого угла.

W - белый (white)
B - черный (black)

R = ладья (rook)
N = конь (knight)
B = слон (bishop)
Q = ферзь (queen)
K = король (king)
P = пешка (pawn)

0 = пусто

Cтартовый статус доски:
"br bn bb bq bk bb bn br
bp bp bp bp bp bp bp bp
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
wp wp wp wp wp wp wp wp
wr wn wb wq wk wb wn wr"

"""


# https://github.com/UmidSadatov/ChessModel.git

board_stat = ("br bn bb bq bk bb bn br "
              "bp bp bp bp bp bp bp bp "
              "00 00 00 00 00 00 00 00 "
              "00 00 00 wp 00 00 00 00 "
              "00 00 00 00 00 00 00 00 "
              "00 00 00 00 00 00 00 00 "
              "wp wp wp 00 wp wp wp wp "
              "wr wn wb wq wk wb wn wr")


board_stat_additional_data = {
    "check_to_white": False,  # Шах белому
    "mate_to_white": False,   # Мат белому
    "check_to_black": False,  # Шах черному
    "mate_to_black": False,   # Мат черному

    "white_can_castle_kingside": False,  # белый может сделать короткую рокировку
    "white_can_castle_queenside": False,  # белый может сделать длинную рокировку
    "black_can_castle_kingside": False,  # белый может сделать короткую рокировку
    "black_can_castle_queenside": False,  # белый может сделать длинную рокировку

    # Взятия на проходе
    # Например для белой пешки на f5: 
    # "Pf5xg6" - взятие на проходе черной пешки стоящей на g5, который последним сделал двойной ход с g7 на g5
    "en_passant_chance_for_white": [],    # шанс взятия на проходе для белого (белый может взять)    
    "en_passant_chance_for_black": []     # шанс взятия на проходе для черного (черный может взять)
}


def get_board_stat_dict(board_stat_str: str) -> dict:
    board_stat_dict = {}

    for letter in 'abcdefgh':
        for num in '12345678':
            board_stat_dict[letter + num] = None

    board_stat_list = board_stat_str.split(' ')

    for num in '87654321':
        for letter in 'abcdefgh':
            board_stat_dict[letter + num] = board_stat_list[0]
            board_stat_list = board_stat_list[1:]

    return board_stat_dict


def get_board_stat_str(board_stat_dict: dict) -> str:
    board_stat_str = ''
    for num in '87654321':
        for letter in 'abcdefgh':
            board_stat_str += board_stat_dict[letter + num] + ' '
    return board_stat_str[:-1]


def get_piece_in_cell(board_stat_str: str, cell: str) -> str:
    bsd = get_board_stat_dict(board_stat_str)
    return bsd[cell]


def remove_piece_in_cell_and_get_new_board_stat(board_stat_str: str, cell: str) -> str:
    # убираем фигуру, сделав заданную клетку пустым, возвращаем новое состояние доски
    bsd = get_board_stat_dict(board_stat_str)
    bsd[cell] = '00'
    bss = get_board_stat_str(bsd)
    return bss


def put_piece_in_cell_and_get_new_board_stat(board_stat_str: str, cell: str, piece: str) -> str:
    # ставим фигуру в заданную клетку 
    # (независимо какая была фигура до этого или была ли пустая данная клетка),
    # возвращаем новое состояние доски
    bsd = get_board_stat_dict(board_stat_str)
    bsd[cell] = piece
    bss = get_board_stat_str(bsd)
    return bss


def get_preliminary_moves_list_of_piece(board_stat_str: str, cell: str) -> list:
    #   получить ПРЕДВАРИТЕЛЬНЫЙ список возможных ходов фигуры 
    #   в заданной клетке при заданном состоянии доски
    #   без учета: шахов, взятий на проходе, рокировок

    moves_list_of_piece = []
    piece = get_piece_in_cell(board_stat_str, cell)

    # Ладья:
    if piece[1] == 'r':

        letters = 'abcdefgh'
        cur_let_indx = letters.index(cell[0])

        # направо:
        next_let_indx = cur_let_indx + 1
        while next_let_indx <= 7:
            next_letter = letters[next_let_indx]
            next_cell = f'{next_letter}{cell[1]}'
            next_piece = get_piece_in_cell(board_stat_str, next_cell)
            if next_piece == '00':
                # если след. клетка пустая
                moves_list_of_piece.append(f'R{cell}{next_cell}')
                next_let_indx += 1
            elif piece[0] != next_piece[0]:
                # если в след. клетке фигура оппонента (другого цвета)
                moves_list_of_piece.append(f'R{cell}x{next_cell}')
                break
            else:
                break

        # налево:
        prev_let_indx = cur_let_indx - 1
        while prev_let_indx >= 0:
            prev_letter = letters[prev_let_indx]
            prev_cell = f'{prev_letter}{cell[1]}'
            prev_piece = get_piece_in_cell(board_stat_str, prev_cell)
            if prev_piece == '00':
                # если пред. клетка пустая
                moves_list_of_piece.append(f'R{prev_cell}')
                prev_let_indx -= 1
            elif piece[0] != prev_piece[0]:
                # если в пред. клетке фигура оппонента (другого цвета)
                moves_list_of_piece.append(f'R{cell}x{prev_cell}')
                break
            else:
                break

        letter = cell[0]
        current_num = cell[1]

        # вверх
        upper_num = int(current_num) + 1
        while upper_num <= 8:
            upper_cell = f'{letter}{upper_num}'
            upper_piece = get_piece_in_cell(board_stat_str, upper_cell)
            if upper_piece == '00':
                # если верхняя клетка пустая
                moves_list_of_piece.append(f'R{cell}{upper_cell}')
                upper_num += 1
            elif piece[0] != upper_piece[0]:
                # если в верхней клетке фигура оппонента (другого цвета)
                moves_list_of_piece.append(f'R{cell}x{upper_cell}')
                break
            else:
                break

        #вниз
        lower_num = int(current_num) - 1
        while lower_num > 0:
            lower_cell = f'{letter}{lower_num}'
            lower_piece = get_piece_in_cell(board_stat_str, lower_cell)
            if lower_piece == '00':
                # если нижняя клетка пустая
                moves_list_of_piece.append(f'R{cell}{lower_cell}')
                lower_num -= 1
            elif piece[0] != lower_piece[0]:
                # если в нижней клетке фигура оппонента (другого цвета)
                moves_list_of_piece.append(f'R{cell}x{lower_cell}')
                break
            else:
                break


    # Слон:
    if piece[1] == 'b':
        letters = 'abcdefgh'

        cur_let_indx = letters.index(cell[0])
        cur_num = int(cell[1])

        # вверх-направо
        upper_num = int(cur_num) + 1
        next_let_indx = cur_let_indx + 1
        while upper_num <= 8 and next_let_indx <= 7:
            next_letter = letters[next_let_indx]
            upper_next_cell = f'{next_letter}{upper_num}'
            upper_next_piece = get_piece_in_cell(board_stat_str, upper_next_cell)
            if upper_next_piece == '00':
                # если верхняя-правая клетка пустая
                moves_list_of_piece.append(f'B{cell}{upper_next_cell}')
                next_let_indx += 1
                upper_num += 1
            elif piece[0] != upper_next_piece[0]:
                # если в верхней-правой клетке фигура оппонента (другого цвета)
                moves_list_of_piece.append(f'B{cell}x{upper_next_cell}')
                break
            else:
                break

        # вверх-налево
        upper_num = int(cur_num) + 1
        prev_let_indx = cur_let_indx - 1
        while upper_num <= 8 and prev_let_indx >= 0:
            prev_letter = letters[prev_let_indx]
            upper_prev_cell = f'{prev_letter}{upper_num}'
            upper_prev_piece = get_piece_in_cell(board_stat_str, upper_prev_cell)
            if upper_prev_piece == '00':
                # если верхняя-левая клетка пустая
                moves_list_of_piece.append(f'B{cell}{upper_prev_cell}')
                prev_let_indx -= 1
                upper_num += 1
            elif piece[0] != upper_prev_piece[0]:
                # если в верхней-левой клетке фигура оппонента (другого цвета)
                moves_list_of_piece.append(f'B{cell}x{upper_prev_cell}')
                break
            else:
                break

        # вниз-направо
        lower_num = int(cur_num) - 1
        next_let_indx = cur_let_indx + 1
        while lower_num > 0 and next_let_indx <= 7:
            next_letter = letters[next_let_indx]
            lower_next_cell = f'{next_letter}{lower_num}'
            lower_next_piece = get_piece_in_cell(board_stat_str, lower_next_cell)
            if lower_next_piece == '00':
                # если нижняя-правая клетка пустая
                moves_list_of_piece.append(f'B{cell}{lower_next_cell}')
                next_let_indx += 1
                lower_num -= 1
            elif piece[0] != lower_next_piece[0]:
                # если в нижней-правой клетке фигура оппонента (другого цвета)
                moves_list_of_piece.append(f'B{cell}x{lower_next_cell}')
                break
            else:
                break

        # вниз-налево
        lower_num = int(cur_num) - 1
        prev_let_indx = cur_let_indx - 1
        while lower_num > 0 and prev_let_indx >= 0:
            prev_letter = letters[prev_let_indx]
            lower_prev_cell = f'{prev_letter}{lower_num}'
            lower_prev_piece = get_piece_in_cell(board_stat_str, lower_prev_cell)
            if lower_prev_piece == '00':
                # если нижняя-левая клетка пустая
                moves_list_of_piece.append(f'B{cell}{lower_prev_cell}')
                prev_let_indx -= 1
                lower_num -= 1
            elif piece[0] != lower_prev_piece[0]:
                # если в нижней-левой клетке фигура оппонента (другого цвета)
                moves_list_of_piece.append(f'B{cell}x{lower_prev_cell}')
                break
            else:
                break

    # Конь
    if piece[1] == 'n':
        letters = 'abcdefgh'
        cur_let_indx = letters.index(cell[0])
        cur_num = int(cell[1])

        # один шаг вверх
        one_step_upper_num = cur_num + 1

        # два шага вверх
        two_steps_upper_num = cur_num + 2

        # один шаг вниз
        one_step_lower_num = cur_num - 1

        # два шага вниз
        two_steps_lower_num = cur_num - 2

        # один шаг направо
        one_step_right_let_indx = cur_let_indx + 1

        # два шага направо
        two_steps_right_let_indx = cur_let_indx + 2

        # один шаг налево
        one_step_left_let_indx = cur_let_indx - 1

        # два шага налево
        two_steps_left_let_indx = cur_let_indx - 2

        # список целевых (возможных) ходов коня, максимум 8
        target_cells = []

        # один шаг вверх
        if one_step_upper_num <= 8:

            # два шага вправо
            if two_steps_right_let_indx <= 7:
                two_steps_right_letter = letters[two_steps_right_let_indx]
                target_cell = f'{two_steps_right_letter}{one_step_upper_num}'
                target_cells.append(target_cell)
            # два шага влево
            if two_steps_left_let_indx >= 0:
                two_steps_left_letter = letters[two_steps_left_let_indx]
                target_cell = f'{two_steps_left_letter}{one_step_upper_num}'
                target_cells.append(target_cell)

            # два шага вверх
            if two_steps_upper_num <= 8:
                # один шаг вправо
                if one_step_right_let_indx <= 7:
                    one_step_right_letter = letters[one_step_right_let_indx]
                    target_cell = f'{one_step_right_letter}{two_steps_upper_num}'
                    target_cells.append(target_cell)
                # один шаг влево
                if one_step_left_let_indx >= 0:
                    one_step_left_letter = letters[one_step_left_let_indx]
                    target_cell = f'{one_step_left_letter}{two_steps_upper_num}'
                    target_cells.append(target_cell)

        # один шаг вниз
        if one_step_lower_num > 0:

            # два шага вправо
            if two_steps_right_let_indx <= 7:
                two_steps_right_letter = letters[two_steps_right_let_indx]
                target_cell = f'{two_steps_right_letter}{one_step_lower_num}'
                target_cells.append(target_cell)
            # два шага влево
            if two_steps_left_let_indx >= 0:
                two_steps_left_letter = letters[two_steps_left_let_indx]
                target_cell = f'{two_steps_left_letter}{one_step_lower_num}'
                target_cells.append(target_cell)

            # два шага вниз
            if two_steps_lower_num > 0:
                # один шаг вправо
                if one_step_right_let_indx <= 7:
                    one_step_right_letter = letters[one_step_right_let_indx]
                    target_cell = f'{one_step_right_letter}{two_steps_lower_num}'
                    target_cells.append(target_cell)
                # один шаг влево
                if one_step_left_let_indx >= 0:
                    one_step_left_letter = letters[one_step_left_let_indx]
                    target_cell = f'{one_step_left_letter}{two_steps_lower_num}'
                    target_cells.append(target_cell)

        for target_cell in target_cells:
            target_piece = get_piece_in_cell(board_stat_str, target_cell)
            if target_piece == '00':
                #если целевая клетка пустая
                moves_list_of_piece.append(f'N{cell}{target_cell}')
            elif piece[0] != target_piece[0]:
                # если в целевой клетке фигура оппонента
                moves_list_of_piece.append(f'N{cell}x{target_cell}')


    # Ферзь
    if piece[1] == 'q':
        # ходы Ладьи + ходы Слона (горизонтально, вертикально и по всем диагоналям)

        # Определим ходы по горизонтали и вертикали (как у Ладьи)
        # сначала создаем временную доску, заменяя Ферзь на Ладью (такого же цвета в той же клетке)
        temp_bss_for_hor_and_vert_moves = put_piece_in_cell_and_get_new_board_stat(board_stat_str, cell, f'{piece[0]}r')
        hor_and_vert_moves = get_preliminary_moves_list_of_piece(temp_bss_for_hor_and_vert_moves, cell)

        # Определим ходы по диагонялям (как у Слона)
        # сначала создаем временную доску, заменяя Ферзь на Слона (такого же цвета в той же клетке)
        temp_bss_for_diagonal_moves = put_piece_in_cell_and_get_new_board_stat(board_stat_str, cell, f'{piece[0]}b')
        diagonal_moves = get_preliminary_moves_list_of_piece(temp_bss_for_diagonal_moves, cell)

        # все ходы соберем в один список
        moves_list_of_piece = hor_and_vert_moves + diagonal_moves

        # первую букву всех ходов заменяем на Q (означающую Ферзь)
        moves_list_of_piece = [f'Q{move[1:]}' for move in moves_list_of_piece]


    # Король
    if piece[1] == 'k':

        letters = 'abcdefgh'
        cur_let_indx = letters.index(cell[0])

        left_let_indx = cur_let_indx - 1
        right_let_indx = cur_let_indx + 1

        upper_num = int(cell[1]) + 1
        lower_num = int(cell[1]) - 1

        target_cells = []

        if upper_num <= 8:
            target_cells.append(f'{cell[0]}{upper_num}')
            if left_let_indx >= 0:
                left_letter = letters[left_let_indx]
                target_cells.append(f'{left_letter}{upper_num}')
            if right_let_indx <= 7:
                right_letter = letters[right_let_indx]
                target_cells.append(f'{right_letter}{upper_num}')

        if left_let_indx >= 0:
            left_letter = letters[left_let_indx]
            target_cells.append(f'{left_letter}{cell[1]}')
        if right_let_indx <= 7:
            right_letter = letters[right_let_indx]
            target_cells.append(f'{right_letter}{cell[1]}')

        if lower_num > 0:
            target_cells.append(f'{cell[0]}{lower_num}')
            if left_let_indx >= 0:
                left_letter = letters[left_let_indx]
                target_cells.append(f'{left_letter}{lower_num}')
            if right_let_indx <= 7:
                right_letter = letters[right_let_indx]
                target_cells.append(f'{right_letter}{lower_num}')

        for target_cell in target_cells:
            target_piece = get_piece_in_cell(board_stat_str, target_cell)
            if target_piece == '00':
                # если целевая клетка пустая
                moves_list_of_piece.append(f'K{cell}{target_cell}')
            elif piece[0] != target_piece[0]:
                # если в целевой клетке находится фигура оппонента (другого цвета)
                moves_list_of_piece.append(f'K{cell}x{target_cell}')


    # Пешка
    if piece[1] == 'p':

        letters = 'abcdefgh'

        cur_letter = cell[0]
        cur_num = int(cell[1])

        cur_let_indx = letters.index(cur_letter)

        right_let_indx = cur_let_indx + 1
        left_let_indx = cur_let_indx - 1

        # для белой пешки
        if piece[0] == 'w':

            one_step_upper_num = cur_num + 1
            two_steps_upper_num = cur_num + 2

            if one_step_upper_num <= 8:

                one_step_upper_cell = f'{cur_letter}{one_step_upper_num}'
                one_step_upper_piece = get_piece_in_cell(board_stat_str, one_step_upper_cell)

                # если клетка на сверху (на одну клетку) пустая
                if one_step_upper_piece == '00':
                    # то можно сделать один ход (на одну клетку выше)
                    moves_list_of_piece.append(f'P{cell}{one_step_upper_cell}')

                    # если пешка находится во второй горизонтальной линии (в первоначальном состоянии)
                    if cur_num == 2:

                        two_steps_upper_cell = f'{cur_letter}{two_steps_upper_num}'
                        two_steps_upper_piece = get_piece_in_cell(board_stat_str, two_steps_upper_cell)
                        
                        #  и если клетка на две ступени выше пустая
                        if two_steps_upper_piece == '00':
                            # то можно сделать двойной ход (на две клетки выше)
                            moves_list_of_piece.append(f'P{cell}{two_steps_upper_cell}')
                    
                if right_let_indx <= 7:
                    right_letter = letters[right_let_indx]
                    upper_right_cell = f'{right_letter}{one_step_upper_num}'
                    upper_right_piece = get_piece_in_cell(board_stat_str, upper_right_cell)
                    if piece[0] != upper_right_piece[0] and upper_right_piece != '00':
                        moves_list_of_piece.append(f'P{cell}x{upper_right_cell}')

                if left_let_indx >= 0:
                    left_letter = letters[left_let_indx]
                    upper_left_cell = f'{left_letter}{one_step_upper_num}'
                    upper_left_piece = get_piece_in_cell(board_stat_str, upper_left_cell)
                    if piece[0] != upper_left_piece[0] and upper_left_piece != '00':
                        moves_list_of_piece.append(f'P{cell}x{upper_left_cell}')

        # для черной пешки
        elif piece[0] == 'b':

            one_step_lower_num = cur_num - 1
            two_steps_lower_num = cur_num - 2

            if one_step_lower_num > 0:
                one_step_lower_cell = f'{cur_letter}{one_step_lower_num}'
                one_step_lower_piece = get_piece_in_cell(board_stat_str, one_step_lower_cell)

                if one_step_lower_piece == '00':
                    moves_list_of_piece.append(f'P{cell}{one_step_lower_cell}')

                    if cur_num == 7:

                        two_steps_lower_cell = f'{cur_letter}{two_steps_lower_num}'
                        two_steps_lower_piece = get_piece_in_cell(board_stat_str, two_steps_lower_cell)

                        if two_steps_lower_piece == '00':
                            moves_list_of_piece.append(f'P{cell}{two_steps_lower_cell}')

                if right_let_indx <= 7:
                    right_letter = letters[right_let_indx]
                    lower_right_cell = f'{right_letter}{one_step_lower_num}'
                    lower_right_piece = get_piece_in_cell(board_stat_str, lower_right_cell)
                    if piece[0] != lower_right_piece[0] and lower_right_piece != '00':
                        moves_list_of_piece.append(f'P{cell}x{lower_right_cell}')

                if left_let_indx >= 0:
                    left_letter = letters[left_let_indx]
                    lower_left_cell = f'{left_letter}{one_step_lower_num}'
                    lower_left_piece = get_piece_in_cell(board_stat_str, lower_left_cell)
                    if piece[0] != lower_left_piece[0] and lower_left_piece != '00':
                        moves_list_of_piece.append(f'P{cell}x{lower_left_piece}')


    return moves_list_of_piece


def get_captured_piece_after_move(original_board_stat_str: str, move: str) -> str:
    if 'x' in move:
        captured_cell = move.split('x')[1]
        return get_piece_in_cell(original_board_stat_str, captured_cell)
    else:
        return '00'


def is_check_to_white(board_stat_str: str) -> bool:
    board_stat_dict = get_board_stat_dict(board_stat_str)
    for cell, piece in board_stat_dict.items():
        if piece[0] == 'b':
            preliminary_moves_list_of_piece = get_preliminary_moves_list_of_piece(board_stat_str, cell)
            for move in preliminary_moves_list_of_piece:                
                if 'x' in move:
                    captured_piece = get_captured_piece_after_move(board_stat_str, move)
                    if captured_piece == 'wk':
                        return True
    return False


def is_check_to_black(board_stat_str: str) -> bool:
    board_stat_dict = get_board_stat_dict(board_stat_str)
    for cell, piece in board_stat_dict.items():
        if piece[0] == 'w':
            preliminary_moves_list_of_piece = get_preliminary_moves_list_of_piece(board_stat_str, cell)
            for move in preliminary_moves_list_of_piece:                
                if 'x' in move:
                    captured_piece = get_captured_piece_after_move(board_stat_str, move)
                    if captured_piece == 'bk':
                        return True
    return False




    # blacks_preliminary_moves_list = get_preliminary_moves_list_of_piece()


def get_board_stat_after_move(original_board_stat_str: str, move: str, change_additional_data = True) -> str:

    if move not in get_preliminary_moves_list_of_piece(original_board_stat_str, move[1:3]):
        raise AttributeError(f"move {move} is impossible")

    # определим начальную и конечную клетку хода
    if 'x' in move[1:]:
        original_cell = move[1:].split('x')[0]
        new_cell = move[1:].split('x')[1]
    else:
        original_cell = move[1:3]
        new_cell = move[3:]

    # определим фигуру (какая фигура выполняет ход: ладья, конь, пешка ит.д.)
    moved_piece = get_piece_in_cell(original_board_stat_str, original_cell)

    # Первый этап: убираем из доски фигуру который ходит из клетки где она находится и записываем доску в новую переменную
    first_step_new_board = remove_piece_in_cell_and_get_new_board_stat(original_board_stat_str, original_cell)

    # Второй этап: ставим фигуру в нужную клетку доски записываем доску в новую переменную
    final_board = put_piece_in_cell_and_get_new_board_stat(first_step_new_board, new_cell, moved_piece)

    # получаем цвет фигуры который ходил
    piece = get_piece_in_cell(original_board_stat_str, move[1:3])
    color = 'white' if piece[0] == 'w' else 'black'

    # взятие на проходе:
    if move in board_stat_additional_data[f'en_passant_chance_for_{color}']:
        letter = move[1:].split('x')[1][0]
        num = move[1:].split('x')[0][1]
        final_board = remove_piece_in_cell_and_get_new_board_stat(final_board, f'{letter}{num}')
    
    if change_additional_data:
        # шанс взятия на проходе исчезает (независимо был ли он применен)
        board_stat_additional_data[f'en_passant_chance_for_{color}'] = []


    # При двойном ходе пешки при некоторых условиях даем противнику шанс на взятие на проходе:
    if move[0] == 'P':
        cur_let_indx = 'abcdefgh'.index(move[1])
        right_let_indx = cur_let_indx + 1
        left_let_indx = cur_let_indx - 1

        if color == 'white' and move[2] == '2' and move[4] == '4':
            if right_let_indx <= 7:
                right_letter = 'abcdefgh'.index(right_let_indx)
                right_cell = f'{right_letter}4'
                right_piece = get_piece_in_cell(final_board, right_cell)
                if right_piece == 'bp' and change_additional_data:
                    blacks_new_en_passant = f"P{right_cell}x{move[1]}3"
                    board_stat_additional_data['en_passant_chance_for_black'].append(blacks_new_en_passant)
            if left_let_indx >= 0:
                left_letter = 'abcdefgh'.index(left_let_indx)
                left_cell = f'{left_letter}4'
                left_piece = get_piece_in_cell(final_board, left_cell)
                if left_piece == 'bp' and change_additional_data:
                    blacks_new_en_passant = f"P{left_cell}x{move[1]}3"
                    board_stat_additional_data['en_passant_chance_for_black'].append(blacks_new_en_passant)
        
        elif color == 'black' and move[2] == '7' and move[4] == '5':
            if right_let_indx <= 7:
                right_letter = 'abcdefgh'[right_let_indx]
                right_cell = f'{right_letter}5'
                right_piece = get_piece_in_cell(final_board, right_cell)
                if right_piece == 'wp' and change_additional_data:
                    whites_new_en_passant = f"P{right_cell}x{move[1]}6"
                    board_stat_additional_data['en_passant_chance_for_white'].append(whites_new_en_passant)
            if left_let_indx >= 0:
                left_letter = 'abcdefgh'[left_let_indx]
                left_cell = f'{left_letter}5'
                left_piece = get_piece_in_cell(final_board, left_cell)
                if left_piece == 'wp' and change_additional_data:
                    whites_new_en_passant = f"P{left_cell}x{move[1]}6"
                    board_stat_additional_data['en_passant_chance_for_white'].append(whites_new_en_passant)       


    # Возвращаем полученную доску
    return final_board


def is_mate_to_white(board_stat_str: str) -> bool:
    if not is_check_to_white(board_stat_str):
        return False
    
    board_stat_dict = get_board_stat_dict(board_stat_str)
    for cell, piece in board_stat_dict.items():
        if piece[0] == 'w':
            preliminary_moves_list_of_piece = get_preliminary_moves_list_of_piece(board_stat_str, cell)
            for move in preliminary_moves_list_of_piece:
                new_board_str = get_board_stat_after_move(board_stat_str, move, change_additional_data=False)
                if not is_check_to_white(new_board_str):
                    return False

    return True


def is_mate_to_black(board_stat_str: str) -> bool:
    if not is_check_to_black(board_stat_str):
        return False
    
    board_stat_dict = get_board_stat_dict(board_stat_str)
    for cell, piece in board_stat_dict.items():
        if piece[0] == 'b':
            preliminary_moves_list_of_piece = get_preliminary_moves_list_of_piece(board_stat_str, cell)
            for move in preliminary_moves_list_of_piece:
                new_board_str = get_board_stat_after_move(board_stat_str, move, change_additional_data=False)
                if not is_check_to_black(new_board_str):
                    return False

    return True

# print(get_preliminary_moves_list_of_piece(board_stat, 'e3'))
# print(is_check_to_black(board_stat))
















