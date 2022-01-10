import pygame as p
from Engine import *

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT / DIMENSION
MOVE_LOG_WIDTH = 280
MOVE_LOG_HEIGHT = HEIGHT
MAX_FPS = 15
IMAGES = {}
COLORS = [p.Color("white"), p.Color("tan")]


def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.image.load("images/" + piece + ".png")

def run(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    p.init()
    screen = p.display.set_mode((WIDTH + MOVE_LOG_WIDTH, HEIGHT))
    clock = p.time.Clock()
    move_log_font = p.font.SysFont("Helvitca", 16, True, False)
    heading_font = p.font.SysFont("Helvitca", 32, True, False)
    screen.fill(p.Color("white"))
    gs = Engine(fen)
    load_images()
    running = True
    sq_selected = ()
    player_clicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (X,Y) location of mouse cursor
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col) or col >= 8: # Clicked same square twice or clicked move log
                    sq_selected = () # Deselect
                    player_clicks = [] # Clear
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)
                if len(player_clicks) == 2: # After second click
                    if gs.official_board.BOARD[translate(player_clicks[0])] != "-" and gs.official_board.BOARD[translate(player_clicks[1])] != "-" and gs.official_board.BOARD[translate(player_clicks[0])].color == gs.official_board.BOARD[translate(player_clicks[1])].color:
                        sq_selected = player_clicks[1]
                        player_clicks = [sq_selected]
                    else:
                        move = (translate(player_clicks[0]), translate(player_clicks[1]))
                        gs.gui_move(move)
                        sq_selected = () # Reset
                        player_clicks = [] # Reset


        draw_game_state(screen, gs, sq_selected, move_log_font, heading_font)
        clock.tick(MAX_FPS)
        p.display.flip() 

def translate(tup):
    x, y = tup[0], tup[1]
    return int((7-x) * 8 + y)

def untranslate(index):
    x = 7 - (index // 8)
    y = index - ((7-x) * 8)
    return (x, y)

def highlight_squares(screen, gs, sq_selected):
    if sq_selected != ():
        r, c = sq_selected
        if gs.official_board.BOARD[translate(sq_selected)] != "-" and gs.official_board.BOARD[translate(sq_selected)].color == gs.official_board.side_to_move:
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # transparency
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('yellow'))
            possible_moves = gs.generate_legal_moves(gs.official_board)
            for move_tuple in possible_moves:
                if move_tuple[1] == translate(sq_selected):
                    move = untranslate(move_tuple[2])
                    screen.blit(s, (move[1] * SQ_SIZE, move[0] * SQ_SIZE))

def draw_game_state(screen, gs, sq_selected, move_log_font, heading_font):
    draw_board(screen)
    highlight_squares(screen, gs, sq_selected)
    draw_pieces(screen, gs.official_board)
    draw_move_log(screen, gs, move_log_font, heading_font)

def draw_board(screen):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = COLORS[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        
def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board.BOARD[c + (7-r) * 8]
            if piece != "-":
                screen.blit(IMAGES[piece.gui_id], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_move_log(screen, gs, font, heading_font):
    heading_log_rect = p.Rect(WIDTH, 0, MOVE_LOG_WIDTH, 30)
    p.draw.rect(screen, p.Color('white'), heading_log_rect)
    text_obj = heading_font.render("Tilapia 1.0", True, p.Color('black'))
    text_loc = heading_log_rect.move(5, 5)
    screen.blit(text_obj, text_loc)
    screen.blit(p.image.load("images/tilapia_2_60x30.png"), p.Rect(WIDTH + 150, 0, 60, 30))
    move_log_rect = p.Rect(WIDTH, 30, MOVE_LOG_WIDTH, MOVE_LOG_HEIGHT)
    p.draw.rect(screen, p.Color('black'), move_log_rect)
    move_log = gs.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_str = str(i // 2 + 1) + ". " + move_log[i] + " "
        if i + 1 < len(move_log):
            move_str += move_log[i + 1] + " "
        move_texts.append(move_str)

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    textY = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]
        text_obj = font.render(text, True, p.Color('white'))
        text_loc = move_log_rect.move(padding, textY)
        screen.blit(text_obj, text_loc)
        textY += text_obj.get_height() + line_spacing

run()


