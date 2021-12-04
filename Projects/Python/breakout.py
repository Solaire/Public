import pygame
import time
import sys
from random import randint
import os

# Path
BASE_PATH = os.path.abspath(os.path.dirname(__file__))

# Window size
W_WIDTH  = 700 
W_HEIGHT = 700

# Text windows subsection
DIVIDER_LINE_Y      = 125
DIVIDER_LINE_WIDTH  = 6

# Colours
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
PURPLE = (182, 149, 192)
BLUE   = (173, 216, 230)
GREEN  = (144, 238, 144)
YELLOW = (255, 225, 115)
ORANGE = (254, 181, 127)
RED    = (255, 114, 111)

# Ball
BALL_SIZE = 10

# Paddle
PADDLE_LENGTH_S = 100
PADDLE_LENGTH_M = 150
PADDLE_LENGTH_L = 200
PADDLE_WIDTH = 10
LEFT_RIGHT = [-1, 1]

# Misc
FPS = 60 # Frames per second
SCORE_TICK_COUNT = 150 # Pause between scoring a point and new ball

# Text positioning
TEXT_Y       = 10
TEXT_SCORE_X = 100
TEXT_LEVEL_X = 400

# Lives
LIVES_X      = 10
LIVES_Y      = 50
LIVES_WIDTH  = 64
LIVES_HEIGHT = 64

# Bricks
COLOURS = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
BRICK_ROW_COUNT = 6
BRICK_COL_COUNT = 10
BRICK_WIDTH     = 70
BRICK_HEIGHT    = 35
BRICK_POS_X     = 0
BRICK_POS_Y     = 210

