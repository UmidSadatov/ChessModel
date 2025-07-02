import copy

# https://github.com/UmidSadatov/ChessModel.git

class ChessBoard:

    def __init__(self):
        # Состояние доски (расположение фигур на доске)
        self.board_stat = ("br bn bb bq bk bb bn br "
                           "bp bp bp bp bp bp bp bp "
                           "00 00 00 00 00 00 00 00 "
                           "00 00 00 00 00 00 00 00 "
                           "00 00 00 00 00 00 00 00 "
                           "00 00 00 00 00 00 00 00 "
                           "wp wp wp wp wp wp wp wp "
                           "wr wn wb wq wk wb wn wr")

        # Контекст (некоторые данные о текущем состоянии): возможности рокировки и взятий на проходе
        self.context = {
            "whites_chance_for_kingside_castling": True,  # у белых есть шанс на короткую рокировку при подходящей позиции
            "whites_chance_for_queenside_castling": True,  # у белых есть шанс на длинную рокировку при подходящей позиции

            "blacks_chance_for_kingside_castling": True,  # у черных есть шанс на короткую рокировку при подходящей позиции
            "blacks_chance_for_queenside_castling": True,  # у черных есть шанс на длинную рокировку при подходящей позиции

            # Взятия на проходе
            # Например для белой пешки на f5:
            # "Pf5xg6" - взятие на проходе черной пешки стоящей на g5, который последним сделал двойной ход с g7 на g5
            "en_passant_chance_for_white": [],    # шанс взятия на проходе для белого (белый может взять)
            "en_passant_chance_for_black": [],     # шанс взятия на проходе для черного (черный может взять)

            # Чей ход: 'white' - ход белых, 'black' - ход черных
            "current_player_color": 'white'
        }

        # Количество полуходов: ходов подряд без взятия и без хода пешкой
        # обнуляется при ходе пешкой или взятии
        # при 50 или более: любой игрок имеет право потребовать ничью
        # а при 75: автоничья
        self.halfmove_clock = 0

        # Список состояний и контекстов доски
        # При троекратном повторении: любой игрок имеет право потребовать ничью
        self.stats_list = [[self.board_stat, self.context]]

    # перевести состояние доски из строчного вида в словарь
    def get_board_stat_dict(self) -> dict:
        board_stat_dict = {}

        for letter in 'abcdefgh':
            for num in '12345678':
                board_stat_dict[letter + num] = None

        board_stat_list = self.board_stat.split(' ')

        for num in '87654321':
            for letter in 'abcdefgh':
                board_stat_dict[letter + num] = board_stat_list[0]
                board_stat_list = board_stat_list[1:]

        return board_stat_dict

    # перевести состояние доски из словаря в строку
    def get_board_stat_from_dict(self, board_stat_dict:dict):
        board_stat_str = ''
        for num in '87654321':
            for letter in 'abcdefgh':
                board_stat_str += board_stat_dict[letter + num] + ' '
        self.board_stat = board_stat_str[:-1]

    # показать доску
    def show(self):
        stat_list = self.board_stat.split(' ')
        print(' '.join(stat_list[:8]))
        print(' '.join(stat_list[8:16]))
        print(' '.join(stat_list[16:24]))
        print(' '.join(stat_list[24:32]))
        print(' '.join(stat_list[32:40]))
        print(' '.join(stat_list[40:48]))
        print(' '.join(stat_list[48:56]))
        print(' '.join(stat_list[56:]))

    # получить фигуру в заданной клетке
    def get_piece_in_cell(self, cell: str) -> str:
        bsd = self.get_board_stat_dict()
        return bsd[cell]
        # try:
        #     return bsd[cell]
        # except KeyError:
        #     for key, value in bsd.items():
        #         print(f'{key}: {value}')
        #     print(cell)

    # сделать заданную клетку пустым (убрать фигуру)
    def remove_piece_in_cell(self, cell: str):
        # убираем фигуру, сделав заданную клетку пустым, возвращаем новое состояние доски
        bsd = self.get_board_stat_dict()
        bsd[cell] = '00'
        self.get_board_stat_from_dict(bsd)

    # поставить заданную фигуру в заданную клетку
    def put_piece_in_cell(self, cell: str, piece: str):
        # ставим фигуру в заданную клетку
        # (независимо какая была фигура до этого или была ли пустая данная клетка),
        # возвращаем новое состояние доски
        bsd = self.get_board_stat_dict()
        bsd[cell] = piece
        self.get_board_stat_from_dict(bsd)

    # получить предварительный список возможных ходов, включая взятия
    def get_preliminary_moves_list_of_piece(self, cell: str) -> list:
        #   получить ПРЕДВАРИТЕЛЬНЫЙ список возможных ходов фигуры
        #   в заданной клетке при заданном состоянии доски
        #   без учета возможных шахов

        moves_list_of_piece = []
        piece = self.get_piece_in_cell(cell)

        # Ладья:
        if piece[1] == 'r':

            letters = 'abcdefgh'
            cur_let_indx = letters.index(cell[0])

            # направо:
            next_let_indx = cur_let_indx + 1
            while next_let_indx <= 7:
                next_letter = letters[next_let_indx]
                next_cell = f'{next_letter}{cell[1]}'
                next_piece = self.get_piece_in_cell(next_cell)
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
                prev_piece = self.get_piece_in_cell(prev_cell)
                if prev_piece == '00':
                    # если пред. клетка пустая
                    moves_list_of_piece.append(f'R{cell}{prev_cell}')
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
                upper_piece = self.get_piece_in_cell(upper_cell)
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

            # вниз
            lower_num = int(current_num) - 1
            while lower_num > 0:
                lower_cell = f'{letter}{lower_num}'
                lower_piece = self.get_piece_in_cell(lower_cell)
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
        elif piece[1] == 'b':
            letters = 'abcdefgh'

            cur_let_indx = letters.index(cell[0])
            cur_num = int(cell[1])

            # вверх-направо
            upper_num = int(cur_num) + 1
            next_let_indx = cur_let_indx + 1
            while upper_num <= 8 and next_let_indx <= 7:
                next_letter = letters[next_let_indx]
                upper_next_cell = f'{next_letter}{upper_num}'
                upper_next_piece = self.get_piece_in_cell(upper_next_cell)
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
                upper_prev_piece = self.get_piece_in_cell(upper_prev_cell)
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
                lower_next_piece = self.get_piece_in_cell(lower_next_cell)
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
                lower_prev_piece = self.get_piece_in_cell(lower_prev_cell)
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
        elif piece[1] == 'n':
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
                target_piece = self.get_piece_in_cell(target_cell)
                if target_piece == '00':
                    # если целевая клетка пустая
                    moves_list_of_piece.append(f'N{cell}{target_cell}')
                elif piece[0] != target_piece[0]:
                    # если в целевой клетке фигура оппонента
                    moves_list_of_piece.append(f'N{cell}x{target_cell}')

        # Ферзь
        elif piece[1] == 'q':
            # ходы Ладьи + ходы Слона (горизонтально, вертикально и по всем диагоналям)

            # Определим ходы по горизонтали и вертикали (как у Ладьи)
            # сначала заменяем Ферзь на Ладью (такого же цвета в той же клетке)
            self.put_piece_in_cell(cell, f'{piece[0]}r')
            hor_and_vert_moves = self.get_preliminary_moves_list_of_piece(cell)

            # Определим ходы по диагонялям (как у Слона)
            # сначала заменяем Ферзь на Слона (такого же цвета в той же клетке)
            self.put_piece_in_cell(cell, f'{piece[0]}b')
            diagonal_moves = self.get_preliminary_moves_list_of_piece(cell)

            # Обратно поставим Ферзь в эту клетку
            self.put_piece_in_cell(cell, f'{piece[0]}q')

            # все ходы соберем в один список
            moves_list_of_piece = hor_and_vert_moves + diagonal_moves

            # первую букву всех ходов заменяем на Q (означающую Ферзь)
            moves_list_of_piece = [f'Q{move[1:]}' for move in moves_list_of_piece]

        # Король
        elif piece[1] == 'k':

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
                target_piece = self.get_piece_in_cell(target_cell)
                if target_piece == '00':
                    # если целевая клетка пустая
                    moves_list_of_piece.append(f'K{cell}{target_cell}')
                elif piece[0] != target_piece[0]:
                    # если в целевой клетке находится фигура оппонента (другого цвета)
                    moves_list_of_piece.append(f'K{cell}x{target_cell}')

            # РОКИРОВКА (при подходящей позиции):

            # для белого
            if piece == 'wk' and cell == 'e1':
                # короткая
                if \
                        self.get_piece_in_cell('f1') == '00' and \
                                self.get_piece_in_cell('g1') == '00' and \
                                self.get_piece_in_cell('h1') == 'wr':
                    moves_list_of_piece.append('Ke1<O-O>')
                # длинная
                if \
                        self.get_piece_in_cell('d1') == '00' and \
                                self.get_piece_in_cell('c1') == '00' and \
                                self.get_piece_in_cell('b1') == '00' and \
                                self.get_piece_in_cell('a1') == 'wr':
                    moves_list_of_piece.append('Ke1<O-O-O>')

            # для черного
            elif piece == 'bk' and cell == 'e8':
                # короткая
                if \
                        self.get_piece_in_cell('f8') == '00' and \
                                self.get_piece_in_cell('g8') == '00' and \
                                self.get_piece_in_cell('h8') == 'br':
                    moves_list_of_piece.append('Ke8<O-O>')
                # длинная
                if \
                        self.get_piece_in_cell('d8') == '00' and \
                                self.get_piece_in_cell('c8') == '00' and \
                                self.get_piece_in_cell('b8') == '00' and \
                                self.get_piece_in_cell('a8') == 'br':
                    moves_list_of_piece.append('Ke8<O-O-O>')

        # Пешка
        elif piece[1] == 'p':

            letters = 'abcdefgh'

            cur_letter = cell[0]
            cur_num = int(cell[1])

            cur_let_indx = letters.index(cur_letter)

            right_let_indx = cur_let_indx + 1
            left_let_indx = cur_let_indx - 1

            pawn_promotion_pieces = ['Q', 'N', 'B', 'R']

            # для белой пешки
            if piece[0] == 'w':

                one_step_upper_num = cur_num + 1
                two_steps_upper_num = cur_num + 2

                if one_step_upper_num < 8:

                    one_step_upper_cell = f'{cur_letter}{one_step_upper_num}'
                    one_step_upper_piece = self.get_piece_in_cell(one_step_upper_cell)

                    # если клетка сверху (на одну клетку выше) пустая
                    if one_step_upper_piece == '00':
                        # то можно сделать один ход (на одну клетку выше)
                        moves_list_of_piece.append(f'P{cell}{one_step_upper_cell}')

                        # если пешка находится во второй горизонтальной линии (в первоначальном состоянии)
                        if cur_num == 2:

                            two_steps_upper_cell = f'{cur_letter}{two_steps_upper_num}'
                            two_steps_upper_piece = self.get_piece_in_cell(two_steps_upper_cell)

                            #  и если клетка на две ступени выше пустая
                            if two_steps_upper_piece == '00':
                                # то можно сделать двойной ход (на две клетки выше)
                                moves_list_of_piece.append(f'P{cell}{two_steps_upper_cell}')

                    # если данная фигура не в самом правом краю доски
                    if right_let_indx <= 7:
                        # определим в какой горизонтали (букве)
                        right_letter = letters[right_let_indx]
                        upper_right_cell = f'{right_letter}{one_step_upper_num}'
                        upper_right_piece = self.get_piece_in_cell(upper_right_cell)
                        # если сверху справа находится фигура оппонента (другого цвета)
                        if piece[0] != upper_right_piece[0] and upper_right_piece != '00':
                            # то добавим взятие как возможный ход
                            moves_list_of_piece.append(f'P{cell}x{upper_right_cell}')

                        # ВЗЯТИЕ НА ПРОХОДЕ В ПРАВУЮ СТОРОНУ
                        # если данная белая пешка находится в 5-ой горизонтали, сверху-справа пусто
                        # и справа от него находится черная пешка
                        if cur_num == 5 and upper_right_piece == '00':
                            right_cell = f'{right_letter}5'
                            right_piece = self.get_piece_in_cell(right_cell)
                            if right_piece == 'bp':
                                moves_list_of_piece.append(f'P{cell}x{upper_right_cell}EP')

                    # если эта фигура не в самом левом краю доски
                    if left_let_indx >= 0:
                        left_letter = letters[left_let_indx]
                        upper_left_cell = f'{left_letter}{one_step_upper_num}'
                        # определим фигуру сверху-слева
                        upper_left_piece = self.get_piece_in_cell(upper_left_cell)
                        # если слева-сверху фигура оппонента (другого цвета)
                        if piece[0] != upper_left_piece[0] and upper_left_piece != '00':
                            # то учтем взятие как ход
                            moves_list_of_piece.append(f'P{cell}x{upper_left_cell}')

                        # ВЗЯТИЕ НА ПРОХОДЕ В ЛЕВУЮ СТОРОНУ
                        # если данная белая пешка находится в 5-ой горизонтали, сверху-слева пусто
                        # и слева от него находится черная пешка
                        if cur_num == 5 and upper_left_piece == '00':
                            left_cell = f'{left_letter}5'
                            left_piece = self.get_piece_in_cell(left_cell)
                            if left_piece == 'bp':
                                moves_list_of_piece.append(f'P{cell}x{upper_left_cell}EP')

                # превращение (в ферзя, коня, слона или ладью)
                elif one_step_upper_num == 8:
                    one_step_upper_cell = f'{cur_letter}{one_step_upper_num}'
                    one_step_upper_piece = self.get_piece_in_cell(one_step_upper_cell)
                    if one_step_upper_piece == '00':
                        for ppp in pawn_promotion_pieces:
                            moves_list_of_piece.append(f'P{cell}{one_step_upper_cell}{ppp}')

                    # если данная фигура не в самом правом краю доски
                    if right_let_indx <= 7:
                        # определим в какой горизонтали (букве)
                        right_letter = letters[right_let_indx]
                        upper_right_cell = f'{right_letter}{one_step_upper_num}'
                        upper_right_piece = self.get_piece_in_cell(upper_right_cell)
                        # если сверху справа находится фигура оппонента (другого цвета)
                        if piece[0] != upper_right_piece[0] and upper_right_piece != '00':
                            # то добавим взятие как возможный ход с превращением
                            for ppp in pawn_promotion_pieces:
                                moves_list_of_piece.append(f'P{cell}x{upper_right_cell}{ppp}')

                    # если эта фигура не в самом левом краю доски
                    if left_let_indx >= 0:
                        left_letter = letters[left_let_indx]
                        upper_left_cell = f'{left_letter}{one_step_upper_num}'
                        # определим фигуру сверху-слева
                        upper_left_piece = self.get_piece_in_cell(upper_left_cell)
                        # если слева-сверху фигура оппонента (другого цвета)
                        if piece[0] != upper_left_piece[0] and upper_left_piece != '00':
                            # то учтем взятие как ход с превращением пешки
                            for ppp in pawn_promotion_pieces:
                                moves_list_of_piece.append(f'P{cell}x{upper_left_cell}{ppp}')


            # для черной пешки
            elif piece[0] == 'b':

                one_step_lower_num = cur_num - 1
                two_steps_lower_num = cur_num - 2

                if one_step_lower_num > 1:
                    one_step_lower_cell = f'{cur_letter}{one_step_lower_num}'
                    one_step_lower_piece = self.get_piece_in_cell(one_step_lower_cell)

                    if one_step_lower_piece == '00':
                        moves_list_of_piece.append(f'P{cell}{one_step_lower_cell}')

                        if cur_num == 7:

                            two_steps_lower_cell = f'{cur_letter}{two_steps_lower_num}'
                            two_steps_lower_piece = self.get_piece_in_cell(two_steps_lower_cell)

                            if two_steps_lower_piece == '00':
                                moves_list_of_piece.append(f'P{cell}{two_steps_lower_cell}')

                    if right_let_indx <= 7:
                        right_letter = letters[right_let_indx]
                        lower_right_cell = f'{right_letter}{one_step_lower_num}'
                        lower_right_piece = self.get_piece_in_cell(lower_right_cell)
                        if piece[0] != lower_right_piece[0] and lower_right_piece != '00':
                            moves_list_of_piece.append(f'P{cell}x{lower_right_cell}')

                        # ВЗЯТИЕ НА ПРОХОДЕ В ПРАВУЮ СТОРОНУ
                        # если данная черная пешка находится в 4-ой горизонтали, снизу-справа пусто
                        # и справа от него находится белая пешка
                        if cur_num == 4 and lower_right_piece == '00':
                            right_cell = f'{right_letter}4'
                            right_piece = self.get_piece_in_cell(right_cell)
                            if right_piece == 'wp':
                                moves_list_of_piece.append(f'P{cell}x{lower_right_cell}EP')

                    if left_let_indx >= 0:
                        left_letter = letters[left_let_indx]
                        lower_left_cell = f'{left_letter}{one_step_lower_num}'
                        lower_left_piece = self.get_piece_in_cell(lower_left_cell)
                        if piece[0] != lower_left_piece[0] and lower_left_piece != '00':
                            moves_list_of_piece.append(f'P{cell}x{lower_left_cell}')

                        # ВЗЯТИЕ НА ПРОХОДЕ В ЛЕВУЮ СТОРОНУ
                        # если данная черная пешка находится в 4-ой горизонтали, снизу-слева пусто
                        # и слева от него находится белая пешка
                        if cur_num == 4 and lower_left_piece == '00':
                            left_cell = f'{left_letter}4'
                            left_piece = self.get_piece_in_cell(left_cell)
                            if left_piece == 'wp':
                                moves_list_of_piece.append(f'P{cell}x{lower_left_cell}EP')

                # превращение (в ферзя, коня, слона или ладью)
                elif one_step_lower_num == 1:
                    one_step_lower_cell = f'{cur_letter}{one_step_lower_num}'
                    one_step_lower_piece = self.get_piece_in_cell(one_step_lower_cell)

                    if one_step_lower_piece == '00':
                        for ppp in pawn_promotion_pieces:
                            moves_list_of_piece.append(f'P{cell}{one_step_lower_cell}{ppp}')

                    if right_let_indx <= 7:
                        right_letter = letters[right_let_indx]
                        lower_right_cell = f'{right_letter}{one_step_lower_num}'
                        lower_right_piece = self.get_piece_in_cell(lower_right_cell)

                        if piece[0] != lower_right_piece[0] and lower_right_piece != '00':
                            for ppp in pawn_promotion_pieces:
                                moves_list_of_piece.append(f'P{cell}x{lower_right_cell}{ppp}')

                    if left_let_indx >= 0:
                        left_letter = letters[left_let_indx]
                        lower_left_cell = f'{left_letter}{one_step_lower_num}'
                        lower_left_piece = self.get_piece_in_cell(lower_left_cell)
                        if piece[0] != lower_left_piece[0] and lower_left_piece != '00':
                            for ppp in pawn_promotion_pieces:
                                moves_list_of_piece.append(f'P{cell}x{lower_left_cell}{ppp}')

        return moves_list_of_piece

    def change_current_player_color(self):
        self.context['current_player_color'] = 'black' \
            if self.context['current_player_color'] == 'white' \
            else 'white'

    # получить какая фигура будет взята при ходе
    def get_captured_piece(self, move: str) -> str:
        if 'x' in move:
            if move[-2:] == 'EP':
                cells = move[1:-2].split('x')
                original_cell, new_cell = cells[0], cells[1]
                captured_cell = f'{new_cell[0]}{original_cell[1]}'
                return self.get_piece_in_cell(captured_cell)
            else:
                captured_cell = move.split('x')[1][:3]
                # if captured_cell == 'wp':
                #     print(move)
                return self.get_piece_in_cell(captured_cell)
        else:
            return '00'

    # сделать ход (изменить состояние доски и контекст)
    def make_considered_move(self, move: str):
        original_cell = move[1:3]
        piece = self.get_piece_in_cell(original_cell)
        mover_color = 'white' if piece[0] == 'w' else 'black'

        pawn_promotion_piece = None

        # если нет этого хода
        if move not in self.get_preliminary_moves_list_of_piece(move[1:3]):
            raise AttributeError(f"move {move} is impossible")

        # если это рокировка
        elif 'O-O' in move:
            # короткая рокировка белого короля
            if move == 'Ke1<O-O>':
                self.remove_piece_in_cell('e1')
                self.remove_piece_in_cell('h1')
                self.put_piece_in_cell('g1', 'wk')
                self.put_piece_in_cell('f1', 'wr')

            # длинная рокировка белого короля
            elif move == 'Ke1<O-O-O>':
                self.remove_piece_in_cell('e1')
                self.remove_piece_in_cell('a1')
                self.put_piece_in_cell('c1', 'wk')
                self.put_piece_in_cell('d1', 'wr')

            # короткая рокировка черного короля
            elif move == 'Ke8<O-O>':
                self.remove_piece_in_cell('e8')
                self.remove_piece_in_cell('h8')
                self.put_piece_in_cell('g8', 'bk')
                self.put_piece_in_cell('f8', 'br')

            # длинная рокировка черного короля
            elif move == 'Ke8<O-O-O>':
                self.remove_piece_in_cell('e8')
                self.remove_piece_in_cell('a8')
                self.put_piece_in_cell('c8', 'bk')
                self.put_piece_in_cell('d8', 'br')

        else:

            # определим начальную и конечную клетку хода
            if 'x' in move[1:]:

                if move[-2:] == 'EP':
                    cells = move[1:-2].split('x')
                    original_cell, target_cell = cells[0], cells[1]
                    en_passant_captured_cell = f'{target_cell[0]}{original_cell[1]}'
                    self.remove_piece_in_cell(en_passant_captured_cell)

                elif move[0] == 'P' and move[-1] in ['Q', 'N', 'B', 'R']:
                    pawn_promotion_piece = move[-1]
                    cells = move[1:-1].split('x')
                    original_cell, target_cell = cells[0], cells[1]
                else:
                    cells = move[1:].split('x')
                    original_cell, target_cell = cells[0], cells[1]

            else:
                if move[0] == 'P' and move[-1] in ['Q', 'N', 'B', 'R']:
                    pawn_promotion_piece = move[-1]
                    original_cell, target_cell = move[1:3], move[3:5]
                else:
                    original_cell = move[1:3]
                    target_cell = move[3:]

            # определим фигуру (какая фигура выполняет ход: ладья, конь, пешка ит.д.)
            moved_piece = self.get_piece_in_cell(original_cell)

            # Первый этап: убираем из доски фигуру который ходит из клетки где она находится
            self.remove_piece_in_cell(original_cell)

            # Второй этап: ставим фигуру в нужную клетку доски
            if pawn_promotion_piece is None:
                self.put_piece_in_cell(target_cell, moved_piece)
            else:
                self.put_piece_in_cell(target_cell, f'{moved_piece[0]}{pawn_promotion_piece.lower()}')

            if move[0] == 'P':
                letters = 'abcdefgh'
                if original_cell[1] == '2' and target_cell[1] == '4' and original_cell[0] == target_cell[0] and mover_color == 'white':
                    right_let_indx = letters.index(target_cell[0]) + 1
                    left_let_indx = letters.index(target_cell[0]) - 1
                    if right_let_indx <= 7:
                        right_letter = letters[right_let_indx]
                        right_cell = f'{right_letter}4'
                        if self.get_piece_in_cell(right_cell) == 'bp':
                            self.context[f'en_passant_chance_for_black'].append(f'P{right_cell}x{target_cell[0]}3EP')
                    if left_let_indx >=0:
                        left_letter = letters[left_let_indx]
                        left_cell = f'{left_letter}4'
                        if self.get_piece_in_cell(left_cell) == 'bp':
                            self.context[f'en_passant_chance_for_black'].append(f'P{left_cell}x{target_cell[0]}3EP')

                elif original_cell[1] == '7' and target_cell[1] == '5' and original_cell[0] == target_cell[0] and mover_color == 'black':
                    right_let_indx = letters.index(target_cell[0]) + 1
                    left_let_indx = letters.index(target_cell[0]) - 1
                    if right_let_indx <= 7:
                        right_letter = letters[right_let_indx]
                        right_cell = f'{right_letter}5'
                        if self.get_piece_in_cell(right_cell) == 'wp':
                            self.context[f'en_passant_chance_for_white'].append(f'P{right_cell}x{target_cell[0]}6EP')
                    if left_let_indx >= 0:
                        left_letter = letters[left_let_indx]
                        left_cell = f'{left_letter}5'
                        if self.get_piece_in_cell(left_cell) == 'wp':
                            self.context[f'en_passant_chance_for_white'].append(f'P{left_cell}x{target_cell[0]}6EP')

            elif move[0] == 'R':
                original_cell = move[1:3]
                if original_cell == 'a1':
                    self.context['whites_chance_for_queenside_castling'] = False
                elif original_cell == 'h1':
                    self.context['whites_chance_for_kingside_castling'] = False
                elif original_cell == 'a8':
                    self.context['blacks_chance_for_queenside_castling'] = False
                elif original_cell == 'h8':
                    self.context['blacks_chance_for_kingside_castling'] = False

            elif move[0] == 'K':
                original_cell = move[1:3]
                if original_cell == 'e1':
                    self.context['whites_chance_for_queenside_castling'] = False
                    self.context['whites_chance_for_kingside_castling'] = False
                elif original_cell == 'e8':
                    self.context['blacks_chance_for_queenside_castling'] = False
                    self.context['blacks_chance_for_kingside_castling'] = False

        self.context[f'en_passant_chance_for_{mover_color}'] = []

        self.change_current_player_color()

        if move[0] == 'P' or 'x' in move:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        self.stats_list.append([self.board_stat, self.context])

    # шах ли
    def is_check(self, to_color: str) -> bool:

        if to_color not in ['white', 'black']:
            raise AttributeError("the parameter 'to_color' must be 'white' or 'black'")

        board_stat_dict = self.get_board_stat_dict()

        # белому
        if to_color == 'white':
            for cell, piece in board_stat_dict.items():
                if piece[0] == 'b':
                    preliminary_moves_list_of_piece = self.get_preliminary_moves_list_of_piece(cell)
                    for move in preliminary_moves_list_of_piece:
                        if self.get_captured_piece(move) == 'wk':
                            return True

        # черному
        elif to_color == 'black':
            for cell, piece in board_stat_dict.items():
                if piece[0] == 'w':
                    preliminary_moves_list_of_piece = self.get_preliminary_moves_list_of_piece(cell)
                    for move in preliminary_moves_list_of_piece:
                        if self.get_captured_piece(move) == 'bk':
                            return True

        return False

        # blacks_preliminary_moves_list = get_preliminary_moves_list_of_piece()

    # Получить список всех разрешенных ходов
    def get_legal_moves_list(self, color: str) -> list:

        if color not in ['white', 'black']:
            raise AttributeError("the parameter 'color' must be 'white' or 'black'")

        moves_list = []

        for letter in 'abcdefgh':

            for num in range(1, 9):

                cell = f'{letter}{num}'
                piece = self.get_piece_in_cell(cell)

                if piece[0][0] == color[0]:


                    preliminary_moves_list_of_piece = self.get_preliminary_moves_list_of_piece(cell)

                    original_board = copy.deepcopy(self.board_stat)
                    original_context = copy.deepcopy(self.context)
                    original_halfmove_clock = copy.deepcopy(self.halfmove_clock)
                    original_statslist = copy.deepcopy(self.stats_list)

                    for move in preliminary_moves_list_of_piece:

                        self.board_stat = copy.deepcopy(original_board)
                        self.context = copy.deepcopy(original_context)
                        self.halfmove_clock = copy.deepcopy(original_halfmove_clock)
                        self.stats_list = copy.deepcopy(original_statslist)

                        # исключаем короткие рокировки, которых нельзя совершать
                        if "<O-O>" in move:

                            if not self.context[f'{color}s_chance_for_kingside_castling']:
                                continue

                            elif self.is_check(color):
                                continue

                            else:
                                num = move[2]

                                self.remove_piece_in_cell(f'e{num}')
                                self.put_piece_in_cell(f'f{num}', f'{color[0]}k')

                                if self.is_check(color):
                                    continue

                                self.remove_piece_in_cell(f'f{num}')
                                self.put_piece_in_cell(f'g{num}', f'{color[0]}k')

                                if self.is_check(color):
                                    continue

                        # исключаем длинные рокировки, которых нельзя совершать
                        elif "<O-O-O>" in move:

                            if not self.context[f'{color}s_chance_for_queenside_castling']:
                                continue

                            elif self.is_check(color):
                                continue

                            else:
                                num = move[2]

                                self.remove_piece_in_cell(f'e{num}')
                                self.put_piece_in_cell(f'c{num}', f'{color[0]}k')

                                if self.is_check(color):
                                    continue

                                self.remove_piece_in_cell(f'c{num}')
                                self.put_piece_in_cell(f'd{num}', f'{color[0]}k')

                                if self.is_check(color):
                                    continue

                        self.board_stat = copy.deepcopy(original_board)
                        self.context = copy.deepcopy(original_context)
                        self.halfmove_clock = copy.deepcopy(original_halfmove_clock)
                        self.stats_list = copy.deepcopy(original_statslist)

                        # рассматриваеый ход
                        self.make_considered_move(move)

                        # исключаем все ходы, после которых самому же игроку (который сделал ход) будет шах (игрок сам себе не должен сделать шах)
                        if self.is_check(color):
                            continue

                        # исключаем взятие на проходе, который не рарешен
                        elif move[-2:] == 'EP' and move not in original_context[f'en_passant_chance_for_{color}']:
                            continue

                        # после всех вышеуказанных фильтров, ход считается разрешенным
                        else:
                            moves_list.append(move)

                    self.board_stat = copy.deepcopy(original_board)
                    self.context = copy.deepcopy(original_context)
                    self.halfmove_clock = copy.deepcopy(original_halfmove_clock)
                    self.stats_list = copy.deepcopy(original_statslist)

        return moves_list

    # мат ли
    def is_mate(self, to_color: str) -> bool:
        legal_moves_list = self.get_legal_moves_list(to_color)
        return len(legal_moves_list) == 0 and self.is_check(to_color)

    # пат ли
    def is_stalemate(self, to_color: str) -> bool:
        legal_moves_list = self.get_legal_moves_list(to_color)
        return len(legal_moves_list) == 0 and not self.is_check(to_color)

    # Сделать ход
    def make_move(self, move):
        original_cell = move[1:3]
        piece = self.get_piece_in_cell(original_cell)

        if piece == '00':
            raise AssertionError(f'{original_cell} is empty')

        else:
            color = 'white' if piece[0] == 'w' else 'black'

            if color != self.context['current_player_color']:
                raise AssertionError(f'error on move \'{move}\': {self.context['current_player_color']} must move now!')

            legal_moves = self.get_legal_moves_list(color)

            if move not in legal_moves:
                raise AssertionError(f'{move} is not valid move')

            else:
                self.make_considered_move(move)



