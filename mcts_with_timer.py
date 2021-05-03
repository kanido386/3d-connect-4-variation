import math
import random
import time

class TreeNode():

  # TODO: wow
  # def __init__(self, board, parent):
  def __init__(self, board, parent, cell):
    self.board = board
    # the depth of the game is 64 moves in total
    self.is_terminal = (self.board.round > 64)
    self.is_fully_expanded = self.is_terminal
    self.parent = parent
    # TODO: wow
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
    
    return node


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
    # TODO: wow
    # for state in states:
    for cell, state in states:
      # make sure that the current state is not present in child nodes
      if str(state.game_board) not in node.children:
        # TODO: wow
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
      # TODO: wow
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
    # TODO:
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
    # TODO: 可能會有 bug，畢竟有正反方！
    best_score = float('-inf')
    best_moves = []

    for child_node in node.children.values():
      # get move score using UCT (Upper Confidence Bounds to Trees) formula
      # TODO: 暫時先註解掉下面那一行，應該用不到
      # current_player = child_node.board.current_player
      # TODO: 可能會有 bug，畢竟有正反方！
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
    # TODO: not sure it's really random or not
    # the_node = random.choice(best_moves)
    length = len(best_moves)
    if length > 1:
      r = random.randint(0, length-1)
    else:
      r = 0
    the_node = best_moves[r]
    # print(the_node.cell)
    return the_node, the_node.cell