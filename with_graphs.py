import random

def random_begin():
	'''Generate a list of 5 random numbers between 20000 and 30000 that are divisible by 12.

	Returns:
		list: A list of 5 random numbers that are divisible by 12.
	'''
	r = []
	count = 0
	while count < 5:
		n = random.randint(20000, 30000)
		if n % 12 == 0:
			r.append(n)
			count += 1
	return r

class State:
	def __init__(self, actual_number, points_player1, points_player2, bank, actual_player):
		self.actual_number = actual_number
		self.points_player1 = points_player1
		self.points_player2 = points_player2
		self.bank = bank
		self.actual_player = actual_player
	
	def __display__(self):
		return f"actual_number: {self.actual_number}\npoints_player1: {self.points_player1}\npoints_player2: {self.points_player2}\nbank: {self.bank}\nactual_player: {self.actual_player}"

class Graph:
	def __init__(self):
		self.nodes = {}  # Dictionary to store the graph nodes

	def add_node(self, state, children=None):
		"""
		Add a node with a state to the graph.

		Args:
			state (State): The state to associate with the node.
			children (list): List of children of the node. Each child is a tuple (state, divisor).
							  By default, the list is empty.
		"""
		if children is None:
			children = []
		self.nodes[state] = children

	def add_edge(self, from_state, to_state, divisor):
		"""
		Add an edge between two nodes.

		Args:
			from_state (State): The starting state of the edge.
			to_state (State): The ending state of the edge.
			divisor (int): The number by which the starting state is divided to reach the ending state.
		"""
		if from_state in self.nodes and to_state in self.nodes:
			self.nodes[from_state].append((to_state, divisor))
		else:
			raise ValueError("Both states must belong to the graph.")

	def get_children(self, state):
		"""
		Returns the children of a given node.

		Args:
			state (State): The state of the node to get the children of.

		Returns:
			list: List of children of the node in the form of tuples (state, edge weight).
		"""
		for node, children in self.nodes.items():
			if node.actual_number == state.actual_number and node.points_player1 == state.points_player1 and node.points_player2 == state.points_player2 and node.bank == state.bank and node.actual_player == state.actual_player:
				return children
		else:
			raise ValueError("The node does not belong to the graph.")
		
	def get_from_divisor(self, state, divisor):
		"""
		Returns the child of a given node that is reached by a specific divisor.

		Args:
			state (State): The state of the node to get the child of.
			divisor (int): The number by which the starting state is divided to reach the child.

		Returns:
			State: The child of the node that is reached by the divisor.
		"""
		for node, children in self.nodes.items():
			if node.actual_number == state.actual_number and node.points_player1 == state.points_player1 and node.points_player2 == state.points_player2 and node.bank == state.bank and node.actual_player == state.actual_player:
				for child, div in children:
					if div == divisor:
						return child
		else:
			raise ValueError("The node does not belong to the graph.")

def display_graph(self):
	"""
	Display the graph in DOT format.
	"""
	dot_code = "digraph G {\n"    
	# Add nodes to the DOT code
	for node, children in self.nodes.items():
		dot_code += f'  {id(node)} [label="actual_number: {node.actual_number}\npoints_player1: {node.points_player1}\npoints_player2: {node.points_player2}\nbank: {node.bank}\nactual_player: {node.actual_player}"];\n'
	# Add edges to the DOT code
	for start, ends in self.nodes.items():
		for end, divisor in ends:
			dot_code += f'  {id(start)} -> {id(end)} [label="{divisor}"];\n'
	dot_code += "}"
	return dot_code

def possible_actions(state):
	'''Generate a list of all possible actions from a given state.

	Args:
		state (state): The state from which to generate the possible actions.

	Returns:
		list: A list of all possible actions from the given state.
	'''
	actions = []
	for divisor in [2, 3, 4]:
		if state.actual_number % divisor == 0:
			actions.append(divisor)
	return actions

def apply_action(state, divisor):
	'''Apply an action to a given state.

	Args:
		state (state): The state to which to apply the action.
		action (int): The action to apply to the state.

	Returns:
		state: The new state after applying the action.
	'''
	new_number = state.actual_number // divisor
	if new_number % 5 == 0:
		new_bank = state.bank + 1
	else:
		new_bank = state.bank
	
	if state.actual_player == 1:
		if new_number % 2 == 0:
			new_points = state.points_player1 - 1
		else:
			new_points = state.points_player1 + 1
		new_state = State(new_number, new_points, state.points_player2, new_bank, 2)
		return new_state
	else:
		if new_number % 2 == 0:
			new_points = state.points_player2 - 1
		else:
			new_points = state.points_player2 + 1
		new_state = State(new_number, state.points_player1, new_points, new_bank, 1)
		return new_state

