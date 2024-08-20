import pygame
import numpy as np
import random
import copy

# Colours
background = (187, 173, 160)
text_light = (249, 246, 242)
text_dark = (119, 110, 101)
colour0 = (204, 192, 179)
colour2 = (238, 228, 218)
colour4 = (237, 224, 200)
colour8 = (242, 177, 121)
colour16 = (245, 149, 99)
colour32 = (246, 124, 95)
colour64 = (246, 94, 59)
colour128 = (237, 207, 114)
colour256 = (237, 204, 97)
colour512 = (237, 200, 80)
colour1024 = (237, 197, 63)
colour2048 = (237, 194, 46)
colour4096 = (0, 0, 0)
colour8192 = (0, 0, 0)

colour_dict = {0:colour0, 2:colour2, 4:colour4, 8:colour8, 16:colour16, 32:colour32,
               64:colour64, 128:colour128, 256:colour256, 512:colour512, 1024:colour1024,
               2048:colour2048, 4096:colour4096, 8192:colour8192}

# Initialize
pygame.init()
pygame.display.set_caption('2048 game')

# Size of game window and font
dis_width = 552
dis_height = 680
dis = pygame.display.set_mode((dis_width, dis_height))
font = pygame.font.SysFont(None, 72)


def ai(tiles, score):
    directions = ['up', 'right', 'left', 'down']
    first_move_score = [0, 0, 0, 0]
    
    for i in range(4):
        tmp_score = 0
        arr = []
        score2 = score
        tiles2 = copy.deepcopy(tiles)
        tiles3 = copy.deepcopy(tiles2)
        tiles2, score2 = move(tiles2, directions[i], score2)
        tiles4 = copy.deepcopy(tiles2)

        if tiles3 != tiles2:
            tmp_score += score2
        else:
            continue
            
        for _ in range(40):
            tmp_score = 0
            num = 0
            tiles2 = copy.deepcopy(tiles4)

            while can_move(tiles2) and num < 20:
                tiles3 = copy.deepcopy(tiles2)
                tiles2, score2 = move(tiles2, directions[random.randint(0, 3)], score2)
                if tiles3 != tiles2:
                    tmp_score += score2
                    num += 1
            arr.append(tmp_score)
            
        first_move_score[i] = sum(arr) / len(arr)
    
    dir = directions[first_move_score.index(max(first_move_score))]
    return dir



