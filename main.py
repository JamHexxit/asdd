import pygame
import chess
import chess.engine
import random 

pygame.init()

screen_width = 640
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Chess Game")

board = chess.Board()

font = pygame.font.SysFont(None, 48)

player_color = chess.WHITE
print(player_color)

def draw_board():
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                color = pygame.Color("white")
            else:
                color = pygame.Color("gray")
            rect = pygame.Rect(col*80, row*80, 80, 80)
            pygame.draw.rect(screen, color, rect)
            square = chess.square(col, 7-row)
            piece = board.piece_at(square)
            if piece is not None:
                text = font.render(piece.symbol(), True, pygame.Color("black"))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def main():
    engine_path = "G:/VSC/py/engine/stockfish-windows-2022-x86-64-avx2.exe"
    engine = chess.engine.SimpleEngine.popen_uci(engine_path)
    selected_piece = None
    piece_square = None
    while True:
        current_player = board.turn
        if current_player is chess.BLACK:
            legal_moves = [move for move in board.legal_moves if board.color_at(move.from_square) == chess.BLACK]
            random_move = random.choice(list(legal_moves))
            info = engine.analyse(board, chess.engine.Limit(time=5.0), root_moves=[random_move])
            score = info["score"].relative.score()
            board.push(random_move)
            print(score)
            if score is None:
                board.reset()
                engine.quit()
                engine = chess.engine.SimpleEngine.popen_uci(engine_path)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                engine.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row = 7- mouse_y//80
                col = mouse_x//80
                square = chess.square(col,row)
                piece = board.piece_at(square)
                if piece is not None and piece.color == player_color:
                    selected_piece = piece
                    piece_square = square
                    
                else :
                    if selected_piece is not None:
                        back_rank = 7
                        move = chess.Move(piece_square,square)
                        if selected_piece.piece_type == chess.PAWN and chess.square_rank(move.to_square) == back_rank:
                            print(1)
                            move = chess.Move(piece_square, square, promotion=chess.QUEEN)
                        if move in board.legal_moves:
                            board.push(move)   
                            selected_piece = None
                            piece_square = None
                        else:
                            selected_piece = None
                            piece_square = None





        screen.fill(pygame.Color("white"))
        draw_board()
        pygame.display.update()

if __name__ == "__main__":
    main()