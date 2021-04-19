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