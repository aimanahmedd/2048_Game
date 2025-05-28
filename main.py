import pygame
import random

pygame.init()

FPS = 60

WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
timer = pygame.time.Clock()
FPS = 60
font = pygame.font.Font("freesansbold.ttf", 24)

#2048 game color library
colors = {0: (255, 182, 193, 255),
          2: (255, 174, 185, 255),
          4: (238, 162, 173, 255),
          8: (205, 140, 149, 255),
          16: (255, 160, 122, 255),
          32:(255, 192, 203, 255),
          64:(139, 10, 80, 255),
          128:(238, 169, 184, 255),
          256:(205, 145, 158, 255),
          512:(139, 99, 108, 255),
          1024:(255, 20, 147, 255),
          2048:(255, 20, 147, 255),
          "light text": (245, 255, 250, 255),
          "dark text" : (119, 110, 101),
          "other" : (0, 0, 0),
          "bg" : (238, 169, 184, 255)}
          
#2048 taylor swift album image
albums = {2: pygame.image.load("debut.png"),
          4: pygame.image.load("fearless.jpg"),
          8: pygame.image.load("speak_now.png"),
          16: pygame.image.load("red.png"),
          32: pygame.image.load("1989.png"),
          64: pygame.image.load("rep.webp"),
          128: pygame.image.load("lover.png"),
          256: pygame.image.load("folklore.png"),
          512: pygame.image.load("evermore.png"),
          1024: pygame.image.load("midnights.png"),
          2048: pygame.image.load("ttpd.jpg")}

for key in albums:
    albums[key] = pygame.transform.scale(albums[key], (75, 75))
          
#game variables initialize
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
file = open("high_score.py", "r")
init_high = int(file.readline())
file.close()
high_score = init_high

#draw game over + restart text
def draw_over():
    pygame.draw.rect(screen, 'cadetblue1', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'lightpink3')
    game_over_text2 = font.render('Press Enter to Restart', True, 'lightpink3')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))    



#turn based on direction
def take_turn(direction, board):
    global score
    merged = [ [False for _ in range(4)] for _ in range(4)]
    if direction == "UP":
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True
                        
    elif direction == "DOWN":
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True
    elif direction == "LEFT":
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direction == "RIGHT":
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board
    

#spawning pieces when turn starts
def new_pieces(board):
    count = 0
    full = False
    #checking if there is a 0 in the board
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0,3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


#draw background for board
def draw_board():
    pygame.draw.rect(screen, colors["bg"], [0, 0, 400, 400], 0, 10)
    score_text = font.render("Score " + str(score), True, 'cadetblue')
    high_score_text = font.render("High  " + str(high_score), True, 'cadetblue')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))
    pass

#draw tiles
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value in albums:
                # Get the corresponding album image
                image = albums[value]
                # Draw the image on the tile
                screen.blit(image, (j * 95 + 20, i * 95 + 20))
            else:
                # If value is not in album_images, draw an empty tile
                pygame.draw.rect(screen, colors[0], [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)


def check_game_over(board):
    if any(0 in row for row in board):
        return False
    for i in range(4):
        for j in range(4):
            if i < 3 and board[i][j] == board[i + 1][j]:
                return False
            if j < 3 and board[i][j] == board[i][j + 1]:
                return False
    return True


#main game loop!
run = True
while run:
    timer.tick(FPS)
    screen.fill('pink')
    draw_board()
    draw_pieces(board_values)
    if spawn_new or init_count < 2:
        new_pieces(board_values)
        spawn_new = False
        init_count += 1
        
    if direction != "":
        board_values = take_turn(direction, board_values)
        direction = ""
        spawn_new = True

    game_over = check_game_over(board_values)

    if game_over:
        draw_over()
        if high_score > init_high:
            with open('high_score', 'w') as file:
                file.write(str(high_score))
            init_high = high_score
            
            
            
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
                
            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    score = 9
                    direction = ""
                    game_over = False
                    
                
    if score> high_score:
        high_score = score
                
    pygame.display.flip()
    
pygame.quit()