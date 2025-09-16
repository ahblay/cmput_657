import math
import numpy as np
import random
import copy

class Node:
    def __init__(self, value, label, player, parent, player_pieces, oppo_pieces, parent_move, height, width):
        self.label = label
        self.children = []
        # set value according to which player
        self.value = value
        self.parent = parent
        self.player = player
        self.player_pieces = player_pieces
        self.oppo_pieces = oppo_pieces
        self.parent_move = parent_move
        self.height = height
        self.width = width
    
    def position(self, player, opponent):
        result = ["  "]
        alphabet = list("abcdefghijklmnopqrstuvwxyz")
        result.append(" ".join(alphabet[:self.width]))
        result.append('\n')
        for y in range(self.height):
            result.append(f"{y + 1} ")
            for x in range(self.width):
                if (x, y) in self.player_pieces:
                    result.append(player)
                elif (x, y) in self.oppo_pieces:
                    result.append(opponent)
                else:
                    result.append('.')
                result.append(' ')
            result.append('\n')
        return ''.join(result)

class Minimax:
    def __init__(self):
        pass

    def available_moves(self, player, oppo):
        moves = []
        neighbors = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for piece in player:
            for neighbor in neighbors:
                cell = tuple(sum(t) for t in zip(piece, neighbor))
                if cell in oppo:
                    moves.append([piece, cell])
        return moves

    def search(self, node):
        # expand node to get children
        self.expand(node)
        if not node.children:
            if node.player == "max":
                value = -math.inf
            else:
                value = math.inf
            node.value = value
            return value
        if node.player == "max":
            value = -math.inf
            for child in node.children:
                value = max(value, self.search(child))
            node.value = value
            return value
        else:
            value = math.inf
            for child in node.children:
                value = min(value, self.search(child))
            node.value = value
            return value
        
    def get_best(self, node):
        if not node.children:
            return node
        best = None
        if node.player == "max":
            # get child node with largest value
            largest_val = -math.inf
            for child in node.children:
                if child.value >= largest_val:
                    largest_val = child.value
                    best = child
        if node.player == "min":
            # get child node with smallest value
            smallest_val = math.inf
            for child in node.children:
                if child.value >= smallest_val:
                    smallest_val = child.value
                    best = child
        return best
        
    def make_move(self, player, oppo, move):
        player.remove(move[0])
        player.append(move[1])
        oppo.remove(move[1])
        return player, oppo
    
    def move_to_coords(self, move):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        piece = alphabet[move[0][0]] + str(move[0][1] + 1)
        destination = alphabet[move[1][0]] + str(move[1][1] + 1)
        return piece + destination
        
    def expand(self, node):
        moves = []
        types = ["max", "min"]
        node_type = types[0] if node.player == types[1] else types[1]
        value = None
        moves = self.available_moves(node.player_pieces, node.oppo_pieces)
        if not moves:
            return
        for move in moves:
            oppo, player = self.make_move(node.player_pieces.copy(), node.oppo_pieces.copy(), move)
            new_node = Node(value, self.move_to_coords(move), node_type, node, player, oppo, move, node.height, node.width)
            node.children.append(new_node)
        return
    
class ABNode(Node):
    def __init__(self, alpha, beta, value, label, player, parent, player_pieces, oppo_pieces, parent_move, height, width):
        super().__init__(value, label, player, parent, player_pieces, oppo_pieces, parent_move, height, width)
        self.alpha = alpha
        self.beta = beta

class AlphaBeta(Minimax):
    def __init__(self):
        super().__init__()
        self.history = []

    @staticmethod
    def trace(fn):
        def wrapper(self, *args, **kwargs):
            node = args[0]
            depth = args[1]
            alpha = args[2]
            beta = args[3]
            if len(self.history) < 50 and depth >= 0 and node.parent:
                node_copy = copy.deepcopy(node.parent)
                node_copy.alpha = alpha
                node_copy.beta = beta
                self.history.append([node_copy, depth, node])
            try:
                return fn(self, *args, **kwargs)
            finally:
                if len(self.history) < 50 and depth > 0:
                    node_copy = copy.deepcopy(node.parent)
                    node_copy.alpha = alpha
                    node_copy.beta = beta
                    self.history.append([node_copy, depth, node])
        return wrapper

    # alpha is tracking the minimum value that Max can achieve (thus far)
    # beta is tracking maximum value the Min can achieve (thus far)
    @trace
    def search(self, node, depth, alpha, beta, heuristic_fn):
        if depth == 0:
            node.value = heuristic_fn(node)
            return node.value
        # expand node to get children
        self.expand(node)
        if not node.children:
            if node.player == "max":
                value = -math.inf
            else:
                value = math.inf
            node.value = value
            return value
        if node.player == "max":
            value = -math.inf
            for child in node.children:
                value = max(value, self.search(child, depth - 1, alpha, beta, heuristic_fn))
                if value >= beta:
                    break
                alpha = max(alpha, value)
            node.value = value
            return value
        else:
            value = math.inf
            for child in node.children:
                value = min(value, self.search(child, depth - 1, alpha, beta, heuristic_fn))
                if value <= alpha:
                    break
                beta = min(beta, value)
            node.value = value
            return value
        
    def expand(self, node):
        moves = []
        types = ["max", "min"]
        node_type = types[0] if node.player == types[1] else types[1]
        value = None
        moves = self.available_moves(node.player_pieces, node.oppo_pieces)
        if not moves:
            return
        for move in moves:
            oppo, player = self.make_move(node.player_pieces.copy(), node.oppo_pieces.copy(), move)
            new_node = ABNode(node.alpha, 
                              node.beta, 
                              value, 
                              self.move_to_coords(move), 
                              node_type, 
                              node, 
                              player, 
                              oppo, 
                              move, 
                              node.height, 
                              node.width)
            node.children.append(new_node)
        return
    
    def random_heuristic(self, node):
        return round(10 * random.random(), 2)

    # stupid heuristic that just looks at available moves 
    def heuristic(self, node):
        #matrix = self.board_to_matrix(node)
        value = 0
        player_moves = len(self.available_moves(node.player_pieces, node.oppo_pieces))
        oppo_moves = len(self.available_moves(node.oppo_pieces, node.player_pieces))
        if node.player == "max":
            value = player_moves - oppo_moves
        else:
            value = oppo_moves - player_moves
        return value
