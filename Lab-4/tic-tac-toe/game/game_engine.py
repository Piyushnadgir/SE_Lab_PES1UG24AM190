"""
GameEngine: owns the board, turn state, and round-end logic.

You (the player) always play X and click to move.
The computer always plays O and moves automatically right after you,
using a simple random-move AI.
"""

from game.rules import check_winner, is_board_full
from game.renderer import board_pos_to_cell
from game.ai import choose_move


HUMAN_SYMBOL = 'X'
COMPUTER_SYMBOL = 'O'


class GameEngine:
    def __init__(self):
        self.board = [[None] * 3 for _ in range(3)]
        self.current_player = HUMAN_SYMBOL
        self.round_over = False
        self.winner = None   # 'X', 'O', or None for a draw

    def handle_click(self, pos):
        # Do not allow any moves after the round has ended
        if self.round_over:
            return

        # Only allow the human to move when it is X's turn
        if self.current_player != HUMAN_SYMBOL:
            return

        cell = board_pos_to_cell(pos)

        if cell is None:
            return

        row, col = cell

        # Do not allow a move on an occupied cell
        if self.board[row][col] is not None:
            return

        # Place X
        self.board[row][col] = self.current_player

        # Check whether the human's move ended the round
        self.check_round_end()

        # If the round ended, stop here.
        # Do not switch turns or let the computer move.
        if self.round_over:
            return

        # Switch to computer
        self.current_player = COMPUTER_SYMBOL

        self._maybe_take_computer_turn()

    def _maybe_take_computer_turn(self):
        # Computer should not move if the round has already ended
        if self.round_over or self.current_player != COMPUTER_SYMBOL:
            return

        move = choose_move(self.board)

        if move is None:
            return

        row, col = move

        # Place O
        self.board[row][col] = self.current_player

        # Check whether the computer's move ended the round
        self.check_round_end()

        # If the round ended, don't switch turns
        if self.round_over:
            return

        # Switch back to human
        self.current_player = HUMAN_SYMBOL

    def handle_keydown(self, key):
        import pygame

        if key == pygame.K_r:
            self.__init__()

    def check_round_end(self):
        # IMPORTANT:
        # Check for a winner FIRST.
        # A winning move can also fill the final empty cell.
        winner = check_winner(self.board)

        if winner:
            self.round_over = True
            self.winner = winner
            return

        # Only check for a draw if there is no winner
        if is_board_full(self.board):
            self.round_over = True
            self.winner = None

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_board(surface, self.board)

        turn_label = (
            "Your turn (X)"
            if self.current_player == HUMAN_SYMBOL
            else "Computer's turn (O)"
        )

        renderer.draw_text(surface, font, turn_label, (10, 20))

        if self.round_over:
            text = f"{self.winner} wins!" if self.winner else "Draw!"
            renderer.draw_banner(
                surface,
                font,
                f"{text} Press R for a new round."
            )