import math
import random

class TreeNode():

  def __init__(self, board, parent):
    self.board = board
    # the depth of the game is 64 moves in total
    self.is_terminal = (self.board.round == 64)
    self.is_fully_expanded = self.is_terminal
    self.parent = parent
    self.visit = 0
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
    pass


  # simulate the game via random moves until reaching the end of the game
  def rollout(self, board):
    pass


  # backpropagate the number of visits and score up to the root node
  def backpropagate(self, node, score):
    pass


  # select the best node based on UCB1 formula
  def get_best_move(self, node, exploration_constant):
    pass