map_24_to_36 = {
   1:  2,    2:  3,    3:  7,    4:  8,    5:  9,
   6: 10,    7: 12,    8: 13,    9: 14,   10: 15,
  11: 16,   12: 17,   13: 18,   14: 19,   15: 20,
  16: 21,   17: 22,   18: 23,   19: 25,   20: 26,
  21: 27,   22: 28,   23: 32,   24: 33
}

map_36_to_24 = {
   0:  0,
   1:  0,    2:  1,    3:  2,    4:  0,    5:  0,
   6:  0,    7:  3,    8:  4,    9:  5,   10:  6,
  11:  0,   12:  7,   13:  8,   14:  9,   15: 10,
  16: 11,   17: 12,   18: 13,   19: 14,   20: 15,
  21: 16,   22: 17,   23: 18,   24:  0,   25: 19,
  26: 20,   27: 21,   28: 22,   29:  0,   30:  0,
  31:  0,   32: 23,   33: 24,   34:  0,   35:  0,
}

# print(map_24_to_36[1])
# print(map_36_to_24[1])



# game_board[z][y][x]
game_board = [[[0 for x in range(6)] for y in range(6)] for z in range(6)]



# whether can drop a game piece in or not
valid = [0 for c in range(36)]
for c in map_36_to_24:
  cell = map_36_to_24[c]  # the actual cell
  if cell != 0:
    valid[c] = 1
# print(valid)



line_home = 0
line_away = 0



def move(who, cell):
  c = map_24_to_36[cell]
  if not valid[c]:    # test whether the cell is full or not
    print('FULL!')
    return
  x = c % 6
  y = c // 6
  for i in range(6):
    if game_board[i][y][x] == 0:
      game_board[i][y][x] = who
      if i == 5:
        valid[c] = 0  # full
      break



def print_game_board():
  for xy in game_board:
    for y in xy:
      print(y)
    print('==============================')



def count_point():

  # TODO: rewrite this file to a class
  global line_home, line_away

  # check the same cell
  for c in range(36):
    cell = map_36_to_24[c]
    if cell == 0:   # not the actual cell
      continue
    x = c % 6
    y = c // 6
    for i in range(3):
      if game_board[i][y][x] + game_board[i+1][y][x] + game_board[i+2][y][x] + game_board[i+3][y][x] == 4:
        line_home += 1
      elif game_board[i][y][x] + game_board[i+1][y][x] + game_board[i+2][y][x] + game_board[i+3][y][x] == -4:
        line_away += 1

  # TODO: add other direction



move(-1, 5)
move(1, 5)
move(1, 5)
move(1, 5)
move(1, 5)
move(1, 5)

# print_game_board()

count_point()
print(line_home, line_away)