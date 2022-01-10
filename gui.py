import pygame as p
from Engine import *

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT / DIMENSION
MAX_FPS = 15
IMAGES = {}
COLORS = [p.Color("white"), p.Color("tan")]


def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.image.load("images/" + piece + ".png")

def run(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
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
                if sq_selected == (row, col): # Clicked same square twice
                    sq_selected = () # Deselect
                    player_clicks = [] # Clear
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)
                if len(player_clicks) == 2: # After second click
                    move = (translate(player_clicks[0]), translate(player_clicks[1]))
                    print(move)
                    gs.gui_move(move)
                    sq_selected = () # Reset
                    player_clicks = [] # Reset


        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip() 

def translate(tup):
    x, y = tup[0], tup[1]
    return (7-x) * 8 + y

def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.official_board)

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

run()


