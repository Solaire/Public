import pygame
import time
import sys
from random import randint
from os.path import abspath, dirname

# Path
BASE_PATH = abspath(dirname(__file__))

# Window size
W_WIDTH  = 1200 
W_HEIGHT = 800

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Ball
BALL_SIZE = 10

# Paddle
PADDING  = 100
PADDLE_L = 100
PADDLE_W = 10

# Misc
FPS = 60 # Frames per second
SCORE_TICK_COUNT = 150 # Pause between scoring a point and new ball

# Text positioning
TEXT_SCORE_Y   = W_HEIGHT // 5
PLAYER_1_SCORE = W_WIDTH // 4
PLAYER_2_SCORE = W_WIDTH - 50 - (W_WIDTH // 4)

LEFT_RIGHT = [-1, 1]

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
        self.velocity = [randint(6, 10) * LEFT_RIGHT[left_or_right], randint(-10, 10)]
        self.in_play = False

        pygame.draw.rect(self.image, self.colour, self.rect)
    
    '''
    Update position
    '''
    def Update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    '''
    Reset ball's position and set 'in-play' flag to false
    '''
    def Reset(self):
        self.in_play  = False
        self.rect.x   = (W_WIDTH // 2)  - self.size
        self.rect.y   = (W_HEIGHT // 2) - self.size

        left_or_right = randint(0, 1)
        self.velocity = [randint(6, 10) * LEFT_RIGHT[left_or_right], 0]

    '''
    Reset positon and set 'in play' flag to true
    '''
    def Play(self):
        self.Reset()
        self.in_play = True

    '''
    Bounce off wall
    '''
    def Bounce(self):
        self.velocity[0] *= -1
        self.velocity[1] = randint(-10, 10)

'''
Player class
'''
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.length = PADDLE_L
        self.width  = PADDLE_W
        self.colour = WHITE
        self.image  = pygame.Surface((self.width, self.length))
        self.image.fill(self.colour)
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.score  = 0

        pygame.draw.rect(self.image, self.colour, self.rect)

    '''
    Move paddle 
    '''
    def Move(self, pixels):
        self.rect.y = max(0, min(W_HEIGHT - self.length, self.rect.y + pixels))

    '''
    Draw to screen
    '''
    def Draw(self, screen):
        screen.blit(self.image, self.rect)

'''
Main class
'''
class Program():
    def __init__(self):
        self.PreInitialise()

        self.player1    = Paddle(PADDING, W_HEIGHT // 2 - (PADDLE_L // 2))
        self.player2    = Paddle(W_WIDTH - (PADDING + PADDLE_W), W_HEIGHT // 2 - (PADDLE_L // 2))
        self.ball       = Ball()
        self.pause_ticks = 0

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)
        self.all_sprites.add(self.ball)
        
        self.clock   = pygame.time.Clock()

    '''
    Set up font, screen and audio components
    '''
    def PreInitialise(self):
        # Pygame pre-initialisation
        pygame.init()
        pygame.font.init()
        pygame.mixer.pre_init()

        # Window initialisation
        self.SCREEN = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
        pygame.display.set_caption("PONG!")

        # Font and audio
        self.FONT = pygame.font.Font(BASE_PATH + '/common/font.ttf', 100)
        pygame.mixer.music.load(BASE_PATH + '/common/Pong.mp3')

    '''
    Main game loop
    '''
    def RunGame(self):
        while True:
            # Handle exit events
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    sys.exit(0)

            # Handle keyboard input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player1.Move(-15)
            if keys[pygame.K_s]:
                self.player1.Move(15)
            if keys[pygame.K_UP]:
                self.player2.Move(-15)
            if keys[pygame.K_DOWN]:
                self.player2.Move(15)

            # Update the pause tick counter (pause between each round)
            if self.pause_ticks > 0:
                self.pause_ticks = (self.pause_ticks + 1) % SCORE_TICK_COUNT

            if self.ball.in_play:
                self.ball.Update()
            elif self.pause_ticks == 0:
                self.ball.Play()

            self.player1.Draw(self.SCREEN)
            self.player2.Draw(self.SCREEN)

            self.CheckScore()
            self.CheckCollisionWall()
            self.CheckCollisionPaddle() 

            # Drawing
            self.SCREEN.fill(BLACK)
            self.DrawNet()
            self.all_sprites.draw(self.SCREEN)

            # Draw score
            txt_player_1 = self.FONT.render(str(self.player1.score), 1, WHITE)
            txt_player_2 = self.FONT.render(str(self.player2.score), 1, WHITE)
            self.SCREEN.blit(txt_player_1, (PLAYER_1_SCORE, TEXT_SCORE_Y))
            self.SCREEN.blit(txt_player_2, (PLAYER_2_SCORE, TEXT_SCORE_Y))

            # Update the screen
            pygame.display.flip()
            self.clock.tick(FPS)

    '''
    Check if any of the players has scored
    '''
    def CheckScore(self):
        scored = False
        if self.ball.rect.x > W_WIDTH:
            self.player1.score += 1
            scored = True

        if self.ball.rect.x < 0:
            self.player2.score += 1
            scored = True

        if scored:
            self.ball.Reset()
            self.pause_ticks = 1
            pygame.mixer.music.play(0)

    '''
    Check if the ball collided with the wall
    '''
    def CheckCollisionWall(self):
        if self.ball.rect.y > W_HEIGHT:
            self.ball.rect.y = W_HEIGHT - self.ball.size
            self.ball.velocity[1] *= -1
            pygame.mixer.music.play(0)
        elif self.ball.rect.y < 0:
            self.ball.rect.y = 0
            self.ball.velocity[1] *= -1
            pygame.mixer.music.play(0)

    '''
    Check if the ball collided with any of the players
    '''
    def CheckCollisionPaddle(self):        
        p1_collision_x = self.ball.rect.x >= self.player1.rect.x and self.ball.rect.x <= self.player1.rect.x + PADDLE_W
        p1_collision_y = self.ball.rect.y + self.ball.size >= self.player1.rect.y and self.ball.rect.y <= self.player1.rect.y + PADDLE_L
        p2_collision_x = self.ball.rect.x >= self.player2.rect.x and self.ball.rect.x <= self.player2.rect.x + PADDLE_W
        p2_collision_y = self.ball.rect.y + self.ball.size >= self.player2.rect.y and self.ball.rect.y <= self.player2.rect.y + PADDLE_L

        if p1_collision_x and p1_collision_y:
            self.ball.Bounce()
            pygame.mixer.music.play(0)
            self.ball.rect.x = self.player1.rect.x + PADDLE_W

        elif p2_collision_x and p2_collision_y:
            self.ball.Bounce()
            pygame.mixer.music.play(0)
            self.ball.rect.x = self.player2.rect.x - self.ball.size
        

    '''
    Draw center net
    '''
    def DrawNet(self):
        for i in range(100, W_HEIGHT - 100, 40):
            left   = (W_WIDTH // 2) - 3
            top    = i
            width  = 6
            height = 30
            pygame.draw.rect(self.SCREEN, WHITE, pygame.Rect(left, top, width, height))

if __name__ == '__main__':
    game = Program()
    game.RunGame()