'''
Ball class
'''
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.size   = BALL_SIZE
        self.colour = WHITE
        self.image  = pygame.Surface((self.size, self.size))
        self.image.fill(self.colour)
        self.rect   = self.image.get_rect()

        left_or_right = randint(0, 1)
        self.velocity = [randint(-10, 10) * LEFT_RIGHT[left_or_right], randint(-10, -6)]
        self.in_play = False

        pygame.draw.rect(self.image, self.colour, self.rect)
    
    '''
    Update position of the ball
    '''
    def Update(self, paddle):
        if self.in_play:
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]
        else:
            self.rect.x = paddle.rect.x + (PADDLE_LENGTH_M // 2)
            self.rect.y = paddle.rect.y - self.size

    '''
    Set 'in-play' flag to false and stick to paddle
    '''
    def Reset(self, paddle):
        self.in_play  = False
        self.rect.x   = paddle.rect.x + (PADDLE_LENGTH_M // 2)
        self.rect.y   = paddle.rect.y - self.size

        left_or_right = randint(0, 1)
        self.velocity = [randint(-15, 15) * LEFT_RIGHT[left_or_right], randint(-10, -6)]

    '''
    Reset ball and set 'in-play' flag to true
    '''
    def Play(self, paddle):
        self.Reset(paddle)
        self.in_play = True

    '''
    Reverst vertical velocity and set horizonal velocity to a random value
    '''
    def Bounce(self):
        self.velocity[0] = randint(-8, 8)
        self.velocity[1] *= -1

'''
Player class
'''
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.width  = PADDLE_WIDTH
        self.length = PADDLE_LENGTH_M
        self.colour = WHITE
        self.image  = pygame.Surface((self.length, self.width))
        self.image.fill(self.colour)
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.score  = 0
        self.lives  = 3

        pygame.draw.rect(self.image, self.colour, self.rect)

    '''
    Move paddle by adding pixels to it's current x position
    Position is clipped to the edges of the game area
    '''
    def Move(self, pixels):
        self.rect.x = max(0, min(W_WIDTH - self.length, self.rect.x + pixels))

    '''
    Reset the paddle's life count and the position
    '''
    def SoftReset(self):
        self.lives  = 3
        self.x      = W_WIDTH // 2 - (PADDLE_LENGTH_M // 2)

    '''
    Perform soft reset and set score to 0
    '''
    def HardReset(self):
        self.SoftReset()
        self.score  = 0

    '''
    Draw paddle to screen
    '''
    def Draw(self, screen):
        screen.blit(self.image, self.rect)

'''
Brick class
The bricks are coloured based on the rainbow colours
Each colour has a number of lives, each life lost will change the colour the the previous one
'''
class Brick(pygame.sprite.Sprite):
    def __init__(self, lives, row, column):
        super().__init__()
        self.width  = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.lives  = lives
        self.colour = COLOURS[max(0, min(self.lives, len(COLOURS)))]
        self.row    = row
        self.column = column

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()

    '''
    Update the brick's colour value
    '''
    def Update(self):
        self.colour = COLOURS[max(0, min(self.lives, len(COLOURS)))]
        self.image.fill(self.colour)

    '''
    Draw the brick to screen
    '''
    def Draw(self, screen):
        screen.blit(self.image, self.rect)

'''
Main program class
Handles logic, input and rendering
'''
class Program():
    def __init__(self):
        self.PreInitialise()

        self.player     = Paddle(W_WIDTH // 2 - (PADDLE_LENGTH_M // 2), W_HEIGHT - PADDLE_WIDTH - 50)
        self.ball       = Ball()
        self.bricks     = []
        self.level      = 0
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.ball)
        self.NextLevel()
        self.clock   = pygame.time.Clock()

    '''
    Initialise all system components such as pygame, autio, text, etc.
    '''
    def PreInitialise(self):
        # Pygame pre-initialisation
        pygame.init()
        pygame.font.init()
        pygame.mixer.pre_init()

        # Window initialisation
        self.SCREEN = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
        pygame.display.set_caption("Breakout")

        # Font and audio
        self.FONT = pygame.font.Font(BASE_PATH + '/common/font.ttf', 30)
        pygame.mixer.music.load(BASE_PATH + '/common/pong.mp3')

        # Sprites
        img = pygame.image.load(BASE_PATH + '/common/heart.png').convert_alpha()
        self.sprite_heart = pygame.transform.scale(img, (LIVES_WIDTH, LIVES_HEIGHT))

    '''
    Run main game logic loop
    '''
    def RunGame(self):
        while True:
            # Handle exit events
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    sys.exit(0)

            # Handle keyboard input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.Move(-15)
            if keys[pygame.K_RIGHT]:
                self.player.Move(15)
            if keys[pygame.K_SPACE] and not self.ball.in_play:
                self.ball.Play(self.player)

            if len(self.bricks) == 0:
                self.player.SoftReset()
                self.ball.Reset(self.player)
                self.player.lives += 1
                self.level += 1
                self.NextLevel()

            self.ball.Update(self.player)  
            self.player.update()
            for brick in self.bricks:
                brick.Update()

            self.CheckCollisionBrick()
            self.CheckCollisionWall()
            self.CheckCollisionPaddle() 

            # ----- DRAWING -----
            # Draw sprites
            self.SCREEN.fill(BLACK)
            self.all_sprites.draw(self.SCREEN)
            for brick in self.bricks:
                brick.Draw(self.SCREEN)

            # Draw text
            txt_score = self.FONT.render("SCORE: " + str(self.player.score), 1, WHITE)
            txt_level = self.FONT.render("LEVEL: " + str(self.level), 1, WHITE)

            self.SCREEN.blit(txt_score, (TEXT_SCORE_X, TEXT_Y))
            self.SCREEN.blit(txt_level, (TEXT_LEVEL_X, TEXT_Y))

            # Draw remaining lives
            x = LIVES_X
            for i in range(0, self.player.lives):
                self.SCREEN.blit(self.sprite_heart, (x, LIVES_Y))
                x += 75

            # Draw dividing line
            pygame.draw.line(self.SCREEN, WHITE, (0, DIVIDER_LINE_Y), (W_WIDTH, DIVIDER_LINE_Y), DIVIDER_LINE_WIDTH)

            # Update the screen
            pygame.display.flip()
            self.clock.tick(FPS)

    '''
    Check if the ball is colliding with the brick
    Function returns after a single collision to avoid scenario where a ball is able to hit multiple bricks before changing velocity
    '''
    def CheckCollisionBrick(self):
        for brick in self.bricks:
            x_collide = self.ball.rect.x >= brick.rect.x - self.ball.size and self.ball.rect.x <= brick.rect.x + brick.width
            y_collide = self.ball.rect.y >= brick.rect.y and self.ball.rect.y <= brick.rect.y + brick.height

            if x_collide and y_collide:
                brick.lives             -= 1
                self.player.score       += 1
                self.ball.Bounce()
                pygame.mixer.music.play(0)

                if brick.lives < 0:
                    self.bricks.remove(brick)
                return

    '''
    Check if the ball bounced off a wall or if player lost a life (below the paddle)
    Change ball velocity if it has 
    '''
    def CheckCollisionWall(self):
        if self.ball.rect.x > W_WIDTH: # Collision with right wall
            self.ball.velocity[0] *= -1
            self.ball.rect.x = W_WIDTH - self.ball.size
            pygame.mixer.music.play(0)
        elif self.ball.rect.x < 0: # Collision with left wall
            self.ball.velocity[0] *= -1
            self.ball.rect.x = 0
            pygame.mixer.music.play(0)
        elif self.ball.rect.y < DIVIDER_LINE_Y + DIVIDER_LINE_WIDTH: # Collision with top wall
            self.ball.velocity[1] *= -1
            pygame.mixer.music.play(0)
        elif self.ball.rect.y > W_HEIGHT: # Collision with bottom
            self.ball.Reset(self.player)
            self.player.lives -= 1
            if self.player.lives < 0:
                print("Game over!")
                sys.exit(0)

    '''
    Check if the ball is collising with the paddle
    Bounce if it has
    '''
    def CheckCollisionPaddle(self):        
        p1_collision_x = self.ball.rect.x >= self.player.rect.x - self.ball.size and self.ball.rect.x <= self.player.rect.x + PADDLE_LENGTH_M
        p1_collision_y = self.ball.rect.y >= self.player.rect.y and self.ball.rect.y <= self.player.rect.y + PADDLE_WIDTH

        if p1_collision_x and p1_collision_y:
            self.ball.Bounce()
            pygame.mixer.music.play(0)
            self.ball.rect.y = self.player.rect.y - PADDLE_WIDTH

    '''
    Prepare next level, spawning bricks
    '''
    def NextLevel(self):
        brick_group = pygame.sprite.Group()
        for row in range(BRICK_ROW_COUNT):
            for column in range(BRICK_COL_COUNT):
                lives        = max(0, min(len(COLOURS) - 1, self.level - row))
                brick        = Brick(lives, row, column)
                brick.rect.x = BRICK_POS_X + (BRICK_WIDTH * column)
                brick.rect.y = BRICK_POS_Y + (BRICK_HEIGHT * row)
                self.bricks.append(brick)

if __name__ == '__main__':
    game = Program()
    game.RunGame()