def already_in_graph(state, graph):
	'''Check if a state is already in the graph.

	Args:
		state (state): The state to check if it is in the graph.
		graph (Graph): The graph to check if the state is in.

	Returns:
		State or None: The existing node if the state is in the graph, None otherwise.
	'''
	for node in graph.nodes:
		if node.actual_number == state.actual_number and node.points_player1 == state.points_player1 and node.points_player2 == state.points_player2 and node.bank == state.bank and node.actual_player == state.actual_player:
			return node
	return None

def generate_graph(state, player, graph):
	'''
	Generate a graph of all possible actions from a given state.
	'''
	graph.add_node(state)
	
	if state.actual_number <= 10:
		return graph

	divisors = possible_actions(state)
	
	for divisor in divisors:
		new_state = apply_action(state, divisor)
		if player == 1:
			new_player = 2
		else:
			new_player = 1
		old_state = already_in_graph(new_state, graph)
		if old_state is None:
			graph.add_node(new_state)
			graph.add_edge(state, new_state, divisor)
			graph = generate_graph(new_state, new_player, graph)
		else:
			graph.add_edge(state, old_state, divisor)
			graph = generate_graph(old_state, new_player, graph)
	
	return graph


def minimax(graph, state, depth, maximizing_player):
	"""
	Apply the minimax algorithm on a graph representing the game tree.

	Args:
		graph (Graph): The graph representing the game tree.
		state (State): The current state of the game.
		depth (int): The depth of the search tree.
		maximizing_player (bool): True if the current player is maximizing, False otherwise.

	Returns:
		State: The best state for the current player.
	"""
	if depth == 0 or graph.get_children(state) == []:
		return state

	if maximizing_player:
		max_score = float('-inf')
		best_state = None
		for child_state, divisor in graph.get_children(state):
			mstate = minimax(graph, child_state, depth - 1, False)
			score = evaluate_state(mstate)
			if score > max_score:
				max_score = score
				best_state = mstate
		return best_state
	else:
		min_score = float('inf')
		best_state = None
		for child_state, divisor in graph.get_children(state):
			mstate = minimax(graph, child_state, depth - 1, True)
			score = evaluate_state(mstate)
			if score < min_score:
				min_score = score
				best_state = mstate
		return best_state

def evaluate_state(state):
	"""
	Evaluate the score of a given state.

	Args:
		state (State): The state to evaluate.

	Returns:
		int: The score of the state.
	"""
	return state.points_player1 - state.points_player2


def alpha_beta(graph, state, depth, alpha, beta, maximizing_player):
	"""
	Apply the alpha-beta pruning algorithm on a graph representing the game tree.

	Args:
		graph (Graph): The graph representing the game tree.
		state (State): The current state of the game.
		depth (int): The depth of the search tree.
		alpha (float): The alpha value for alpha-beta pruning.
		beta (float): The beta value for alpha-beta pruning.
		maximizing_player (bool): True if the current player is maximizing, False otherwise.

	Returns:
		State: The best state for the current player.
	"""
	if depth == 0 or graph.get_children(state) == []:
		return state

	if maximizing_player:
		max_score = float('-inf')
		best_state = None
		for child_state, divisor in graph.get_children(state):
			
			mstate = alpha_beta(graph, child_state, depth - 1, alpha, beta, False)
			score = evaluate_state(mstate)
			if score > max_score:
				max_score = score
				best_state = mstate
			alpha = max(alpha, max_score)
			if beta <= alpha:
				break
		return best_state
	else:
		min_score = float('inf')
		best_state = None
		for child_state, divisor in graph.get_children(state):
			mstate = alpha_beta(graph, child_state, depth - 1, alpha, beta, True)
			score = evaluate_state(mstate)
			if score < min_score:
				min_score = score
				best_state = mstate
			beta = min(beta, min_score)
			if beta <= alpha:
				break
		return best_state

def get_path(graph, origin, goal):
	"""
	Get the path between the origin and goal states in the graph.

	Args:
		graph (Graph): The graph representing the game tree.
		origin (State): The starting state of the path.
		goal (State): The ending state of the path.

	Returns:
		list: A list of states representing the path from origin to goal.
	"""
	path = []
	visited = set()
	stack = [(origin, [])]

	while stack:
		current_state, current_path = stack.pop()
		visited.add(current_state)

		if current_state == goal:
			path = current_path
			break

		for child_state, _ in graph.get_children(current_state):
			if child_state not in visited:
				stack.append((child_state, current_path + [child_state]))

	return path


def get_depth(graph, origin):
	"""
	Get the depth of the graph starting from a given node.
	"""
	depth = 0
	for c in graph.get_children(origin):
		depth = max(depth, get_depth(graph, c[0]))
	return depth + 1
	
