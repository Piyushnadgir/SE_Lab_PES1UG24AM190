"""
renderer: all pygame drawing lives here,
kept separate from game logic.
"""

import pygame


# -----------------------------------
# WINDOW / BOARD
# -----------------------------------

WIDTH, HEIGHT = 400, 630

BOARD_SIZE = 360
CELL_SIZE = BOARD_SIZE // 3
BOARD_TOP = 100

WINDOW_SIZE = (WIDTH, HEIGHT)


# -----------------------------------
# COLORS
# -----------------------------------

COLOR_BG = (245, 245, 245)
COLOR_LINE = (60, 60, 60)

COLOR_X = (200, 60, 60)
COLOR_O = (60, 100, 200)

COLOR_TEXT = (30, 30, 30)

COLOR_BUTTON = (220, 220, 220)
COLOR_BUTTON_HOVER = (200, 200, 200)
COLOR_BUTTON_BORDER = (100, 100, 100)


# -----------------------------------
# BUTTON POSITIONS
# -----------------------------------

# Who starts next round
START_TOGGLE_RECT = pygame.Rect(
    10,
    475,
    180,
    45
)

# Start new round
NEW_ROUND_RECT = pygame.Rect(
    200,
    475,
    190,
    45
)

# Reset entire match
RESET_MATCH_RECT = pygame.Rect(
    10,
    525,
    180,
    35
)


# -----------------------------------
# BOARD INPUT
# -----------------------------------

def board_pos_to_cell(pos):
    x, y = pos

    y -= BOARD_TOP

    if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
        return None

    col = x // CELL_SIZE
    row = y // CELL_SIZE

    return int(row), int(col)


# -----------------------------------
# DRAW BOARD
# -----------------------------------

def draw_board(surface, board):
    surface.fill(COLOR_BG)

    # Grid lines
    for i in range(1, 3):
        pygame.draw.line(
            surface,
            COLOR_LINE,
            (i * CELL_SIZE, BOARD_TOP),
            (
                i * CELL_SIZE,
                BOARD_TOP + BOARD_SIZE
            ),
            3
        )

        pygame.draw.line(
            surface,
            COLOR_LINE,
            (
                0,
                BOARD_TOP + i * CELL_SIZE
            ),
            (
                BOARD_SIZE,
                BOARD_TOP + i * CELL_SIZE
            ),
            3
        )

    # Symbols
    for r in range(3):
        for c in range(3):

            symbol = board[r][c]

            if symbol is None:
                continue

            center = (
                c * CELL_SIZE + CELL_SIZE // 2,
                BOARD_TOP + r * CELL_SIZE + CELL_SIZE // 2
            )

            if symbol == 'X':

                offset = CELL_SIZE // 3

                pygame.draw.line(
                    surface,
                    COLOR_X,
                    (
                        center[0] - offset,
                        center[1] - offset
                    ),
                    (
                        center[0] + offset,
                        center[1] + offset
                    ),
                    6
                )

                pygame.draw.line(
                    surface,
                    COLOR_X,
                    (
                        center[0] + offset,
                        center[1] - offset
                    ),
                    (
                        center[0] - offset,
                        center[1] + offset
                    ),
                    6
                )

            else:

                pygame.draw.circle(
                    surface,
                    COLOR_O,
                    center,
                    CELL_SIZE // 3,
                    6
                )


# -----------------------------------
# TEXT
# -----------------------------------

def draw_text(
    surface,
    font,
    text,
    pos,
    color=COLOR_TEXT
):
    surface.blit(
        font.render(text, True, color),
        pos
    )


# -----------------------------------
# BUTTONS
# -----------------------------------

def draw_button(
    surface,
    rect,
    text,
    font
):
    mouse_pos = pygame.mouse.get_pos()

    if rect.collidepoint(mouse_pos):
        color = COLOR_BUTTON_HOVER
    else:
        color = COLOR_BUTTON

    # Button background
    pygame.draw.rect(
        surface,
        color,
        rect,
        border_radius=6
    )

    # Button border
    pygame.draw.rect(
        surface,
        COLOR_BUTTON_BORDER,
        rect,
        width=2,
        border_radius=6
    )

    # Center text
    text_surface = font.render(
        text,
        True,
        COLOR_TEXT
    )

    text_rect = text_surface.get_rect(
        center=rect.center
    )

    surface.blit(
        text_surface,
        text_rect
    )


# -----------------------------------
# END-OF-ROUND BANNER
# -----------------------------------

def draw_banner(surface, font, text):
    surf = font.render(
        text,
        True,
        (180, 40, 40)
    )

    rect = surf.get_rect(
        center=(
            surface.get_width() // 2,
            BOARD_TOP + BOARD_SIZE + 40
        )
    )

    surface.blit(
        surf,
        rect
    )