import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (0, 0, 255)
CROSS_COLOR = (255, 0, 0)

# Game variables
board = [[' ' for _ in range(3)] for _ in range(3)]
current_player = 'X'
game_over = False
player1_score = 0
player2_score = 0
selected_game_mode = None

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')

def draw_grid():
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, i * HEIGHT / 3), (WIDTH, i * HEIGHT / 3), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * WIDTH / 3, 0), (i * WIDTH / 3, HEIGHT), LINE_WIDTH)

def draw_symbols():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                draw_cross(col * WIDTH / 3, row * HEIGHT / 3)
            elif board[row][col] == 'O':
                draw_circle(col * WIDTH / 3, row * HEIGHT / 3)

def draw_cross(x, y):
    pygame.draw.line(screen, CROSS_COLOR, (x + 50, y + 50), (x + WIDTH / 3 - 50, y + HEIGHT / 3 - 50), LINE_WIDTH)
    pygame.draw.line(screen, CROSS_COLOR, (x + WIDTH / 3 - 50, y + 50), (x + 50, y + HEIGHT / 3 - 50), LINE_WIDTH)

def draw_circle(x, y):
    pygame.draw.circle(screen, CIRCLE_COLOR, (int(x + WIDTH / 6), int(y + HEIGHT / 6)), int(WIDTH / 6 - 50), LINE_WIDTH)

def check_winner():
    for row in board:
        if all(cell == 'X' for cell in row) or all(cell == 'O' for cell in row):
            return True

    for col in range(3):
        if all(row[col] == 'X' for row in board) or all(row[col] == 'O' for row in board):
            return True

    if all(board[i][i] == 'X' for i in range(3)) or all(board[i][2 - i] == 'O' for i in range(3)):
        return True

    return False

def is_board_full():
    return all(cell != ' ' for row in board for cell in row)

def switch_player():
    global current_player
    if current_player == 'X':
        current_player = 'O'
    else:
        current_player = 'X'

def reset_game():
    global board, game_over
    board = [[' ' for _ in range(3)] for _ in range(3)]
    game_over = False

# AI opponent logic
def computer_move():
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
    if empty_cells:
        return random.choice(empty_cells)
    return None

# Main menu
def main_menu():
    font = pygame.font.Font(None, 36)
    text_one_player = font.render("One Player Game", True, LINE_COLOR)
    text_two_players = font.render("Two Players Game", True, LINE_COLOR)
    
    rect_one_player = text_one_player.get_rect(center=(WIDTH/2, HEIGHT/3))
    rect_two_players = text_two_players.get_rect(center=(WIDTH/2, 2*HEIGHT/3))

    while True:
        screen.fill(WHITE)
        screen.blit(text_one_player, rect_one_player)
        screen.blit(text_two_players, rect_two_players)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                if rect_one_player.collidepoint(mouseX, mouseY):
                    return "one_player"
                elif rect_two_players.collidepoint(mouseX, mouseY):
                    return "two_players"

selected_game_mode = main_menu()

# Game loop based on the selected game mode
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX, mouseY = event.pos
            clicked_row = int(mouseY // (HEIGHT / 3))
            clicked_col = int(mouseX // (WIDTH / 3))
            if board[clicked_row][clicked_col] == ' ':
                board[clicked_row][clicked_col] = current_player
                if check_winner():
                    print(f"Player {current_player} wins!")
                    if current_player == 'X':
                        player1_score += 1
                    else:
                        player2_score += 1
                    game_over = True
                elif is_board_full():
                    print("It's a tie!")
                    game_over = True
                else:
                    switch_player()

        # AI move in one-player mode
        if selected_game_mode == "one_player" and not game_over and current_player == 'O':
            computer_move_result = computer_move()
            if computer_move_result :
                ai_row, ai_col = computer_move_result
                board[ai_row][ai_col] = current_player
                if check_winner():
                    print("COMPUTER wins!")
                    player2_score += 1
                    game_over = True
                elif is_board_full():
                    print("It's a tie!")
                    game_over = True
                else:
                    switch_player()

    screen.fill(WHITE)
    draw_grid()
    draw_symbols()
    pygame.display.flip()

    if game_over:
        pygame.time.delay(2000)  # Delay for 2 seconds after game over
        reset_game()
        selected_game_mode = main_menu()