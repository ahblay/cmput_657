import math
from minimax import Node, ABNode
from PrettyPrint import PrettyPrintTree
import copy

class Handler:
    def __init__(self, player, board, time, print=False):
        self.player = player
        self.opponent = "x" if player == "o" else "o"
        self.board = board
        self.print = print
        self.time = time
        self.player_pieces = self.init_pieces(player)
        self.oppo_pieces = self.init_pieces(self.opponent)

    def init_pieces(self, player):
        if player == "o":
            pieces = self.board.player_1.pieces
        else:
            pieces = self.board.player_2.pieces
        return pieces

    def run(self):
        pass

    def get_result(self, piece, destination):
        success, result = self.board.move(self.player, piece, destination)
        return success, self.board.__str__()


class MinimaxHandler(Handler):
    def __init__(self, minimax, player, board, time, print=False):
        if print:
            super().__init__(player, board, time, print)
        else:
            super().__init__(player, board, time)
        self.minimax = minimax
        self.history = []
    
    def run(self):
        root = Node(-math.inf, "root", "max", None, self.player_pieces, self.oppo_pieces, [], self.board.height, self.board.width)
        self.minimax.search(root)
        best_node = self.minimax.get_best(root)
        piece, destination = best_node.parent_move
        return self.get_result(piece, destination)  
    
class AlphaBetaHandler(Handler):
    def __init__(self, ab, depth, player, board, time, explain=False, print=False):
        if print:
            super().__init__(player, board, time, print)
        else:
            super().__init__(player, board, time)
        self.ab = ab
        self.depth = depth
        self.dummy_node = ABNode("N/A", "N/A", "N/A", "...", "N/A", None, None, None, [], 0, 0)
        self.explain = explain
    
    def run(self):
        root = ABNode(-math.inf, 
                      math.inf, 
                      -math.inf, 
                      "root", 
                      "max", 
                      None, 
                      self.player_pieces, 
                      self.oppo_pieces, 
                      [], 
                      self.board.height, 
                      self.board.width)
        if self.explain:
            heuristic_fn = self.ab.random_heuristic
        else:
            heuristic_fn = self.ab.heuristic
        self.ab.search(root, self.depth, -math.inf, math.inf, heuristic_fn)
        best_node = self.ab.get_best(root)
        piece, destination = best_node.parent_move
        if self.explain:
            self.show_steps()
        return self.get_result(piece, destination)
        
    def show_steps(self):
        history = self.ab.history
        index = 0
        command = input("press + to go forward, - to go back, and q to exit\n")
        while True:
            # replace this with function for handling pretty print
            self.print_tree(history[index])
            command = input()
            if command == "+":
                index = (index + 1) % len(history)
            elif command == "-":
                index = (index - 1) % len(history)
            elif command == "q":
                break
        return
    
    def print_tree(self, data):
        node = data[0]
        depth = data[1]
        current_node_label = data[2].label
        # which player are we?
        opponent = 'x' if self.player == 'o' else 'o'
        if (self.depth - depth) % 2 == 0:
            print(node.position(self.player, opponent))
        else:
            print(node.position(opponent, self.player))

        node_label = lambda x: f"player: {x.player}\nvalue: {x.value}\nalpha {x.alpha}\nbeta: {x.beta}"
        print_tree = PrettyPrintTree(lambda x: x.children[:4], 
                                     node_label, 
                                     lambda x: x.label, 
                                     max_depth=2, 
                                     start_message=lambda x: f'subtree root at depth: {self.depth - depth}')
        #print_tree(node)
        print_tree(self.update_rooted_node_children(node, current_node_label))
        return
    
    def update_rooted_node_children(self, root, child_label):
        num_children = len(root.children)
        child_index = 0
        for node in root.children:
            if node.label == child_label:
                child_index = root.children.index(node)
        root.children = root.children[max(0, child_index - 1):child_index + 1]
        if child_index > 1:
            root.children.insert(0, self.dummy_node)
        if num_children > child_index:
            root.children.append(self.dummy_node)
        return root