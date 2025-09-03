from game_logic import TricTacToe

class TricTacToeAI:
    def __init__(self, depth = 9):
        self.depth = depth

    def get_move(self, game: TricTacToe):
        player = 1 if game.current_player == 1 else -1
        _, move = self.negmax(game, self.depth, float('-inf'), float('inf'), player)
        return move

    def negmax(self, game: TricTacToe, depth: int, alpha: float, beta: float, player: int):
        if (depth == 0):
            return self.evaluate(game, player), None

        max_eval = float('-inf')
        best_move = None

        moves = self.order_moves(game.valid_moves())

        for move in moves:
            game_copy = game.copy()
            game_copy.make_move(move)
            score, _ = self.negmax(game_copy, depth - 1, -beta, -alpha, -player)
            score = -score
            max_eval = max(max_eval, score)
            if max_eval == score:
                best_move = move

            alpha = max(alpha, score)
            if beta <= alpha:
                break

        return max_eval, best_move
    
    def evaluate(self, game: TricTacToe, player: int):
        if game.check_winner(player, game.get_last_move()[1]):
            return 1000
        elif game.check_winner(-player, game.get_last_move()[1]):
            return -1000

        return self.heuristic_score(game, player)

    def heuristic_score(self, game: TricTacToe, color: int):
        player = 1 if color == 1 else -1
        opponent = -player
        
        score = 0
        
        patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
        board = game.get_board()
        
        for pattern in patterns:
            line = [board[i] for i in pattern]
            
            player_count = line.count(player)
            opponent_count = line.count(opponent)
            
            # Heavily penalize opponent threats
            if opponent_count == 2 and player_count == 0:
                score -= 1000000
            elif opponent_count == 1 and player_count == 0:
                score -= 20    
            
            if player_count == 2 and opponent_count == 0:
                score += 500
            elif player_count == 1 and opponent_count == 0:
                score += 5    
        
        if board[4] == player:
            score += 15
        
        return score


    def order_moves(self, moves):

        center = [4]
        corners = [0, 2, 6, 8]
        edges = [1, 3, 5, 7]

        ordered_moves = []
        for move in center + edges + corners:
            if move in moves:
                ordered_moves.append(move)
        return ordered_moves
