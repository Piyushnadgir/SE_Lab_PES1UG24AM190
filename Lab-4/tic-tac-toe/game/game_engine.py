"""
GameEngine: owns the board, turn state, round-end logic,
and persistent match scoreboard.

Player = X
Computer = O

R = New round
M = Reset entire match
"""

import pygame

from game.rules import check_winner, is_board_full
from game.renderer import board_pos_to_cell
from game.ai import choose_move


HUMAN_SYMBOL = 'X'
COMPUTER_SYMBOL = 'O'


class GameEngine:
    def __init__(self):
        # Current round
        self.board = [[None] * 3 for _ in range(3)]
        self.current_player = HUMAN_SYMBOL
        self.round_over = False
        self.winner = None

        # Persistent match scoreboard
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0

    def handle_click(self, pos):
        # Don't allow moves after the round has ended
        if self.round_over:
            return

        # Only X can make a human move
        if self.current_player != HUMAN_SYMBOL:
            return

        cell = board_pos_to_cell(pos)

        if cell is None:
            return

        row, col = cell

        # Don't allow clicking an occupied cell
        if self.board[row][col] is not None:
            return

        # Place X
        self.board[row][col] = HUMAN_SYMBOL

        # Check if X ended the round
        self.check_round_end()

        # If X won or caused a draw, stop here
        if self.round_over:
            return

        # Computer's turn
        self.current_player = COMPUTER_SYMBOL

        self._maybe_take_computer_turn()

    def _maybe_take_computer_turn(self):
        # Don't let computer move after round has ended
        if self.round_over:
            return

        if self.current_player != COMPUTER_SYMBOL:
            return

        move = choose_move(self.board)

        if move is None:
            return

        row, col = move

        # Place O
        self.board[row][col] = COMPUTER_SYMBOL

        # Check if O ended the round
        self.check_round_end()

        # If O won or caused a draw, stop here
        if self.round_over:
            return

        # Back to player's turn
        self.current_player = HUMAN_SYMBOL

    def check_round_end(self):
        """
        Check winner FIRST.

        This is important because the final empty cell
        can also be the winning move.
        """

        winner = check_winner(self.board)

        # Winner takes priority over draw
        if winner:
            self.round_over = True
            self.winner = winner

            # Update persistent scoreboard
            if winner == HUMAN_SYMBOL:
                self.x_wins += 1
            elif winner == COMPUTER_SYMBOL:
                self.o_wins += 1

            return

        # Only check for draw if nobody won
        if is_board_full(self.board):
            self.round_over = True
            self.winner = None

            # Update persistent scoreboard
            self.draws += 1

    def new_round(self):
        """
        Start a new round.

        The scoreboard stays unchanged.
        """

        self.board = [[None] * 3 for _ in range(3)]
        self.current_player = HUMAN_SYMBOL
        self.round_over = False
        self.winner = None

    def reset_match(self):
        """
        Reset the entire match.

        Both the board and scoreboard are cleared.
        """

        self.board = [[None] * 3 for _ in range(3)]
        self.current_player = HUMAN_SYMBOL
        self.round_over = False
        self.winner = None

        # Reset scoreboard
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0

    def handle_keydown(self, key):
        """
        Keyboard controls:

        R = New round
        M = Reset entire match
        """

        if key == pygame.K_r:
            self.new_round()

        elif key == pygame.K_m:
            self.reset_match()

    def draw(self, surface, font):
        from game import renderer

        # Draw board
        renderer.draw_board(surface, self.board)

        # Compact persistent scoreboard
        # Short labels keep everything inside the window.
        scoreboard = (
            f"X: {self.x_wins}    "
            f"O: {self.o_wins}    "
            f"D: {self.draws}"
        )

        renderer.draw_text(
            surface,
            font,
            scoreboard,
            (10, 20)
        )

        # Current turn / round result
        if self.round_over:
            if self.winner:
                result_text = f"{self.winner} wins!"
            else:
                result_text = "Draw!"

            renderer.draw_banner(
                surface,
                font,
                f"{result_text}  Press R for a new round."
            )

        else:
            if self.current_player == HUMAN_SYMBOL:
                turn_text = "Your turn (X)"
            else:
                turn_text = "Computer's turn (O)"

            renderer.draw_text(
                surface,
                font,
                turn_text,
                (10, 50)
            )