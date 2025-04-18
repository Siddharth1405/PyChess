import pygame
import chess
import chess.engine
import os

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700 
SQ_SIZE = WIDTH // 8
WHITE = (238, 238, 210)
GREEN = (118, 150, 86)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GREEN_TEXT = (0, 200, 0)
FONT = pygame.font.Font(None, 36)

# Load images
pieces = {}
image_path = os.path.join(os.path.dirname(__file__), 'images')
piece_names = {
    'p': 'blackpawn', 'r': 'blackrook', 'n': 'blackknight', 'b': 'blackbishop', 'q': 'blackqueen', 'k': 'blackking',
    'P': 'whitepawn', 'R': 'whiterook', 'N': 'whiteknight', 'B': 'whitebishop', 'Q': 'whitequeen', 'K': 'whiteking'
}
for piece, filename in piece_names.items():
    piece_file = os.path.join(image_path, f'{filename}.png')
    if os.path.exists(piece_file):
        pieces[piece] = pygame.transform.scale(pygame.image.load(piece_file), (SQ_SIZE, SQ_SIZE))
    else:
        print(f"Warning: Missing image file {piece_file}")

# Initialize board
board = chess.Board()
move_history = []
redo_stack = []

# Load Stockfish engine
engine_path = r"YOUR_PATH_TO\stockfish-windows-x86-64-avx2.exe" 
try:
    engine = chess.engine.SimpleEngine.popen_uci(engine_path)
except:
    print("ERROR: Stockfish not found! Please download it from:")
    print("https://stockfishchess.org/download/")
    exit()

#Prints board
def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else GREEN
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

