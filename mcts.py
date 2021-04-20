import math
import random

class TreeNode():

  def __init__(self, board, parent):
    self.board = board
    # the depth of the game is 64 moves in total
    self.is_terminal = (self.board.round == 64)
    self.is_fully_expanded = self.is_terminal
    self.parent = parent
    self.visits = 0
    self.score = 0
    self.children = {}

class MCTS():
  
  # search for the best move in the current position
  def search(self, initial_state):
    self.root = TreeNode(initial_state, None)

    for iteration in range(300):
      node = self.select(self.root)     # select a node (selection phase)
      score = self.rollout(node.board)  # score current node (simulation phase)
      self.backpropagate(node, score)
    
    return get_best_move(self.root, 0)


  # select most promising node
  def select(self, node):
    while not node.is_terminal:
      if node.is_fully_expanded:
        node = self.get_best_move(node, 2)
      else:
        node = self.expand(node)
    return node


  # simulate the game via random moves until reaching the end of the game
  def rollout(self, board):
    pass


  # backpropagate the number of visits and score up to the root node
  def backpropagate(self, node, score):
    pass


  # select the best node based on UCB1 formula
  def get_best_move(self, node, exploration_constant):
    # TODO: 可能會有 bug，畢竟有正反方！
    best_score = float('-inf')
    best_moves = []

    for child_node in node.children.values():
      # get move score using UCT (Upper Confidence Bounds to Trees) formula
      current_player = child_node.board.current_player
      # TODO: 可能會有 bug，畢竟有正反方！
      move_score = current_player * child_node.score / child_node.visits + \
        exploration_constant * math.sqrt(math.log(node.visits / child_node.visits))

      # better move has been found
      if move_score > best_score:
        best_score = move_score
        best_moves = [child_node]
      # found as good move as already available
      elif move_score == best_score:
        best_moves.append(child_node)

    # return one of the best moves randomly
    return random.choice(best_moves)