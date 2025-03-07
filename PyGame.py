import pygame
from game import Game

# Initialisierung von Pygame
pygame.init()

# Constants
X_GAME_SIZE = 7
Y_GAME_SIZE = 6
SQUARE_SIZE = 100
WIDTH = X_GAME_SIZE * SQUARE_SIZE
HEIGHT = Y_GAME_SIZE * SQUARE_SIZE + SQUARE_SIZE
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect Four")


def draw_selection(col):

    pygame.draw.rect(screen, BLACK, (0, 0, SQUARE_SIZE * X_GAME_SIZE, SQUARE_SIZE))
    if game.current_player == 1:
        pygame.draw.polygon(screen, YELLOW, [[col * SQUARE_SIZE + 25, 25], [col * SQUARE_SIZE + 50, 75],
                                          [col * SQUARE_SIZE + 75, 25]], 4)
    elif game.current_player == -1:
        pygame.draw.polygon(screen, RED, [[col * SQUARE_SIZE + 25, 25], [col * SQUARE_SIZE + 50, 75],
                                          [col * SQUARE_SIZE + 75, 25]], 4)
    pygame.display.update()


def draw_board(board):
    pygame.draw.rect(screen, BLACK, (0, 0, SQUARE_SIZE * X_GAME_SIZE, SQUARE_SIZE))
    for c in range(X_GAME_SIZE):
        for r in range(Y_GAME_SIZE):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK,
                               (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE * 3 / 2)),
                               int(SQUARE_SIZE / 2 - 5))

    for c in range(X_GAME_SIZE):
        for r in range(Y_GAME_SIZE):
            if board[r][c] == 1:
                pygame.draw.circle(screen, YELLOW,
                                   (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE / 2 + SQUARE_SIZE)),
                                   int(SQUARE_SIZE / 2 - 5))
            elif board[r][c] == -1:
                pygame.draw.circle(screen, RED,
                                   (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE / 2 + SQUARE_SIZE)),
                                   int(SQUARE_SIZE / 2 - 5))

    pygame.display.update()


def drop(board, row, col, player):
    """Animiert das Herunterfallen des Spielsteins."""
    y = SQUARE_SIZE/2  # Startposition außerhalb des sichtbaren Bereichs
    target_y = (row * SQUARE_SIZE + SQUARE_SIZE * 3 / 2)  # Zielposition

    if player == 1:
        color = YELLOW
    else:
        color = RED

    while y <= target_y:
        pygame.time.delay(15)  # Animationsgeschwindigkeit
        draw_board(board)  # Zeichne das Spielfeld neu, to show the board UNDERNEATH
        pygame.draw.circle(screen, color,
                           (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(y)),
                           int(SQUARE_SIZE / 2 - 5))
        pygame.display.update()
        y += 10  # Schrittweise Bewegung

def main():
    draw_board(game.board)  # Initial draw of the board
    pygame.display.update()
    running = True
    while running and not game.is_done():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(posx // SQUARE_SIZE)
                try:
                    action = game.map_number_to_action(col + 1)
                    if game.board[action[0], action[1]] == 0:
                        row, col = action
                        #drop(game.board, row, col, game.current_player)  # Animation!

                        game.make_move(action)
                        draw_board(game.board)
                        draw_selection(col)
                        pygame.display.update()


                except ValueError as e:
                    print(f"Invalid move: {e}")

            if event.type == pygame.MOUSEMOTION:
                posx = event.pos[0]
                col = int(posx // SQUARE_SIZE)
                draw_selection(col)


    winner = game.check_winner()
    if winner == 1:
        print('\033[93m' + "Spieler 1 hat gewonnen!")
    elif winner == -1:
        print('\033[91m' +"Spieler 2 hat gewonnen!")
    else:
        print("Unentschieden!")

if __name__ == '__main__':
    game = Game()
    draw_board(game.board)
    pygame.display.update()

    main()
