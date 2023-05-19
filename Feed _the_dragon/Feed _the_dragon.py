import pygame, random

#Initialise pygame
pygame.init()

#Set Display Surface
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
display_surface = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
pygame.display.set_caption("Feed the Dragon")

#Set FPS and Clock
FPS = 60
clock = pygame.time.Clock()

#Set game values
PLAYER_STARTING_LIVES = 3
PLAYER_VELOCITY = 8
COIN_STARTING_VELOCITY = 8
COIN_ACCELERATION = .5
BUFFER_DISTANCE = 100

score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

#Set Colors
DEEPPINK = (255,20,147)
VIOLET = (148,0,211)
WHITE = (255,255,255)
BLACK = (0,0,0)

#Set Fonts
font = pygame.font.Font('/Users/sammymylove/Desktop/Pygame/Feed _the_dragon/AttackGraffiti.ttf', 32)

#Set Texts
score_text = font.render("Score:" + str(score) , True, DEEPPINK, VIOLET)
score_rect = score_text.get_rect()
score_rect.topleft = (10,10)

title_text = font.render("Feed the Dragon", True, DEEPPINK, WHITE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.centery = 10

lives_text = font.render("Lives:" + str(player_lives), True, DEEPPINK, VIOLET)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10, 10)

game_over_text = font.render("GAMEOVER", True, DEEPPINK, VIOLET)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_HEIGHT//2, WINDOW_WIDTH//2)

continue_text = font.render("Press any key to play again", True, DEEPPINK, VIOLET)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 32)


#Set Sounds and Music
coin_sound = pygame.mixer.Sound('/Users/sammymylove/Desktop/Pygame/Feed _the_dragon/coin_sound.wav')
miss_sound = pygame.mixer.Sound('/Users/sammymylove/Desktop/Pygame/Feed _the_dragon/miss_sound.wav')
miss_sound.set_volume(.1)
pygame.mixer.music.load('/Users/sammymylove/Desktop/Pygame/Feed _the_dragon/ftd_background_music.wav')


#Set Images
player_image = pygame.image.load('/Users/sammymylove/Desktop/Pygame/Feed _the_dragon/dragon_right.png')
player_rect = player_image.get_rect()
player_rect.left  = 32
player_rect.centery = WINDOW_HEIGHT//2

coin_image = pygame.image.load('/Users/sammymylove/Desktop/Pygame/Feed _the_dragon/coin.png')
coin_rect = coin_image.get_rect()
coin_rect.x  = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)


#Loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    #Check if user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Check if user wants to quit
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_rect.top > 64:
        player_rect.y -= PLAYER_VELOCITY
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += PLAYER_VELOCITY

    #Move Coin
    if coin_rect.x < 0:
        #Player missed coin
        player_lives -= 1
        miss_sound.play()
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)
    else:
        #Move coin
        coin_rect.x -= coin_velocity

    #Check for collisions
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_sound.play()
        coin_velocity += COIN_ACCELERATION
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

    #Update HUD
    score_text = font.render("Score:" + str(score) , True, DEEPPINK, VIOLET)
    lives_text = font.render("Lives:" + str(player_lives), True, DEEPPINK, VIOLET)

    #Check for collisions
    if player_lives == 0:
         display_surface.blit(game_over_text,game_over_rect)
         display_surface.blit(continue_text,continue_rect)
         pygame.display.update()

         #Pause game till player press key, then reset game
         pygame.mixer.music.stop()
         is_paused = True
         while is_paused:
             for event in pygame.event.get():
                 #Player wants to play again
                 if event.type == pygame.KEYDOWN:
                     score = 0
                     player_lives = PLAYER_STARTING_LIVES
                     player_rect.y = WINDOW_HEIGHT//2
                     coin_velocity = COIN_STARTING_VELOCITY
                     pygame.mixer.music.play(-1, 0.0)
                     is_paused = False
                 #Player wants to quit
                 if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
             

    #Fill display
    display_surface.fill(BLACK)

    #Blit HUD to screen
    display_surface.blit(score_text,score_rect)
    display_surface.blit(title_text,title_rect)
    display_surface.blit(lives_text,lives_rect)
    pygame.draw.line(display_surface, WHITE, (0,64), (WINDOW_WIDTH, 64), 5)

    #Blit assets to screen
    display_surface.blit(player_image,player_rect)
    display_surface.blit(coin_image,coin_rect)
    
    #Update display and tick the clock 
    pygame.display.update()
    clock.tick(FPS)

#End Game
pygame.quit()