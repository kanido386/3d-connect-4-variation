from copy import deepcopy
import random

class Board():

  def __init__(self, board=None):

    self.line_home = 0
    self.line_away = 0

    # define players
    self.current_player = 1
    # self.player_home = 1
    # self.player_away = -1

    self.map_24_to_36 = {
      1:  2,    2:  3,    3:  7,    4:  8,    5:  9,
      6: 10,    7: 12,    8: 13,    9: 14,   10: 15,
      11: 16,   12: 17,   13: 18,   14: 19,   15: 20,
      16: 21,   17: 22,   18: 23,   19: 25,   20: 26,
      21: 27,   22: 28,   23: 32,   24: 33
    }
    self.map_36_to_24 = {
      0:  0,
      1:  0,    2:  1,    3:  2,    4:  0,    5:  0,
      6:  0,    7:  3,    8:  4,    9:  5,   10:  6,
      11:  0,   12:  7,   13:  8,   14:  9,   15: 10,
      16: 11,   17: 12,   18: 13,   19: 14,   20: 15,
      21: 16,   22: 17,   23: 18,   24:  0,   25: 19,
      26: 20,   27: 21,   28: 22,   29:  0,   30:  0,
      31:  0,   32: 23,   33: 24,   34:  0,   35:  0,
    }

    # whether can drop a game piece in or not
    self.valid = [0 for c in range(36)]
    self.init_valid()

    # game_board[z][y][x]
    self.game_board = [[[0 for x in range(6)] for y in range(6)] for z in range(6)]

    # create a copy of previous board state if available
    if board is not None:
      self.__dict__ = deepcopy(board.__dict__)


  def move(self, cell):
    # create new board instance that inherits from the current state
    board = Board(self)

    c = self.map_24_to_36[cell]
    if not board.valid[c]:    # test whether the cell is full or not
      # TODO:
      # print('FULL!')
      return self
    x = c % 6
    y = c // 6
    for i in range(6):
      if board.game_board[i][y][x] == 0:
        board.game_board[i][y][x] = self.current_player
        if i == 5:
          board.valid[c] = 0  # full
        break

    # change player
    board.current_player *= -1
    
    return board


  def generate_states(self):
    # list of available actions to consider
    actions = []
    for cell in range(1, 25):   # cell 1~24
      c = self.map_24_to_36[cell]
      if self.valid[c] != 0:    # not full
        actions.append(self.move(cell))
    return actions


  def game_loop(self):
    while True:
      input_cell = int(input(f'player {self.current_player}: '))
      self = self.move(input_cell)
      self.print_game_board()


  def is_the_actual_cell(self, c):
    cell = self.map_36_to_24[c]
    if cell == 0:   # not the actual cell
      return False
    else:
      return True


  def do_some_magic(self, z, y, x, dz, dy, dx):

    total = 0
    for i in range(4):
      c = 6 * y + x
      if not self.is_the_actual_cell(c):
        continue
      total += self.game_board[z][y][x]
      z += dz
      y += dy
      x += dx
    # return total
    if total == 4:
      self.line_home += 1
    elif total == -4:
      self.line_away += 1


  def count_point(self):

    # check the same cell
    for c in range(36):
      if not self.is_the_actual_cell(c):
        continue
      x = c % 6
      y = c // 6
      for i in range(3):
        self.do_some_magic(i, y, x, 1, 0, 0)

    # check horizontal
    for c in range(36):
      if not self.is_the_actual_cell(c):
        continue
      x = c % 6
      y = c // 6
      if x > 2:
        continue
      for i in range(6):
        self.do_some_magic(i, y, x, 0, 0, 1)

    # check vertical
    for c in range(36):
      if not self.is_the_actual_cell(c):
        continue
      x = c % 6
      y = c // 6
      if y > 2:
        continue
      for i in range(6):
        self.do_some_magic(i, y, x, 0, 1, 0)

    # check diagonal (same z)
    for c in range(36):
      if not self.is_the_actual_cell(c):
        continue
      x = c % 6
      y = c // 6
      if y > 2:
        continue
      for i in range(6):
        if x <= 2:
          self.do_some_magic(i, y, x, 0, 1, 1)
        else:
          self.do_some_magic(i, y, x, 0, 1, -1)

    # check diagonal (same y)
    for c in range(36):
      if not self.is_the_actual_cell(c):
        continue
      x = c % 6
      y = c // 6
      for i in range(3, 6):   # 3, 4, 5
        if x <= 2:
          self.do_some_magic(i, y, x, -1, 0, 1)
        else:
          self.do_some_magic(i, y, x, -1, 0, -1)

    # check diagonal (same x)
    for c in range(36):
      if not self.is_the_actual_cell(c):
        continue
      x = c % 6
      y = c // 6
      for i in range(3, 6):   # 3, 4, 5
        if y <= 2:
          self.do_some_magic(i, y, x, -1, 1, 0)
        else:
          self.do_some_magic(i, y, x, -1, -1, 0)

    # check diagonal (all different)
    for c in range(36):
      if not self.is_the_actual_cell(c):
        continue
      x = c % 6
      y = c // 6
      if y > 2:
        continue
      for i in range(3):
        if x <= 2:
          self.do_some_magic(i, y, x, 1, 1, 1)
        else:
          self.do_some_magic(i, y, x, 1, 1, -1)
      for i in range(3, 6):
        if x <= 2:
          self.do_some_magic(i, y, x, -1, 1, 1)
        else:
          self.do_some_magic(i, y, x, -1, 1, -1)


  def print_game_board(self):
    for xy in self.game_board:
      for y in xy:
        print(y)
      print('==============================')

  
  def init_valid(self):
    for c in self.map_36_to_24:
      cell = self.map_36_to_24[c]  # the actual cell
      if cell != 0:
        self.valid[c] = 1



if __name__ == '__main__':

  total_home = 0
  total_away = 0
  
  for i in range(30):
    board = Board()
    # print(board.__dict__)

    for i in range(64):
      cell = random.randint(1, 24)
      board = board.move(cell)
    # board.print_game_board()
    board.count_point()
    # print(board.line_home, board.line_away)
    total_home += board.line_home
    total_away += board.line_away

  print(total_home, total_away)

  # ==============================

  board = Board()
  actions = board.generate_states()
  for action in actions:
    action.print_game_board()
    print('**************************************************')

  # ==============================

  board = Board()
  board.game_loop()