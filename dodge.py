import pygame
from random import randint
from pygame import mixer
from os import listdir,getcwd
import os.path
# initialize sounds
mixer.init()
mixer.music.set_volume(1)

print('press "q" to quit')
# Initial stats
width = 15
vel = 5
score = 0

# high score
directory_path = getcwd()
if "high_score.txt" in listdir(directory_path):

    with open(f'{directory_path}/high_score.txt', 'r') as file:
        text = file.read()
        high_score = int(text)

else:
    open(f'{directory_path}/high_score.txt','w').close()
    high_score = 0

# left obstacle coordinates
obstacle_1_x1 = 0
obstacle_1_y2 = 10
obstacle_2_x2 = 500
obstacle_2_y2 = 10

# generates the coordinates of where the obstacles are placed on the x - axis
def gen_random_coords():
    left = randint(0,500)
    right = randint(0, 500)     # \/upper bound                     \/lower bound
    if abs(right - left) < randint(30,50) and abs(right - left) > 29 and left < right:
        return left, right
    else: #loops until coordinates are in between bounds
        return gen_random_coords()


# game loop
while True:
    #setup pygame
    pygame.init()
    win = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Dodge")

    #player details
    player_x = (250 - 7.5)
    player_y  = (500 - 15)


    coords = gen_random_coords()
    # left obstacle coordinates
    obstacle_1_y1 = 0
    obstacle_1_x2 = coords[0]

    # right obstacle coordinates
    obstacle_2_x1 = coords[1]
    obstacle_2_y1 = 0


    run = True
    while run:
        pygame.time.delay(25)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        win.fill((0,0,0))

        # define the player and obstacles
        player = pygame.draw.rect(win,(255,255,255),(player_x,player_y,width,width))
        obstacle_1 = pygame.draw.rect(win,(255,255,255),(obstacle_1_x1,obstacle_1_y1,obstacle_1_x2,obstacle_1_y2))
        obstacle_2 = pygame.draw.rect(win,(255,255,255),(obstacle_2_x1,obstacle_2_y1,obstacle_2_x2,obstacle_2_y2))

        # movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_x > 0 or keys[pygame.K_a] and player_x > 0:
            player_x -= vel + score/10
        if keys[pygame.K_RIGHT] and player_x < (500 - width) or keys[pygame.K_d] and player_x < (500 - width):
            player_x += vel + score/10
        if keys[pygame.K_UP] and player_y > 0 or keys[pygame.K_w] and player_y > 0:
            player_y -= vel + score/10
        if keys[pygame.K_DOWN] and player_y < (500 - width) or keys[pygame.K_s] and player_y < (500 - width):
            player_y += vel + score/10

        # display score and highscore
        my_font = pygame.font.SysFont('Comic Sans MS', 20)
        text_surface = my_font.render(f"{str(score)}", False, (255, 255, 255))
        text_surface_2 = my_font.render(f"high score: {str(high_score)}", False, (255, 255, 255))
        win.blit(text_surface, (250,250))
        win.blit(text_surface_2, (0,0))


        # collision
        if player.colliderect(obstacle_1) or player.colliderect(obstacle_2):
            mixer.music.load("fail.mp3")
            mixer.music.play()
            score = 0
            break

        # move obstacles
        obstacle_1_y1 += (5 + score/5)
        obstacle_2_y1 += (5 + score/5)

        # win loop
        pygame.display.update()


        # add to high score
        if int(score) > int(high_score):
            high_score = score
            with open('high_score.txt', 'w') as file:
                file.write(str(high_score))


        # add to score if the player gets passed the obstacle
        if obstacle_1_y1 > player_y + 20:
            mixer.music.load("success.mp3")
            mixer.music.play()
            score += 1
            break

        # end program if q is pressed
        if keys[pygame.K_q]:
            quit()
