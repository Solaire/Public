from pygame import *
import sys
from os.path import abspath, dirname
from random import *

BASE_PATH = abspath(dirname(__file__))

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Window size
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 700
FPS = 20

# Game area
GAME_AREA_WIDTH = 500
GAME_AREA_HEIGHT = 500
GAME_AREA_X_POS = 100
GAME_AREA_Y_POS = 100

# Game states
MENU_STATE = 0
PLAY_STATE = 1
GAME_OVER_STATE = 2
END_STATE = 3

# Font and font size
FONT = BASE_PATH + '/common/font.ttf'
FONT_SIZE_TITLE = 50
FONT_SIZE_PROMPT = 25
FONT_SIZE_SCORE = 30

# Text location
TITLE_TEXT_POS_X = 130
TITLE_TEXT_POS_Y = (SCREEN_HEIGHT // 2) - 100
PLAY_PROMPT_TEXT_POS_X = 80
PLAY_PROMPT_TEXT_POS_Y = (SCREEN_HEIGHT // 2)

SCORE_TEXT_POS_X = GAME_AREA_X_POS
SCORE_TEXT_POS_Y = 50
HI_SCORE_TEXT_POS_X = (SCREEN_WIDTH // 2)
HI_SCORE_TEXT_POS_Y = 50

# Snake directions
DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 3
DIRECTION_RIGHT = 4

# Snake and food size
SIZE = 10

'''
Calculate and return the closest divisible of n / m
'''
def FindClosestDivisible(n, m):
    # Find the quotient
    q = int(n / m)

    # 1st possible closeset number
    n1 = int(m * q)

    # 2nd possible closest number
    n2 = 0

    if m * m > 0:
        n2 = int(m * (q + 1))
    else:
        n2 = int(m * (q - 1))

    # If true, this is the closest number
    if abs(n - n1) < abs(n - n2):
        return n1

    # else this is the closest number
    return n2

'''
Text drawing class
'''
class Text(object):
    def __init__(self, textFont, size, message, color, xpos, ypos):
        self.font = font.Font(textFont, size)
        self.surface = self.font.render(message, True, color)
        self.rect = self.surface.get_rect(topleft=(xpos, ypos))

    '''
    Draw text to screen
    '''
    def Draw(self, surface):
        surface.blit(self.surface, self.rect)

'''
Snake food class
'''
class Food:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = SIZE
        self.colour = WHITE
        self.SetRandomPosition(None)

    '''
    Return current food position
    '''
    def GetPosition(self):
        return Vector2(self.x, self.y)

    '''
    Set radnom position, snapping it to the invisible "grid"
    This function does not check if the position is occupied by snake parts
    '''
    def SetRandomPosition(self, snake):
        if snake is None:
            x = uniform(GAME_AREA_X_POS, GAME_AREA_X_POS + GAME_AREA_WIDTH - 20)
            y = uniform(GAME_AREA_Y_POS, GAME_AREA_Y_POS + GAME_AREA_HEIGHT - 20)
            self.x = FindClosestDivisible(x, SIZE)
            self.y = FindClosestDivisible(y, SIZE)
        else:
            overlap = True
            while overlap:
                overlap = False
                x = FindClosestDivisible(uniform(GAME_AREA_X_POS, GAME_AREA_X_POS + GAME_AREA_WIDTH - 20), SIZE)
                y = FindClosestDivisible(uniform(GAME_AREA_Y_POS, GAME_AREA_Y_POS + GAME_AREA_HEIGHT - 20), SIZE)
                for i in range(1, len(snake.parts)):
                    tmp = snake.parts[i].GetPosition()
                    if tmp.x == x and tmp.y == y:
                        overlap = True
            self.x = x
            self.y = y

    '''
    Draw food to screen
    '''
    def Draw(self, screen):
        draw.rect(screen, self.colour, Rect(self.x, self.y, self.size, self.size))

'''
Represents snake's invidicual cells
'''
class SnakePart:
    def __init__(self, x, y, size, colour):
        self.x = x
        self.y = y
        self.size = size
        self.colour = colour

    '''
    Return position of the cell
    '''
    def GetPosition(self):
        return Vector2(self.x, self.y)

    '''
    Set position of the cell
    '''
    def SetPosition(self, vec2Pos):
        self.x = vec2Pos.x
        self.y = vec2Pos.y

    '''
    If the cell's position is outside of game area, set the position to the opposite size of the axis
    This allows the snake to "wrap around the game area"
    '''
    def MaybeWrapAround(self):
        if self.x < GAME_AREA_X_POS:
            self.x = GAME_AREA_X_POS + GAME_AREA_WIDTH - 20
        elif self.x > GAME_AREA_X_POS + GAME_AREA_WIDTH - 20:
            self.x = GAME_AREA_X_POS

        if self.y < GAME_AREA_Y_POS:
            self.y = GAME_AREA_Y_POS + GAME_AREA_HEIGHT - 20
        elif self.y > GAME_AREA_Y_POS + GAME_AREA_HEIGHT - 20:
            self.y = GAME_AREA_Y_POS

        self.x = FindClosestDivisible(self.x, SIZE)
        self.y = FindClosestDivisible(self.y, SIZE)

    '''
    Move the cell's position by x and y
    '''
    def Move(self, x, y):
        self.x += x
        self.y += y

    '''
    Set cell's colour
    '''
    def SetColour(self, colour):
        self.colour = colour

    ''' 
    Draw cell to screen
    '''
    def Draw(self, screen):
        draw.rect(screen, self.colour, Rect(self.x, self.y, self.size, self.size))

'''
Snake class
Contains array of snake parts
'''
class Snake:
    def __init__(self):
        self.parts = []
        self.direction  = DIRECTION_UP
        self.directionChanged = False
        self.Reset()

    '''
    Reset snake's state to default
    '''
    def Reset(self):
        self.parts = []
        almostRed = (255, 10, 0)

        initX = int(SCREEN_WIDTH / 2)
        initY = int(SCREEN_WIDTH / 2)
        self.parts.append(SnakePart(FindClosestDivisible(initX, SIZE), FindClosestDivisible(initY, SIZE), SIZE, almostRed))

    '''
    Get snake's movement vector
    '''
    def GetMovement(self):
        dir = self.GetDirection()
        offset = Vector2(dir.x * SIZE, dir.y * SIZE)
        return offset

    '''
    Get snake's direction of travel
    '''
    def GetDirection(self):
        dir = Vector2(0, 0)

        if self.direction == DIRECTION_LEFT:
            dir.x = -1

        elif self.direction == DIRECTION_RIGHT:
            dir.x = 1

        elif self.direction == DIRECTION_UP:
            dir.y = -1

        elif self.direction == DIRECTION_DOWN:
            dir.y = 1

        self.directionChanged = False
        return dir

    '''
    Set colour of a specified cell
    Colour is a rainbow gradient
    '''
    def SetColour(self, cell):
        r = 0
        g = 0
        b = 0

        colourPicker = int(((len(self.parts) - 1 ) % 150) / 25)
        snakePartCountMod25 = (len(self.parts) - 1) % 25

        if colourPicker == 0:
            r = 255
            g = 10 * snakePartCountMod25
            b = 0

        elif colourPicker == 1:
            r = 255 - 10 * snakePartCountMod25
            g = 255
            b = 0

        elif colourPicker == 2:
            r = 0
            g = 255
            b = 10 * snakePartCountMod25

        elif colourPicker == 3:
            r = 0
            g = 255 - 10 * snakePartCountMod25
            b = 255

        elif colourPicker == 4:
            r = 10 * snakePartCountMod25
            g = 0
            b = 255

        elif colourPicker == 5:
            r = 255
            g = 0
            b = 255 - 10 * snakePartCountMod25

        colour = (r, g, b)
        cell.SetColour(colour)

    '''
    Move the snake along its direction of travel
    '''
    def Move(self):
        previousPos = self.parts[0].GetPosition()
        movement = self.GetMovement()

        self.parts[0].Move(movement.x, movement.y)
        self.parts[0].MaybeWrapAround()

        # Due to each cell having a different colour, we need to move each cell
        # Otherwise a solution would be to move the last cell (tail) to the head
        for i in range(1, len(self.parts)):
            tmp = self.parts[i].GetPosition()
            self.parts[i].SetPosition(previousPos)
            previousPos = tmp

    '''
    Change snake's direction of travel
    '''
    def ChangeDirection(self, newDirection):
        if abs(newDirection - self.direction) > 1 and self.directionChanged == False:
            self.direction = newDirection
            self.directionChanged = True

    '''
    Add a cell to snake's tail
    '''
    def AddBodyPart(self):
        bodyPart = SnakePart(-16, -16, SIZE, WHITE)
        self.SetColour(bodyPart)
        self.parts.append(bodyPart)

    '''
    Return true if snake's head overlaps with other body part
    Otherwise false
    '''
    def IsBitingSelf(self):
        headPos = self.GetHeadPosition()
        for i in range(1, len(self.parts)):
            partPos = self.parts[i].GetPosition()
            if headPos == partPos:
                return True

        return False

    '''
    Get position of snake's head
    '''
    def GetHeadPosition(self):
        return self.parts[0].GetPosition()

    '''
    Draw snake to the screen
    '''
    def Draw(self, game):
        for part in self.parts:
            part.Draw(game)

'''
Main game class
'''
class Game:
    def __init__(self):
        init()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        display.set_caption("Rainbow Snake")
        icon = image.load(BASE_PATH + '/common/snake.ico')
        display.set_icon(icon)
        self.clock = time.Clock()
        self.timer = time.get_ticks()

        self.score = 0
        self.hiScore = 0
        
        self.snake = Snake()
        self.food = Food()

    def Run(self):
        state   = MENU_STATE
        newGame = False
        ticks   = 0

        # Game loop
        while state is not END_STATE:
            self.screen.fill((0, 0, 0)) # Clear screen

            # Get key events or all states
            for evt in event.get():
                if evt.type == QUIT or (evt.type == KEYDOWN and evt.key == K_ESCAPE):
                    state = END_STATE
                    break

                if state == MENU_STATE or state == GAME_OVER_STATE:
                    if evt.type == KEYDOWN and (evt.key == K_SPACE or evt.key == K_RETURN):
                        state = PLAY_STATE
                        newGame = True

                elif state == PLAY_STATE:
                    if evt.type == KEYDOWN and evt.key == K_LEFT:
                        self.snake.ChangeDirection(DIRECTION_LEFT)
                    elif evt.type == KEYDOWN and evt.key == K_RIGHT:
                        self.snake.ChangeDirection(DIRECTION_RIGHT)
                    elif evt.type == KEYDOWN and evt.key == K_UP:
                        self.snake.ChangeDirection(DIRECTION_UP)
                    elif evt.type == KEYDOWN and evt.key == K_DOWN:
                        self.snake.ChangeDirection(DIRECTION_DOWN)

            if state == END_STATE:
                continue

            # Update game based on state
            if state == MENU_STATE:
                self.DrawMenuState()

            elif state == PLAY_STATE:
                if newGame:
                    self.ResetGame()
                    newGame = False
                self.UpdateGame()
                if self.IsFailure():
                    state = GAME_OVER_STATE

            if state is not MENU_STATE:
                # Draw the studd
                self.DrawGameArea()
                self.snake.Draw(self.screen)
                self.food.Draw(self.screen)

                # Draw text
                scoreText      = Text(FONT, FONT_SIZE_SCORE, "Score: " + str(self.score),      WHITE, SCORE_TEXT_POS_X,    SCORE_TEXT_POS_Y)
                hiScoreText    = Text(FONT, FONT_SIZE_SCORE, "Hi Score: "+ str(self.hiScore),  WHITE, HI_SCORE_TEXT_POS_X, HI_SCORE_TEXT_POS_Y)
                scoreText.Draw(self.screen)
                hiScoreText.Draw(self.screen)

                if(state == GAME_OVER_STATE):
                    ticks += 1
                    self.DrawGameOver(ticks)

            # Update the screen
            display.flip()
            self.clock.tick(FPS)

    '''
    Reset game state
    '''
    def ResetGame(self):
        self.snake.Reset()
        self.food = Food()
        self.keys = key.get_pressed()
        self.timer = time.get_ticks()
        self.noteTimer = time.get_ticks()
        self.snakeAlive = True
        self.score = 0

    '''
    Update game logic
    '''
    def UpdateGame(self):        
        self.snake.Move()

        if self.snake.GetHeadPosition() == self.food.GetPosition():
            self.food.SetRandomPosition(self.snake)
            self.snake.AddBodyPart()
            self.score += 1
            if self.hiScore < self.score:
                self.hiScore = self.score

    '''
    Check if failure condition has been reached
    '''
    def IsFailure(self):
        if self.snake.IsBitingSelf():
            return True

        vec2SnakePos = self.snake.GetHeadPosition()
        if (vec2SnakePos.x < 0 or vec2SnakePos.x > SCREEN_WIDTH) and ((vec2SnakePos.y < 0 or vec2SnakePos.y > SCREEN_HEIGHT)):
            return True

        return False
    
    '''
    Display game over screen
    '''
    def DrawGameOver(self, ticks):
        if (ticks % FPS) < 13:
            gameOverText = Text(FONT, FONT_SIZE_TITLE, "Game Over", WHITE, TITLE_TEXT_POS_X + 30, TITLE_TEXT_POS_Y)
            promptText  = Text(FONT, FONT_SIZE_PROMPT, "Press   [SPACE]   or   [ENTER]   to  play", WHITE, PLAY_PROMPT_TEXT_POS_X, PLAY_PROMPT_TEXT_POS_Y)
            gameOverText.Draw(self.screen)
            promptText.Draw(self.screen)

    '''
    Draw game region
    '''
    def DrawGameArea(self):
        draw.rect(self.screen, WHITE, Rect(GAME_AREA_X_POS - 5, GAME_AREA_Y_POS - 5, GAME_AREA_WIDTH, GAME_AREA_HEIGHT))
        draw.rect(self.screen, BLACK, Rect(GAME_AREA_X_POS, GAME_AREA_Y_POS, GAME_AREA_WIDTH - 10, GAME_AREA_HEIGHT - 10))

    '''
    Draw menu
    '''
    def DrawMenuState(self):
        menuText    = Text(FONT, FONT_SIZE_TITLE, "Rainbow snake", WHITE, TITLE_TEXT_POS_X, TITLE_TEXT_POS_Y)
        promptText  = Text(FONT, FONT_SIZE_PROMPT, "Press   [SPACE]   or   [ENTER]   to  play", WHITE, PLAY_PROMPT_TEXT_POS_X, PLAY_PROMPT_TEXT_POS_Y)
        menuText.Draw(self.screen)
        promptText.Draw(self.screen)

if __name__ == '__main__':
    game = Game()
    game.Run()
