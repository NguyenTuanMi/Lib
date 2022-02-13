import pygame
import os
import random
pygame.font.init()
#pygame.mixer.init()

# The spaceship data
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 45

# The window data
WIDTH, HEIGHT = 900, 500
VEL = 5
MAX_BULLETS = 10

# The border
BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)

# The color
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
#BULLER_FIRE_SOUND = pygame.mixer.Sound(os.path.join('resources', 'Gun+Silencer.mp3'))

# The bullet data
red_bullets = []
yellow_bullets = []
bullet_velocity = 7

# red_hit and yellow_hit event
RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

# Font of the health bar and the winner
HEALTH = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 70)

# Change the scale of the window and display it
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First game!s")

# The fps, frames per second
FPS = 60

# Load the picture 
YELLOW_SPACESHIP_PIC = pygame.image.load(
    os.path.join('resources','spaceship_yellow.png'))
RED_SPACESHIP_PIC = pygame.image.load(
    os.path.join('resources','spaceship_red.png'))
# Load the background and change its scale
SPACE = pygame.transform.scale(
pygame.image.load(os.path.join('resources', 'space.png')), (900,500))

# Rotate the spaceship and its scale
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_PIC, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 270)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_PIC, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)

# The controller of the red_spaceship, 
# increasing its coordinates to move around but it cannot get pass the border
def red_spaceship_controller(key_pressed, red):
    if key_pressed[pygame.K_a] and red.x - VEL > 0:
            red.x -= VEL   
    if key_pressed[pygame.K_d] and red.x + VEL + SPACESHIP_WIDTH < BORDER.x:
            red.x += VEL  
    if key_pressed[pygame.K_w] and red.y - VEL > 0:
            red.y -= VEL
    if key_pressed[pygame.K_s] and red.y + VEL + SPACESHIP_HEIGHT < HEIGHT:
            red.y += VEL    

# The controller of the yellow_spaceship, 
# increasing its coordinates to move around but it cannot get pass the border      
def yellow_spaceship_controller(key_pressed, yellow):
    if key_pressed[pygame.K_LEFT] and yellow.x - VEL > BORDER.x + BORDER.width:
            yellow.x -= VEL   
    if key_pressed[pygame.K_RIGHT] and yellow.x + VEL + SPACESHIP_WIDTH < WIDTH :
            yellow.x += VEL  
    if key_pressed[pygame.K_UP] and yellow.y - VEL > 0:
            yellow.y -= VEL
    if key_pressed[pygame.K_DOWN] and yellow.y + VEL + SPACESHIP_HEIGHT < HEIGHT:
            yellow.y += VEL    

#This class deals with bullets, shoot it by increasing its y-coordinates 
def handle_bullet_function(red_bullets, yellow_bullets, red, yellow):
    for bullet in yellow_bullets:
        bullet.x -= bullet_velocity
        if red.colliderect(bullet):
# If it collides the other spaceship, 
# post the RED_HIT event and remove the bullet from the list
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x += bullet_velocity
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

#Draw the winner
def draw_winner(text, COLOR):
    draw_text = WINNER_FONT.render(text, 1, COLOR) 
    # The test written in WINNER_FONT 
    WIN.blit(draw_text,(
    WIDTH/2 - draw_text.get_width() /2, HEIGHT/2 - draw_text.get_height()/2))
    # Show the text
    pygame.display.update()
    # Update the window
    pygame.time.delay(5000)
    # After that, delay the window for 5000 milliseconds

# Draw the window 
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # Draw the background
    WIN.blit(SPACE,(0,0))
    # Draw the black border
    pygame.draw.rect(WIN, BLACK, BORDER)
    # Display 2 spaceships 
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))
    
    # Display the health
    red_health_text = HEALTH.render(
    "Health :" + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH.render(
    "Health :" + str(yellow_health), 1, WHITE)
    
    WIN.blit(red_health_text, (10,10))
    WIN.blit(yellow_health_text, (
    (WIDTH - 10 - yellow_health_text.get_width()),10))

    # Display the bullet of 2 spaceships
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update() 

def main():
    red_health = 15
    yellow_health = 15
    
    red = pygame.Rect(100,100,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(700,100,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) #This will make sure that the code run with the given frame
        for event in pygame.event.get():  #for all the event in the pygame list
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN: # Check all the key have been pressed
                
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                    red.x + red.width, red.y + red.height,10,5)
                    red_bullets.append(bullet)
                    #BULLER_FIRE_SOUND.play()
                
                if event.key == pygame.K_RCTRL and len(yellow_bullets) < MAX_BULLETS:
                    # If we press the left control and the length of red_bullets is 
                    # smaller than the maximum bullets we could during a momment, 
                    # append a bullet, which is a black colored rectangle, to our list
                    bullet = pygame.Rect(
                    yellow.x + yellow.width,yellow.y + yellow.height,10,5)
                    yellow_bullets.append(bullet)
                    #BULLER_FIRE_SOUND.play()
            
            # If the event is the RED_HIT, occured when the red is hit by the enemy's bullet, 
            # disminish 1 point for the red
            if event.type == RED_HIT:
                red_health -= 1
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1
        
        winner_text = ""
        # If the red_health is smaller than 0, decleare that the winner is the yellow
        if red_health <= 0:
            winner_text = "Yellow win "
            draw_winner(winner_text, YELLOW)
            break
        if yellow_health <= 0:
            winner_text = "Red win "
            draw_winner(winner_text, RED)
            break
        
        # Get the key pressed
        key_pressed = pygame.key.get_pressed()
        # Use the spaceship controller
        red_spaceship_controller(key_pressed,red)
        yellow_spaceship_controller(key_pressed,yellow)
        
        # check the bullet and shoot it
        handle_bullet_function(red_bullets, yellow_bullets, red, yellow)
        
        # Draw the window
        draw_window(red, yellow, red_bullets, 
        yellow_bullets, red_health, yellow_health)
     
if __name__ == "__main__": #only run in file name main 
    main()
