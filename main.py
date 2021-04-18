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



def do_some_magic(z, y, x, dz, dy, dx):

  global line_home, line_away

  total = 0
  for i in range(4):
    c = 6 * y + x
    if not is_the_actual_cell(c):
      continue
    total += game_board[z][y][x]
    z += dz
    y += dy
    x += dx
  # return total
  if total == 4:
    line_home += 1
  elif total == -4:
    line_away += 1



def is_the_actual_cell(c):
  cell = map_36_to_24[c]
  if cell == 0:   # not the actual cell
    return False
  else:
    return True



def count_point():

  # check the same cell
  for c in range(36):
    if not is_the_actual_cell(c):
      continue
    x = c % 6
    y = c // 6
    for i in range(3):
      do_some_magic(i, y, x, 1, 0, 0)
      # # if game_board[i][y][x] + game_board[i+1][y][x] + game_board[i+2][y][x] + game_board[i+3][y][x] == 4:
      # if do_some_magic(i, y, x, 1, 0, 0) == 4:
      #   line_home += 1
      # # elif game_board[i][y][x] + game_board[i+1][y][x] + game_board[i+2][y][x] + game_board[i+3][y][x] == -4:
      # elif do_some_magic(i, y, x, 1, 0, 0) == -4:
      #   line_away += 1

  # check horizontal
  for c in range(36):
    if not is_the_actual_cell(c):
      continue
    x = c % 6
    y = c // 6
    if x > 2:
      continue
    for i in range(6):
      do_some_magic(i, y, x, 0, 0, 1)

  # check vertical
  for c in range(36):
    if not is_the_actual_cell(c):
      continue
    x = c % 6
    y = c // 6
    if y > 2:
      continue
    for i in range(6):
      do_some_magic(i, y, x, 0, 1, 0)

  # check diagonal (same z)
  for c in range(36):
    if not is_the_actual_cell(c):
      continue
    x = c % 6
    y = c // 6
    if y > 2:
      continue
    for i in range(6):
      if x <= 2:
        do_some_magic(i, y, x, 0, 1, 1)
      else:
        do_some_magic(i, y, x, 0, 1, -1)

  # check diagonal (same y)
  for c in range(36):
    if not is_the_actual_cell(c):
      continue
    x = c % 6
    y = c // 6
    for i in range(3, 6):   # 3, 4, 5
      if x <= 2:
        do_some_magic(i, y, x, -1, 0, 1)
      else:
        do_some_magic(i, y, x, -1, 0, -1)

  # check diagonal (same x)
  for c in range(36):
    if not is_the_actual_cell(c):
      continue
    x = c % 6
    y = c // 6
    for i in range(3, 6):   # 3, 4, 5
      if y <= 2:
        do_some_magic(i, y, x, -1, 1, 0)
      else:
        do_some_magic(i, y, x, -1, -1, 0)

  # check diagonal (all different)
  for c in range(36):
    if not is_the_actual_cell(c):
      continue
    x = c % 6
    y = c // 6
    if y > 2:
      continue
    for i in range(3):
      if x <= 2:
        do_some_magic(i, y, x, 1, 1, 1)
      else:
        do_some_magic(i, y, x, 1, 1, -1)
    for i in range(3, 6):
      if x <= 2:
        do_some_magic(i, y, x, -1, 1, 1)
      else:
        do_some_magic(i, y, x, -1, 1, -1)


# test the same cell: (2, 0)
# move(-1, 5), move(1, 5), move(1, 5), move(1, 5), move(1, 5), move(1, 5)

# test horizontal: (1, 1)
# move(-1, 15), move(-1, 16), move(-1, 17), move(-1, 18)
# move(1, 15), move(1, 16), move(1, 17), move(1, 18)

# test vertical: (1, 1)
# move(-1, 9), move(-1, 15), move(-1, 20), move(-1, 23)
# move(1, 9), move(1, 15), move(1, 20), move(1, 23)

# test diagonal (same z): (1, 1)
# move(-1, 3), move(-1, 9), move(-1, 16), move(-1, 22)
# move(1, 6), move(1, 10), move(1, 15), move(1, 19)

# test diagonal (same y): (1, 0)
# move(1, 8), move(-1, 9), move(1, 9), move(1, 10), move(-1, 10)
# move(1, 10), move(-1, 11), move(-1, 11), move(-1, 11), move(1, 11)

# test diagonal (same x): (1, 0)
# move(1, 6), move(-1, 11), move(1, 11), move(1, 17), move(-1, 17)
# move(1, 17), move(-1, 22), move(-1, 22), move(-1, 22), move(1, 22)

# test diagonal (all different): (1, 0)
# move(1, 6), move(-1, 10), move(1, 10), move(1, 15), move(-1, 15)
# move(1, 15), move(-1, 19), move(-1, 19), move(-1, 19), move(1, 19)


# print_game_board()

count_point()
print(line_home, line_away)