import argparse

#Player/Mark ID Enum
PM_ = 0
PMX = 1
PMO = 2

#Player/Mark Str Enum
PM___STR = '_'
PM_X_STR = 'X'
PM_O_STR = 'O'

#Player/Mark ID to Str Array
PM_ID_TO_STR = [PM___STR, PM_X_STR, PM_O_STR]

def ParseCommandLineArgs():
	prog_desc = ('It\'s Tic-tac-toe... yup.')
	mnk_help = ('Enter 3 numbers separted by spaces, which represent: '
		'Width of the board, '
		'Height of the board, '
		'Number of sequential marks needed to win. '
		'Default values are: 3 3 3')
	
	parser = argparse.ArgumentParser(description = prog_desc)
	parser.add_argument('--mnk', '-n', nargs = 3, type = int, help = mnk_help)
	parser.set_defaults(mnk = [3, 3, 3])
	
	args = parser.parse_args()
	(width, height, n) = (args.mnk[0], args.mnk[1], args.mnk[2])
	
	if width <= 0 or height <= 0 or n <= 0:
		print('Width, height, and num arguments must be at least 1.')
		return None
	
	return (width, height, n)

def BoardHasEmptySpaces(board):
	for row in board:
		for space in row:
			if space == PM_:
				return True
	return False

def GetNumDigits(x):
	return len(str(x))

def PrintBoard(board):
	#print the board, and the coordinates of each space
	num_digits_in_height = GetNumDigits(len(board) - 1)
	top_str = ' '*(num_digits_in_height + 1) + ' '.join(map(str, list(range(len(board[0])))))
	print(top_str)
	
	for i, row in enumerate(board):
		num_digits_in_i = GetNumDigits(i)
		line_str = str(i) + ' '*(num_digits_in_height + 1 - num_digits_in_i)
		for j, mark in enumerate(row):
			num_digits_in_j = GetNumDigits(j)
			line_str += ' '*(num_digits_in_j - 1) + PM_ID_TO_STR[mark] + ' '
		
		print(line_str)

def CoordIsOutOfBounds(board, row_idx, col_idx):
	return row_idx < 0 or row_idx >= len(board) or col_idx < 0 or col_idx >= len(board[0])

def RetrieveCoords(board):
	player_input = None
	input_is_valid = False
	syntax_help_str = 'Please enter input in the form of "x,y", where x and y are integers representing the row and column coordinates, respectively.'
	placement_help_str = 'Coordinates are either out of range or the spot has already been marked. Please choose a different coordinate.'
	
	while not input_is_valid:
		player_input = input('Enter Coordinates: ').strip().split(',')
		
		if len(player_input) != 2:
			print(syntax_help_str)
			continue
		
		try:
			player_input = (int(player_input[0]), int(player_input[1]))
		except ValueError:
			print(syntax_help_str)
			continue
		
		if CoordIsOutOfBounds(board, player_input[1], player_input[0]) or board[player_input[1]][player_input[0]] != PM_:
			print(placement_help_str)
			continue
		
		input_is_valid = True
	
	return player_input

def PlayerHasMatchedThisPattern(board, n, row_inc, col_inc):
	for row_idx in range(len(board)):
		for col_idx in range(len(board[0])):
			pattern_matched = True
			if board[row_idx][col_idx] == PM_ or CoordIsOutOfBounds(board, row_idx + (n-1)*row_inc, col_idx + (n-1)*col_inc):
				continue
			
			for i in range(1, n):
				if board[row_idx + i*row_inc][col_idx + i*col_inc] != board[row_idx + (i-1)*row_inc][col_idx + (i-1)*col_inc]:
					pattern_matched = False
					break
			
			if pattern_matched:
				return board[row_idx][col_idx]
	
	return PM_

def GetWinner(board, n):
	#horizontal check
	player = PlayerHasMatchedThisPattern(board, n, 0, 1)
	if player != PM_:
		return player
	
	#vertical check
	player = PlayerHasMatchedThisPattern(board, n, 1, 0)
	if player != PM_:
		return player
	
	#diagonal up-left to bot-right check
	player = PlayerHasMatchedThisPattern(board, n, 1, 1)
	if player != PM_:
		return player
	
	#diagonal up-right to bot-left check
	player = PlayerHasMatchedThisPattern(board, n, 1, -1)
	if player != PM_:
		return player
	
	return PM_

def GameLoop(board, n):
	winner = PM_
	current_player = PMX
	
	while winner == PM_ and BoardHasEmptySpaces(board):
		print('\n' + PM_ID_TO_STR[current_player] + '\'s turn!\n')
		PrintBoard(board)
		coords = RetrieveCoords(board)
		board[coords[1]][coords[0]] = current_player
		
		winner = GetWinner(board, n)
		
		if current_player == PMX:
			current_player = PMO
		else:
			current_player = PMX
	
	if winner == PMX or winner == PMO:
		print('\n' + PM_ID_TO_STR[winner] + ' wins!')
	else:
		print('\nDraw!')

	PrintBoard(board)

def Main():
	args = ParseCommandLineArgs()
	if args == None:
		return
	(width, height, n) = args
	
	board = [[]] * width
	for i in range(height):
		board[i] = [PM_]*width
	
	print('Welcome to TicTacToe.py! Take turns filling the grid by specifying the coordinates of the space as "x,y". X moves first')
	
	GameLoop(board, n)

if __name__ == '__main__':
	Main()