import math

class Node:
    def __init__(self, label, player, parent, player_pieces, oppo_pieces, parent_move):
        self.label = label
        self.children = []
        self.parent = parent
        self.proof_number = 1
        self.disproof_number = 1
        self.player = player
        self.player_pieces = player_pieces
        self.oppo_pieces = oppo_pieces
        self.parent_move = parent_move

class PNSearch:
    def __init__(self):
        pass

    def look_up(self, node):
        pass

    def update(self, node):
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

    def make_move(self, player, oppo, move):
        #print(f"player: {player}")
        #print(f"oppo: {oppo}")
        #print(f"move: {move}")

        player.remove(move[0])
        player.append(move[1])
        oppo.remove(move[1])
        return player, oppo
    
    def get_minimum_val(self, children, proof_number):
        best = None
        if proof_number == "pn":
            pn = math.inf
            for child in children:
                if child.proof_number <= pn:
                    pn = child.proof_number
                    best = child
        if proof_number == "dpn":
            dpn = math.inf
            for child in children:
                if child.disproof_number <= dpn:
                    dpn = child.disproof_number
                    best = child
        return best
    
    def move_to_coords(self, move):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        piece = alphabet[move[0][0]] + str(move[0][1] + 1)
        destination = alphabet[move[1][0]] + str(move[1][1] + 1)
        return piece + destination
    
    def get_best(self, node):
        if not node.children:
            return node
        best = None
        if node.player == "or":
            # get child node with smallest proof number
            best = self.get_minimum_val(node.children, "pn")
        if node.player == "and":
            # get child node with smallest disproof number
            best = self.get_minimum_val(node.children, "dpn")
        return best

    def select(self, node):
        if not node.children:
            return node
        best = None
        if node.player == "or":
            # get child node with smallest proof number
            best = self.get_minimum_val(node.children, "pn")
        if node.player == "and":
            # get child node with smallest disproof number
            best = self.get_minimum_val(node.children, "dpn")
        result = self.select(best)
        return result

    def expand(self, node):
        moves = []
        types = ["or", "and"]
        node_type = types[0] if node.player == types[1] else types[1]
        moves = self.available_moves(node.player_pieces, node.oppo_pieces)
        #print(moves)
        # if leaf node, do not backpropagate because this was already done?
        if not moves:
            #self.backpropagate(node.parent)
            return
        for move in moves:
            oppo, player = self.make_move(node.player_pieces.copy(), node.oppo_pieces.copy(), move)
            new_node = Node(self.move_to_coords(move), node_type, node, player, oppo, move)
            self.evaluate(new_node)
            node.children.append(new_node)
            #print(new_node.label)
            #print(f"player_pieces: {new_node.player_pieces}")
            #print(f"oppo_pieces: {new_node.oppo_pieces}")
        # backpropagate from this node, updating parent nodes to root
        self.backpropagate(node)

    def evaluate(self, node):
        if not node.children:
            moves = self.available_moves(node.player_pieces, node.oppo_pieces)
            if not moves:
                if node.player == "and":
                    node.proof_number = 0
                    node.disproof_number = math.inf
                if node.player == "or":
                    node.proof_number = math.inf
                    node.disproof_number = 0

    def backpropagate(self, node):
        if node.player == "or":
            min = self.get_minimum_val(node.children, "pn")
            node.proof_number = min.proof_number
            dpn = 0
            for child in node.children:
                dpn += child.disproof_number
            node.disproof_number = dpn
        if node.player == "and":
            min = self.get_minimum_val(node.children, "dpn")
            node.disproof_number = min.disproof_number
            pn = 0
            for child in node.children:
                pn += child.proof_number
            node.proof_number = pn
        if not node.parent:
            return
        else:
            self.backpropagate(node.parent)
