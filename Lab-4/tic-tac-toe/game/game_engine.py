"""
GameEngine: owns the board, turn state, round-end logic,
persistent match scoreboard, and UI controls.

Player = X
Computer = O

R = New Round
M = Reset Match
"""

import pygame

from game.rules import check_winner, is_board_full
from game.renderer import (
    board_pos_to_cell,
    START_TOGGLE_RECT,
    NEW_ROUND_RECT,
    RESET_MATCH_RECT,
)
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

        # Who should start the NEXT round
        self.starting_player = HUMAN_SYMBOL

    def handle_click(self, pos):
        """
        Handle both UI buttons and board clicks.
        """

        # -----------------------------------
        # UI BUTTONS
        # -----------------------------------

        # Toggle who starts the NEXT round
        if START_TOGGLE_RECT.collidepoint(pos):
            if self.starting_player == HUMAN_SYMBOL:
                self.starting_player = COMPUTER_SYMBOL
            else:
                self.starting_player = HUMAN_SYMBOL

            return

        # New Round button
        if NEW_ROUND_RECT.collidepoint(pos):
            self.new_round()
            return

        # Reset Match button
        if RESET_MATCH_RECT.collidepoint(pos):
            self.reset_match()
            return

        # -----------------------------------
        # BOARD
        # -----------------------------------

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
        """
        Let the computer make its move.

        This is also used when O is selected to start
        a new round.
        """

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

        A winning move can also fill the final empty cell,
        so a winner must always be checked before a draw.
        """

        winner = check_winner(self.board)

        # Winner takes priority over draw
        if winner:
            self.round_over = True
            self.winner = winner

            if winner == HUMAN_SYMBOL:
                self.x_wins += 1

            elif winner == COMPUTER_SYMBOL:
                self.o_wins += 1

            return

        # Only check for draw if nobody won
        if is_board_full(self.board):
            self.round_over = True
            self.winner = None
            self.draws += 1

    def new_round(self):
        """
        Restart only the current round.

        The scoreboard stays unchanged.

        The selected starting player is applied here.
        """

        self.board = [[None] * 3 for _ in range(3)]

        self.round_over = False
        self.winner = None

        # Apply the selected starting player
        self.current_player = self.starting_player

        # If O starts, computer moves automatically
        if self.current_player == COMPUTER_SYMBOL:
            self._maybe_take_computer_turn()

    def reset_match(self):
        """
        Reset the entire match.

        Clears:
            - Board
            - X wins
            - O wins
            - Draws

        The selected starting player is preserved.
        """

        # Clear scoreboard
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0

        # Start a fresh round using the selected starting player
        self.new_round()

    def handle_keydown(self, key):
        """
        Keyboard controls:

        R = New Round
        M = Reset Match
        """

        if key == pygame.K_r:
            self.new_round()

        elif key == pygame.K_m:
            self.reset_match()

    def draw(self, surface, font, small_font):
        """
        Draw the complete game UI.
        """

        from game import renderer

        # -----------------------------------
        # BOARD
        # -----------------------------------

        renderer.draw_board(surface, self.board)

        # -----------------------------------
        # SCOREBOARD
        # -----------------------------------

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

        # -----------------------------------
        # STARTING PLAYER
        # -----------------------------------

        renderer.draw_button(
            surface,
            START_TOGGLE_RECT,
            f"Next: {self.starting_player} starts",
            small_font
        )

        # -----------------------------------
        # ROUND BUTTONS
        # -----------------------------------

        renderer.draw_button(
            surface,
            NEW_ROUND_RECT,
            "New Round",
            small_font
        )

        renderer.draw_button(
            surface,
            RESET_MATCH_RECT,
            "Reset Match",
            small_font
        )

        # -----------------------------------
        # GAME STATUS
        # -----------------------------------

        if self.round_over:

            if self.winner:
                result_text = f"{self.winner} wins!"
            else:
                result_text = "Draw!"

            renderer.draw_text(
                surface,
                small_font,
                result_text,
                (10, 565)
            )

        else:

            if self.current_player == HUMAN_SYMBOL:
                turn_text = "Your turn (X)"
            else:
                turn_text = "Computer's turn (O)"

            renderer.draw_text(
                surface,
                small_font,
                turn_text,
                (10, 565)
            )

        # Keyboard hint
        renderer.draw_text(
            surface,
            small_font,
            "R: New Round    M: Reset Match",
            (10, 595)
        )