#Prints pieces
def draw_pieces():
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_symbol = piece.symbol()
            col, row = chess.square_file(square), 7 - chess.square_rank(square)
            if selected_square and chess.parse_square(selected_square) == square:
                pygame.draw.rect(screen, YELLOW, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            screen.blit(pieces[piece_symbol], (col * SQ_SIZE, row * SQ_SIZE))

#Prints bottom menu
def draw_menu():
    pygame.draw.rect(screen, BLACK, pygame.Rect(0, HEIGHT - 100, WIDTH, 100))
    
    if board.is_checkmate():
        winner = "White" if not board.turn else "Black"
        winner_text = FONT.render(f"Checkmate! {winner} wins", True, GREEN_TEXT)
        screen.blit(winner_text, ((WIDTH - winner_text.get_width()) // 2, HEIGHT - 80))
    elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves():
        draw_text = FONT.render("Game Draw!", True, GREEN_TEXT)
        screen.blit(draw_text, ((WIDTH - draw_text.get_width()) // 2, HEIGHT - 80))
    else:
        turn_text = FONT.render(f"Turn: {'White' if board.turn else 'Black'}", True, WHITE)
        screen.blit(turn_text, (20, HEIGHT - 80))

    if not single_player:

        undo_text = FONT.render("Undo", True, GREEN)
        redo_text = FONT.render("Redo", True, GREEN)
        screen.blit(undo_text, (450, HEIGHT - 80))
        screen.blit(redo_text, (530, HEIGHT - 80))

def bot_move():
    if not board.turn and not game_over:
        result = engine.play(board, chess.engine.Limit(time=2.0))
        board.push(result.move)

#Prints Start menu
def draw_start_menu():
    screen.fill(BLACK)

    
    title_font = pygame.font.Font(None, 88) 
    button_font = pygame.font.Font(None, 44)  

    title_text = title_font.render("Chess", True, WHITE)
    single_player_text = button_font.render("Single Player", True, BLACK)
    multi_player_text = button_font.render("Two Player", True, BLACK)
    quit_text = button_font.render("Quit Game", True, BLACK)

    # Center title properly
    title_x = (WIDTH - title_text.get_width()) // 2
    screen.blit(title_text, (title_x, 80))

    # Button positions
    button_width, button_height = 240, 60  # Slightly larger buttons
    button_x = (WIDTH - button_width) // 2

    pygame.draw.rect(screen, GREEN, (button_x, 250, button_width, button_height))
    pygame.draw.rect(screen, GREEN, (button_x, 330, button_width, button_height))
    pygame.draw.rect(screen, RED, (button_x, 410, button_width, button_height))

    # Center button text inside buttons
    screen.blit(single_player_text, (button_x + (button_width - single_player_text.get_width()) // 2, 260))
    screen.blit(multi_player_text, (button_x + (button_width - multi_player_text.get_width()) // 2, 340))
    screen.blit(quit_text, (button_x + (button_width - quit_text.get_width()) // 2, 420))

    pygame.display.flip()

#Prints promotion menu
def choose_promotion():
    """Displays a GUI menu to choose a piece for promotion."""
    promotion_options = {
        "Q": (chess.QUEEN, "whitequeen.png"),
        "R": (chess.ROOK, "whiterook.png"),
        "N": (chess.KNIGHT, "whiteknight.png"),
        "B": (chess.BISHOP, "whitebishop.png"),
    }

  
    menu_width, menu_height = 400, 120
    menu_x, menu_y = (WIDTH - menu_width) // 2, (HEIGHT - menu_height) // 2

   
    pygame.draw.rect(screen, BLACK, (menu_x, menu_y, menu_width, menu_height))
    pygame.draw.rect(screen, WHITE, (menu_x, menu_y, menu_width, menu_height), 3)

  
    button_size = 80
    spacing = 20
    x_offset = menu_x + spacing
    buttons = {}

    for key, (piece, img) in promotion_options.items():
        piece_img = pygame.image.load(os.path.join(image_path, img))
        piece_img = pygame.transform.scale(piece_img, (button_size, button_size))
        screen.blit(piece_img, (x_offset, menu_y + 20))
        buttons[key] = pygame.Rect(x_offset, menu_y + 20, button_size, button_size)
        x_offset += button_size + spacing

    pygame.display.flip()

   
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for key, rect in buttons.items():
                    if rect.collidepoint(mx, my):
                        return promotion_options[key][0]  

#Prints difficulty menu
def select_difficulty():
    screen.fill(BLACK)
    
    title_font = pygame.font.Font(None, 72)
    button_font = pygame.font.Font(None, 48)

    title_text = title_font.render("Select Difficulty", True, WHITE)
    easy_text = button_font.render("Easy", True, BLACK)
    medium_text = button_font.render("Medium", True, BLACK)
    hard_text = button_font.render("Hard", True, BLACK)
    impossible_text = button_font.render("Impossible", True, BLACK)

    title_x = (WIDTH - title_text.get_width()) // 2
    screen.blit(title_text, (title_x, 80))

    button_width, button_height = 240, 60
    button_x = (WIDTH - button_width) // 2

    pygame.draw.rect(screen, GREEN, (button_x, 200, button_width, button_height))
    pygame.draw.rect(screen, YELLOW, (button_x, 280, button_width, button_height))
    pygame.draw.rect(screen, ORANGE, (button_x, 360, button_width, button_height))
    pygame.draw.rect(screen, RED, (button_x, 440, button_width, button_height))

    screen.blit(easy_text, (button_x + (button_width - easy_text.get_width()) // 2, 210))
    screen.blit(medium_text, (button_x + (button_width - medium_text.get_width()) // 2, 290))
    screen.blit(hard_text, (button_x + (button_width - hard_text.get_width()) // 2, 370))
    screen.blit(impossible_text, (button_x + (button_width - impossible_text.get_width()) // 2, 450))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if button_x <= x <= button_x + button_width:
                    if 200 <= y <= 260:
                        return 0  
                    elif 280 <= y <= 340:
                        return 4 
                    elif 360 <= y <= 420:
                        return 10  
                    elif 440 <= y <= 500:
                        return None

def start_menu():
    global single_player, skill_level
    while True:
        draw_start_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 180 <= x <= 420 and 250 <= y <= 310:  
                    single_player = True
                    skill_level = select_difficulty()  
                    if skill_level is not None:
                        engine.configure({"Skill Level": skill_level})
                    return
                elif 180 <= x <= 420 and 330 <= y <= 390: 
                    single_player = False
                    return
                elif 180 <= x <= 420 and 410 <= y <= 470:  
                    pygame.quit()
                    engine.quit() 
                    exit()


# Start menu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")
single_player = False
start_menu()

running = True
selected_square = None
game_over = False

while running:
    draw_board()
    draw_pieces()
    draw_menu() 
    if board.is_checkmate():
        king_square = board.king(board.turn)
        col, row = chess.square_file(king_square), 7 - chess.square_rank(king_square)
        pygame.draw.rect(screen, RED, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        winner = "White" if not board.turn else "Black"
        game_over = True
    
    pygame.display.flip()
    
    if single_player and not board.turn and not game_over:
        pygame.time.delay(500)
        bot_move()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                start_menu()
                board.reset()
                game_over = False
                selected_square = None
            else:
                x, y = pygame.mouse.get_pos()
                if not single_player and HEIGHT - 90 <= y <= HEIGHT - 50:
                   if 450 <= x <= 510 and move_history:
                     if move_history:  
                      redo_stack.append(board.pop())
                      move_history.pop()
                     else:
                      print("No moves to undo.")
                   elif 530 <= x <= 590 and redo_stack:
                     board.push(redo_stack.pop())
                     move_history.append(move)
                else:
                    if single_player and not board.turn:
                        print("Please wait, it is not your turn.")
                        continue
                    square = chess.square_name(chess.square(x // SQ_SIZE, 7 - (y // SQ_SIZE)))
                    if selected_square == square:
                        selected_square = None
                    elif selected_square:
                        move = chess.Move.from_uci(selected_square + square)
                        if board.piece_at(move.from_square) and board.piece_at(move.from_square).piece_type == chess.PAWN:
                         if chess.square_rank(move.to_square) in [0, 7]: 
                          promotion_choice = choose_promotion()
                          move = chess.Move(move.from_square, move.to_square, promotion=promotion_choice)  
                        if move in board.legal_moves:
                            board.push(move)
                            move_history.append(move)
                            redo_stack.clear()
                            selected_square = None
                        else:
                            print("Illegal move!")
                            selected_square = None
                    else:
                        selected_square = square

pygame.quit()
engine.quit()
