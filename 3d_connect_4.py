from copy import deepcopy
import random
from mcts import *

class Board():

  def __init__(self, board=None):

    # the order of players connect a line
    self.line_order = []

    # define players
    self.current_player = 1
    self.round = 1
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

    # put here to prevent count_point() bug
    self.line_home = 0
    self.line_away = 0
    self.score_home = 0
    self.score_away = 0


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
    board.round += 1
    
    return board


  def generate_states(self):
    # list of available actions to consider
    actions = []
    for cell in range(1, 25):   # cell 1~24
      c = self.map_24_to_36[cell]
      if self.valid[c] != 0:    # not full
        # TODO: wow
        # actions.append(self.move(cell))
        actions.append((cell, self.move(cell)))
    return actions


  def game_loop(self):
    while True:
      print(f'round {self.round}')
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

    # print(self.current_player)

    first_flag = True
    first_position = 0

    total = 0
    for i in range(4):
      c = 6 * y + x

      # never happen
      if not self.is_the_actual_cell(c):
        return
      # record the first one
      if first_flag:
        first_position = self.game_board[z][y][x]
        if first_position != 0:
          first_flag = False
      # means never forms a line
      if not first_flag and self.game_board[z][y][x] == -first_position:
        return
        
      total += self.game_board[z][y][x]
      # print('here')
      z += dz
      y += dy
      x += dx
    # return total

    # print(total)

    if first_position == 1:
      self.score_home += total
    elif first_position == -1:
      self.score_away += (-total)

    # print(total)

    # TODO: may have bug
    # print(total)
    # if self.current_player == 1:
    #   self.score_home += total
    # elif self.current_player == -1:
    #   self.score_away += (-total)

    # form a line!
    if total == 4:
      self.line_home += 1
      # TODO: 更改參數
      self.score_home += 30
    elif total == -4:
      self.line_away += 1
      # TODO: 更改參數
      self.score_away += 30


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


  # TODO:
  def naive_approach(self):
    maximum = float('-inf')
    the_cell = 0
    the_board = None
    for i in range(1, 25):  # cell 1~24

      c = self.map_24_to_36[i]
      if self.valid[c] == 0:    # full
        continue

      board = self.move(i)
      board.count_point()
      # board.print_game_board()
      temp = abs(board.score_home - board.score_away)
      if temp > maximum:
        maximum = temp
        the_cell = i
        the_board = board
    #   print(i, board.score_home, board.score_away)
    # print('==============================')
    # print(the_cell, maximum, the_board)

    print(the_cell)

    return the_board



if __name__ == '__main__':

  # total_home = 0
  # total_away = 0
  
  # for i in range(1):
  #   board = Board()
  #   # print(board.__dict__)

  #   for i in range(64):
  #     # cell = random.randint(1, 24)
  #     # board = board.move(cell)
  #     board = random.choice(board.generate_states())
    
  #   board.print_game_board()
  #   board.count_point()
  #   # print(board.line_home, board.line_away)
  #   total_home += board.line_home
  #   total_away += board.line_away

  # print(total_home, total_away)

  # ==============================

  # # test generate_states()
  # board = Board()
  # actions = board.generate_states()
  # for action in actions:
  #   action.print_game_board()
  #   print('**************************************************')

  # ==============================

  board = Board()
  # board.game_loop()
  # root = TreeNode(board, None)
  # root.children['test'] = TreeNode(board.move(11), root)
  # print(root.__dict__)
  # print(root.children['test'].__dict__)

  mcts = MCTS()

  # i = 1

  # # loop to play AI vs AI
  # while i <= 64:
  #   board = board.naive_approach()
  #   # board.print_game_board()
  #   print(board.score_home, board.score_away)
  #   print(board.line_home, board.line_away)
  #   print(f'**************** {i} **************')
    
  #   i += 1

  i = 1

  # loop to play AI vs AI
  while board.round <= 64:
    best_move = mcts.search(board)
    board = best_move.board
    board.count_point()
    # board.print_game_board()
    print(board.score_home, board.score_away)
    print(board.line_home, board.line_away)
    print(f'**************** {i} **************')
    
    i += 1