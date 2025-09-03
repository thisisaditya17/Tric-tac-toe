from collections import deque

class TricTacToe:
    def __init__(self):
        self.board = [0] * 9               
        self.move_history = deque()         
        self.current_player = 1          
        self.moves_played = 0             
        self.game_over = False
        self.winner = None

    def valid_moves(self):
        return [i for i in range(9) if self.board[i] == 0]  

    def make_move(self, position):
        if self.game_over or position not in self.valid_moves():
            return False  

        if len(self.move_history) >= 6:
            old_player, old_pos, _ = self.move_history.popleft()
            self.board[old_pos] = 0  


        self.board[position] = self.current_player
        self.moves_played += 1
        self.move_history.append((self.current_player, position, self.moves_played))

        if self.check_winner(self.current_player, position):
            self.game_over = True
            self.winner = self.current_player
            return True 

        self.current_player *= -1
        return True

    def check_winner(self, player, last_pos):
        r = last_pos // 3
        c = last_pos % 3

        # Row
        if self.board[3*r] == player and self.board[3*r+1] == player and self.board[3*r+2] == player:
            return True   

        # Column
        if self.board[c] == player and self.board[c+3] == player and self.board[c+6] == player:
            return True   

        # Main diagonal
        if last_pos in (0, 4, 8):
            if self.board[0] == player and self.board[4] == player and self.board[8] == player:
                return True   

        # Anti-diagonal
        if last_pos in (2, 4, 6):
            if self.board[2] == player and self.board[4] == player and self.board[6] == player:
                return True   

        return False

    def get_board_state(self):
        return self.board.copy()  

    def reset(self):
        self.__init__()  

    def get_game_history(self):
        game_history = [9] * 6
        recent = list(self.move_history)[-6:]
        for i, (_, pos, _) in enumerate(recent):
            game_history[i] = pos
        return game_history 
    
    def get_last_move(self):
        return self.move_history[-1] if self.move_history else None

    def moves_until_removal(self):
        return max(0, 6 - len(self.move_history))
    
    def copy(self):
        new_game = TricTacToe()
        new_game.board = self.board.copy()
        new_game.move_history = self.move_history.copy()
        new_game.current_player = self.current_player
        new_game.moves_played = self.moves_played
        new_game.game_over = self.game_over
        new_game.winner = self.winner
        return new_game

    def get_board(self):
        return self.board.copy()