def display(tiles, score, game_over=False):
    """Display the PyGame board.
    
    Args:
        tiles (list[list[int]]): 2D representation of the tiles on the board.
        score (int): The score of the game.
        game_over (bool): Boolean variable stating if game is over or not.
    
    Returns:
        None
    """
    dis.fill(background)

    # Draw tiles
    for i in range(4):
        for j in range(4):

            # Draw the square
            colour = colour_dict[tiles[i][j]]
            pygame.draw.rect(dis, colour, [8+136*i, 136+136*j, 128, 128], border_radius=10)

            # Add text to the rectangle
            if tiles[i][j] > 0:
                text_color = text_light if tiles[i][j] >= 8 else text_dark
                img = font.render(str(tiles[i][j]), True, text_color)
                img_rect = img.get_rect()
                img_rect.center = (8 + 136 * i + 128 // 2, 136 + 136 * j + 128 // 2)
                dis.blit(img, img_rect)

    # Add score to top of board
    img = font.render("Score: "+str(score), True, text_light)
    dis.blit(img, (26, 26))

    # Add game over text if no more moves
    if game_over:
        img = font.render("Game Over!", True, (0, 0, 0))
        img_rect = img.get_rect(center=(dis_width // 2, 30))
        dis.blit(img, img_rect)
        img = font.render("Q - quit  P - play again", True, (0, 0, 0))
        img_rect = img.get_rect(center=(dis_width // 2, 400))
        dis.blit(img, img_rect)
        
    pygame.display.update()
    

def new_tile(tiles):
    """Insert a 2 or 4 tile in a random empty spot after each move."""
    # Count the number of empty cells
    count = 0
    for i in range(4):
        for j in range(4):
            if tiles[i][j] == 0:
                count += 1
    
    # Choose a random empty cell
    place = random.randint(1, count)
    value = random.choice([2] * 9 + [4])  # 90% chance of 2, 10% chance of 4
    
    # Insert the 2 or 4 tile in the randomly chosen cell
    count = 0
    for i in range(4):
        for j in range(4):
            if tiles[i][j] == 0:
                count += 1
                if count == place:
                    tiles[i][j] = value
                    return tiles
                

def can_move(tiles):
    """Check if any legal moves are available. The are no more legal moves if
    there are no empty cells and no identical values next to each other.
    
    Args:
        tiles (list[list[int]]): 2D representation of the tiles on the board.
    
    Returns:
        bool: True if a move is possible, False otherwise.
    """
    # Check for any empty cells
    for i in range(4):
        for j in range(4):
            if tiles[i][j] == 0:
                return True
    
    # Check for any adjacent cells with the same value
    for i in range(4):
        for j in range(3):
            if tiles[i][j] == tiles[i][j + 1] or tiles[j][i] == tiles[j + 1][i]:
                return True
    
    return False
                
    
def move(tiles, direction, score):
    """Perform the actual moves in the 2048 game.
    
    Args:
        tiles (list[list[int]]): The 4x4 list representing the game board.
        direction (str): The direction of the move ('up', 'down', 'left', 'right').
        score (int): The current score of the game.
    
    Returns:
        tuple: The updated tiles and score.
    """
    tiles_temp = copy.deepcopy(tiles)
    
    for i in range(4):
        temp = []
        for j in range(4):
            if direction in ("up", "down"):
                if tiles[i][j] != 0:
                    temp.append(tiles[i][j])
            else:
                if tiles[j][i] != 0:
                    temp.append(tiles[j][i])

        if direction in ("up", "left"):
            k = 0
            while k < len(temp) - 1:
                if temp[k] == temp[k + 1]:
                    temp[k] *= 2
                    score += temp[k]
                    del temp[k + 1]
                    k += 1
                else:
                    k += 1
        elif direction in ("down", "right"):
            k = 1
            while k < len(temp):
                if temp[-k] == temp[-(k + 1)]:
                    temp[-(k + 1)] *= 2
                    score += temp[-(k + 1)]
                    del temp[-k]
                else:
                    k += 1

        for j in range(4):
            if j < len(temp):
                if direction == "up":
                    tiles[i][j] = temp[j]
                elif direction == "down":
                    tiles[i][3 - j] = temp[-(j + 1)]
                elif direction == "left":
                    tiles[j][i] = temp[j]
                elif direction == "right":
                    tiles[3 - j][i] = temp[-(j + 1)]
            else:
                if direction == "up":
                    tiles[i][j] = 0
                elif direction == "down":
                    tiles[i][3 - j] = 0
                elif direction == "left":
                    tiles[j][i] = 0
                elif direction == "right":
                    tiles[3 - j][i] = 0

    # If the move didn't change the position, then don't add a
    # new tile - i.e. it was not a valid move so it was ignored
    if tiles_temp != tiles:
        tiles = new_tile(tiles)

    return tiles, score


def game_loop():
    """Start a game of 2048."""
    # Initialize empty board with two random tiles (2 or 4)
    game_over = False
    score = 0
    tiles = [[0, 0, 0, 0] for _ in range(4)]
    new_tile(tiles)
    new_tile(tiles)

    while True:
        # Display message showing score and options (play again or quit)
        display(tiles, score, game_over)

        # Check for game over condition
        if not game_over:
            game_over = not can_move(tiles)
        
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if game_over:
                    # If game is over, allow the user to play again or quit
                    if event.key == pygame.K_q:
                        pygame.quit()
                    elif event.key == pygame.K_p:
                        # Reset game
                        game_over = False
                        score = 0
                        tiles = [[0, 0, 0, 0] for _ in range(4)]
                        new_tile(tiles)
                        new_tile(tiles)
                else:
                    # If game is not over, allow the user to make moves
                    if event.key == pygame.K_UP:
                        tiles, score = move(tiles, "up", score)
                    elif event.key == pygame.K_DOWN:
                        tiles, score = move(tiles, "down", score)
                    elif event.key == pygame.K_LEFT:
                        tiles, score = move(tiles, "left", score)
                    elif event.key == pygame.K_RIGHT:
                        tiles, score = move(tiles, "right", score)
                    elif event.key == pygame.K_SPACE:
                        # Activate AI
                        while True:
                            if not can_move(tiles):
                                game_over = True
                                break

                            # Select AI
                            dir = ai(tiles, score)

                            # Perform move and update board
                            tiles, score = move(tiles, dir, score)
                            display(tiles, score, game_over)
                            pygame.display.update()
                            # pygame.time.wait(100)  # Delay for smoother visualization


# Starts game
game_loop()