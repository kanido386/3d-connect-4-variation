
import STcpClient
import random

from copy import deepcopy
import math
import time



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
    if not board.valid[c]:    # the cell is full
      # FIXME:
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
        # FIXME: wow
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

    # FIXME: may have bug
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



class TreeNode():

  # FIXME: wow
  # def __init__(self, board, parent):
  def __init__(self, board, parent, cell):
    self.board = board
    # the depth of the game is 64 moves in total
    self.is_terminal = (self.board.round > 64)
    self.is_fully_expanded = self.is_terminal
    self.parent = parent
    # FIXME: wow
    self.cell = cell
    self.visits = 0
    self.score = 0
    self.children = {}



class MCTS():
  
  # search for the best move in the current position
  def search(self, initial_state):

    start_time = time.time()
    # print(start_time)

    # if initial_state.round == 1:
    #   the_node = TreeNode(initial_state.move(15), None, 15)
    #   print(15)
    #   return the_node

    # if initial_state.round == 64:
    #   the_node = TreeNode(initial_state.move(11), None, 11)
    #   print(11)
    #   return the_node

    self.root = TreeNode(initial_state, None, None)

    # TODO: modify iteration number (the larger, the better, but slower)
    for iteration in range(500):

      current_time = time.time()
      elapse_time = current_time - start_time
      print(elapse_time)
      if elapse_time > 4.2:
        break

      node = self.select(self.root)     # select a node (selection phase)
      score = self.rollout(node.board)  # score current node (simulation phase)
      self.backpropagate(node, score)

    node, cell = self.get_best_move(self.root, 0)
    print('===========')
    print(cell)
    
    # return node
    return cell


  # select most promising node
  def select(self, node):
    while not node.is_terminal:
      if node.is_fully_expanded:
        node, cell = self.get_best_move(node, 2)
      else:
        node = self.expand(node)
    return node


  def expand(self, node):
    states = node.board.generate_states()
    # FIXME: wow
    # for state in states:
    for cell, state in states:
      # make sure that the current state is not present in child nodes
      if str(state.game_board) not in node.children:
        # FIXME: wow
        # new_node = TreeNode(state, node)
        new_node = TreeNode(state, node, cell)
        node.children[str(state.game_board)] = new_node
        # when node is fully expanded
        if len(states) == len(node.children):
          node.is_fully_expanded = True
        return new_node


  # simulate the game via random moves until reaching the end of the game
  def rollout(self, board):
    line_home_previous = 0
    line_away_previous = 0
    while board.round < 64:
      # board = random.choice(board.generate_states())
      r = random.randint(0, len(board.generate_states())-1)
      # FIXME: wow
      # board = board.generate_states()[r]
      cell, board = board.generate_states()[r]
      # board.print_game_board()
      board.count_point()

      if board.line_home > line_home_previous:
        new_line_number = board.line_home - line_home_previous
        while new_line_number > 0:
          board.line_order.append(1)
          new_line_number -= 1
        line_home_previous = board.line_home
      elif board.line_away > line_away_previous:
        new_line_number = board.line_away - line_away_previous
        while new_line_number > 0:
          board.line_order.append(-1)
          new_line_number -= 1
        line_away_previous = board.line_away

    #   print(board.line_home, board.line_away)
    #   print(board.score_home, board.score_away)
    #   print('==============================')
    # print(board.line_home, board.line_away)
    # print(board.score_home, board.score_away)
    # print(board.line_order)
    # FIXME:
    if board.current_player == 1:
      return board.score_home - board.score_away
    elif board.current_player == -1:
      return board.score_away - board.score_home


  # backpropagate the number of visits and score up to the root node
  def backpropagate(self, node, score):
    # update nodes up to root node
    while node is not None:
      node.visits += 1
      node.score += score
      node = node.parent



  # select the best node based on UCB1 formula
  def get_best_move(self, node, exploration_constant):
    # FIXME: 可能會有 bug，畢竟有正反方！
    best_score = float('-inf')
    best_moves = []

    for child_node in node.children.values():
      # get move score using UCT (Upper Confidence Bounds to Trees) formula
      # FIXME: 暫時先註解掉下面那一行，應該用不到
      # current_player = child_node.board.current_player
      # FIXME: 可能會有 bug，畢竟有正反方！
      # move_score = current_player * child_node.score / child_node.visits + \
      #   exploration_constant * math.sqrt(math.log(node.visits / child_node.visits))
      move_score = child_node.score / child_node.visits + \
        exploration_constant * math.sqrt(math.log(node.visits / child_node.visits))

      # better move has been found
      if move_score > best_score:
        # print(child_node)
        best_score = move_score
        best_moves = [child_node]
      # found as good move as already available
      elif move_score == best_score:
        best_moves.append(child_node)

    # return one of the best moves randomly
    # FIXME: not sure it's really random or not
    # the_node = random.choice(best_moves)
    length = len(best_moves)
    if length > 1:
      r = random.randint(0, length-1)
    else:
      r = 0
    the_node = best_moves[r]
    # print(the_node.cell)
    return the_node, the_node.cell



def to_my_board_format(board):

    which_round = 1

    for l in range(6):
        for i in range(6):
            for j in range(6):
                if board[l][i][j] == 1 or board[l][i][j] == 2:
                    which_round += 1
                if board[l][i][j] == -1:
                    board[l][i][j] = 0
                else:
                    if board[l][i][j] == 1:
                        board[l][i][j] = 1 if is_black else -1
                    elif board[l][i][j] == 2:
                        board[l][i][j] = -1 if is_black else 1
    
    return which_round, board

def map_24_to_36(cell):
    the_map = {
        1:  2,    2:  3,    3:  7,    4:  8,    5:  9,
        6: 10,    7: 12,    8: 13,    9: 14,   10: 15,
        11: 16,   12: 17,   13: 18,   14: 19,   15: 20,
        16: 21,   17: 22,   18: 23,   19: 25,   20: 26,
        21: 27,   22: 28,   23: 32,   24: 33
    }
    return the_map[cell]


'''
    輪到此程式移動棋子
    board : 棋盤狀態(list of list), board[l][i][j] = l layer, i row, j column 棋盤狀態(l, i, j 從 0 開始)
            0 = 空、1 = 黑、2 = 白、-1 = 四個角落
    is_black : True 表示本程式是黑子、False 表示為白子

    return Step
    Step : single touple, Step = (r, c)
            r, c 表示要下棋子的座標位置 (row, column) (zero-base)
'''


def GetStep(board, is_black):
    """
    Example:

    row = random.randint(0, 5)
    col = random.randint(0, 5)
    return (row, col)
    """
    # Modify board to my format
    which_round, game_board = to_my_board_format(board)

    board = Board()
    board.game_board = game_board
    board.round = which_round

    mcts = MCTS()
    best_move = mcts.search(board)      # cell number 1~24

    # Translate to (row, col) according to the spec
    the_position = map_24_to_36(best_move)
    row = the_position / 6
    col = the_position % 6

    return (row, col)


while(True):
    (stop_program, id_package, board, is_black) = STcpClient.GetBoard()
    if(stop_program):
        break

    Step = GetStep(board, is_black)
    STcpClient.SendStep(id_package, Step)
