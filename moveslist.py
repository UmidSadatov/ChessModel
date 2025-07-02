import json

moves_list = []

cells_list = []

for letter in 'abcdefgh':
    for num in range(1, 9):
        cells_list.append(f'{letter}{num}')

for original_cell in cells_list:
    for target_cell in cells_list:
        if original_cell != target_cell:
            moves_list.append(f'{original_cell}{target_cell}')

for king_cell in ['e1', 'e8']:
    for castling_type in ['<O-O>', '<O-O-O>']:
        moves_list.append(f'{king_cell}{castling_type}')


letters = 'abcdefgh'
for letter in letters:
    let_indx = letters.index(letter)
    right_letter_indx = let_indx + 1
    left_letter_indx = let_indx - 1

    for prom_piece in ['Q', 'N', 'B', 'R']:
        moves_list.append(f'{letter}7{letter}8{prom_piece}')
        moves_list.append(f'{letter}2{letter}1{prom_piece}')

    if left_letter_indx >= 0:
        left_letter = letters[left_letter_indx]
        for prom_piece in ['Q', 'N', 'B', 'R']:
            moves_list.append(f'{letter}7{left_letter}8{prom_piece}')
            moves_list.append(f'{letter}2{left_letter}1{prom_piece}')

    if right_letter_indx <= 7:
        right_letter = letters[right_letter_indx]
        for prom_piece in ['Q', 'N', 'B', 'R']:
            moves_list.append(f'{letter}7{right_letter}8{prom_piece}')
            moves_list.append(f'{letter}2{right_letter}1{prom_piece}')


with open("moves.json", "w", encoding="utf-8") as file:
    json.dump(moves_list, file, ensure_ascii=False, indent=4)


