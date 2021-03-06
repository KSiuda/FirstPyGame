import pygame
import os
pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 2048)
pygame.mixer.init()
pygame.font.init()


WIDTH, HEIGHT = 900, 500
BORDER_TOP_POSITION = 0
BORDER_WIDTH = 10
BORDER = pygame.Rect(WIDTH/2 - BORDER_WIDTH/2, BORDER_TOP_POSITION, BORDER_WIDTH, HEIGHT)
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First PyGame!")

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Hit_sound.wav'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','Fire_sound.wav'))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 8
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT  = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP, 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP, 270)

SPACE = pygame.image.load(os.path.join('Assets', 'space.png'))
SPACE = pygame.transform.scale(SPACE, (WIDTH, HEIGHT))

YELLOW_SPACESHIP_KEYS = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]
YELLOW_BORDER_POSITIONS = [0,BORDER.x, 0, HEIGHT]

RED_SPACESHIP_KEYS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
RED_BORDER_POSITIONS = [BORDER.x, WIDTH, 0, HEIGHT]

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
        WIN.blit(SPACE, (0,0))
        pygame.draw.rect(WIN, BLACK, BORDER)

        red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
        yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
        WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() -10, 10))
        WIN.blit(yellow_health_text, (10, 10))
        

        WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
        WIN.blit(RED_SPACESHIP, (red.x, red.y))

        for bullet in red_bullets:
            pygame.draw.rect(WIN, RED, bullet)

        for bullet in yellow_bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)


        pygame.display.update()

def handle_ship_movement(keys_pressed, ship, ship_keys_list, border_positions):
    if keys_pressed[ship_keys_list[0]] and ship.x - VELOCITY > border_positions[0]:
            ship.x -= VELOCITY
    if keys_pressed[ship_keys_list[1]] and ship.x + VELOCITY < border_positions[1]:
            ship.x += VELOCITY
    if keys_pressed[ship_keys_list[2]] and ship.y - VELOCITY > border_positions[2] :
            ship.y -= VELOCITY
    if keys_pressed[ship_keys_list[3]] and ship.y + SPACESHIP_HEIGHT + VELOCITY < border_positions[3]: 
            ship.y += VELOCITY

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2 ,
                         HEIGHT/2 - draw_text.get_height() / 2))

    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(800,220, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,220, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []
    bullet_width = 10
    bullet_height = 5

    red_health = 10
    yellow_health = 10


    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height/2, bullet_width, bullet_height)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height/2, bullet_width, bullet_height)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text =""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text ="Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            main()

        
        keys_pressed = pygame.key.get_pressed()
        handle_ship_movement(keys_pressed, yellow, YELLOW_SPACESHIP_KEYS, YELLOW_BORDER_POSITIONS)
        handle_ship_movement(keys_pressed, red, RED_SPACESHIP_KEYS, RED_BORDER_POSITIONS)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)


        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

        

if __name__ == "__main__":
    main()            